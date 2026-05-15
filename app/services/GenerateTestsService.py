from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

from app.repositories.LlmCatcherRepositoryFactory import LlmCatcherRepositoryFactory
from app.services import generator
from app.services.LlmTestCaseService import LlmTestCaseService
from assets.components import Method, Parameter, TestSet, ParamRange


class GenerateTestsService:

    def generate_tests_archive(self, data):
        if data is None:
            return {'error': "Invalid Json format provided."}, 400

        methods_json = data.get('methods')

        if not methods_json:
            error_msg = "Invalid JSON body. Please provide a list of methods"
            return {'error': error_msg}, 400

        methods = self._build_legacy_methods(methods_json)
        generated_files = self._build_generated_files(methods)

        if not generated_files:
            return {'error': "No tests could be generated from the provided methods"}, 400

        if len(generated_files) == 1:
            file_name, content = next(iter(generated_files.items()))
            file_buffer = BytesIO(content.encode('utf-8'))
            file_buffer.seek(0)

            return {
                'buffer': file_buffer,
                'download_name': file_name,
                'mimetype': 'text/x-java-source'
            }, 200

        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w', ZIP_DEFLATED) as zip_file:
            for file_name, content in generated_files.items():
                zip_file.writestr(file_name, content)
        zip_buffer.seek(0)

        return {
            'buffer': zip_buffer,
            'download_name': 'AutomTestGeneratedTests.zip',
            'mimetype': 'application/zip'
        }, 200

    def generate_tests_file(self, data):
        if data is None:
            return {'error': "Invalid Json format provided."}, 400

        methods_json = data.get('methods')
        directory = data.get('directory')

        if not methods_json or not directory:
            error_msg = "Invalid JSON body. Please provide a list of methods and a directory to save the result"
            return {'error': error_msg}, 400

        methods = self._build_legacy_methods(methods_json)

        for method in methods:
            generator.generate_tests(method, directory)

        return "Success generating tests", 200

    def generate_tests_with_llm(self, data):
        if data is None:
            return {'error': "Invalid Json format provided."}, 400

        methods = data.get('methods')
        equivalence_classes = (
            data.get('equivalenceClasses')
            or data.get('equivClasses')
            or data.get('classesEquivalence')
        )
        lang = data.get('lang', 'pt')
        selected_ia = data.get('selectedIA', 'gpt')
        target_language = data.get('targetLanguage', data.get('language', 'java'))

        if lang not in ['pt', 'en']:
            return {'error': "Field 'lang' must be 'pt' or 'en'"}, 400

        if not methods or not isinstance(methods, list):
            return {'error': "Field 'methods' is required and must be a non-empty list"}, 400

        if not selected_ia or selected_ia.lower() not in LlmCatcherRepositoryFactory.LLM_MAP:
            return {'error': "Field 'selectedIA' must be one of: gpt, gemini, deepseek"}, 400

        normalized_methods = self._normalize_methods_for_llm(methods, equivalence_classes)
        if not normalized_methods:
            return {'error': "Field 'methods' must contain valid method objects"}, 400

        methods_without_equiv_classes = [
            method.get('name') or method.get('identifier')
            for method in normalized_methods
            if not method.get('equivClasses')
        ]

        if methods_without_equiv_classes:
            return {
                'error': "Every method must include at least one equivalence class",
                'methodsWithoutEquivalenceClasses': methods_without_equiv_classes
            }, 400

        service = LlmTestCaseService(
            methods=normalized_methods,
            lang=lang,
            selected_ia=selected_ia,
            target_language=target_language
        )

        return service.get(), 200

    def _build_generated_files(self, methods):
        generated_files = {}
        test_counter_by_file = {}

        for method in methods:
            file_name = f"{method.class_name}Test.java"

            if file_name not in generated_files:
                generated_files[file_name] = generator.header_content(method)
                test_counter_by_file[file_name] = 1

            for testset_position in range(0, len(method.testsets)):
                methods_already_written = []
                retries = 1000
                generated_count = 0

                while generated_count < method.testsets[testset_position].number_of_cases:
                    test_method_generated = generator.test_content(
                        method,
                        method.testsets[testset_position].name,
                        test_counter_by_file[file_name],
                        testset_position
                    )

                    if generator.methodDoesNotExistYet(test_method_generated, methods_already_written):
                        generated_files[file_name] += test_method_generated
                        methods_already_written.append(test_method_generated)
                        test_counter_by_file[file_name] += 1
                        generated_count += 1
                    elif retries != 0:
                        retries -= 1
                    else:
                        break

        return {
            file_name: f"{content}\n}}"
            for file_name, content in generated_files.items()
        }

    def _normalize_methods_for_llm(self, methods, equivalence_classes=None):
        normalized_methods = []

        for method in methods:
            if not isinstance(method, dict):
                continue

            normalized_method = dict(method)
            normalized_method['equivClasses'] = list(method.get('equivClasses') or [])
            normalized_methods.append(normalized_method)

        if not equivalence_classes:
            return normalized_methods

        method_by_identifier = {
            method.get('identifier'): method
            for method in normalized_methods
            if method.get('identifier')
        }
        method_by_name = {
            method.get('name'): method
            for method in normalized_methods
            if method.get('name')
        }

        for equiv_class in equivalence_classes:
            if not isinstance(equiv_class, dict):
                continue

            method_identifier = (
                equiv_class.get('methodIdentifier')
                or equiv_class.get('methodId')
                or equiv_class.get('method_id')
            )
            method_name = equiv_class.get('methodName') or equiv_class.get('method')

            target_method = method_by_identifier.get(method_identifier) or method_by_name.get(method_name)
            if target_method is not None:
                target_method.setdefault('equivClasses', []).append(equiv_class)
            elif len(normalized_methods) == 1:
                normalized_methods[0].setdefault('equivClasses', []).append(equiv_class)

        return normalized_methods

    def _build_legacy_methods(self, methods_json):
        methods = []
        for method_json in methods_json:
            method = Method(
                identifier=method_json.get('identifier'),
                name=method_json.get('name'),
                package_name=method_json.get('packageName') if method_json.get('packageName') else '',
                class_name=method_json.get('className'),
                output_type=method_json.get('returnType')
            )
            for parameter in method_json.get('parameters') or []:
                method.add_param_by_parameter(
                    Parameter(
                        identifier=parameter.get('identifier'),
                        name=parameter.get('name'),
                        type_name=parameter.get('type')
                    )
                )
            for equiv_class in method_json.get('equivClasses') or []:
                output_json = equiv_class.get('expectedOutputRange') or {}
                output_range = ParamRange(
                    Parameter('saida_esperada', method_json.get('returnType')),
                    output_json.get('v1'),
                    output_json.get('v2'),
                    output_json.get('v3')
                )
                test_set = TestSet(
                    name=equiv_class.get('name'),
                    number_of_cases=equiv_class.get('numberOfCases'),
                    expected_range=output_range,
                    identifier=equiv_class.get('identifier'),
                )

                param_ranges_json = equiv_class.get('acceptableParamRanges') or []
                for param_range_json in param_ranges_json:
                    param = method.findParamByIdentifier(param_range_json.get('param_id'))
                    test_set.add_param_range(
                        ParamRange(
                            param,
                            param_range_json.get('v1'),
                            param_range_json.get('v2'),
                            param_range_json.get('v3')
                        )
                    )
                method.add_testset(test_set)
            if len(method.testsets) > 0:
                methods.append(method)

        return methods
