from io import BytesIO
import re
from zipfile import ZipFile, ZIP_DEFLATED

from app.repositories.LlmCatcherRepositoryFactory import (
    LlmCatcherRepositoryFactory
)
from app.services import generator
from app.services.LlmTestCaseService import (
    LlmResponseParseError,
    LlmTestCaseService
)
from assets.components import Method, Parameter, TestSet, ParamRange


class GenerateTestsService:

    def generate_tests_archive(self, data):
        if data is None:
            return {'error': "Invalid Json format provided."}, 400

        methods_json = data.get('methods')

        if not methods_json:
            error_msg = "Invalid JSON body. Please provide a list of methods"
            return {'error': error_msg}, 400

        try:
            methods = self._build_legacy_methods(methods_json)
            generated_files = self._build_generated_files(methods)
        except ValueError as error:
            return {'error': str(error)}, 400

        if not generated_files:
            return {'error': "No tests could be generated from the provided methods"}, 400

        return self._build_file_response(
            generated_files,
            'AutomTestGeneratedTests.zip'
        ), 200

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
        target_language = data.get(
            'targetLanguage',
            data.get('language', 'java')
        )

        if lang not in ['pt', 'en']:
            return {'error': "Field 'lang' must be 'pt' or 'en'"}, 400

        if not methods or not isinstance(methods, list):
            return {'error': "Field 'methods' is required and must be a non-empty list"}, 400

        if (not selected_ia
                or selected_ia.lower() not in LlmCatcherRepositoryFactory.LLM_MAP):
            return {'error': "Field 'selectedIA' must be one of: gpt, gemini, claude"}, 400

        normalized_methods = self._normalize_methods_for_llm(methods, equivalence_classes)
        if not normalized_methods:
            return {'error': "Field 'methods' must contain valid method objects"}, 400

        methods_with_equiv_classes = [
            method
            for method in normalized_methods
            if method.get('equivClasses')
        ]

        if not methods_with_equiv_classes:
            return {
                'error': "At least one method must include at least one equivalence class"
            }, 400

        service = LlmTestCaseService(
            methods=methods_with_equiv_classes,
            lang=lang,
            selected_ia=selected_ia,
            target_language=target_language
        )

        try:
            generated_tests = service.get()
            generated_files = self._build_llm_generated_files(generated_tests)

            if not generated_files:
                return {'error': "No test files could be generated from the LLM response"}, 502

            return self._build_file_response(
                generated_files,
                'AutomTestGeneratedLlmTests.zip'
            ), 200
        except LlmResponseParseError as error:
            return {
                'error': str(error),
                'rawResponse': error.raw_response
            }, 502

    def _build_file_response(self, generated_files, zip_file_name):
        if len(generated_files) == 1:
            file_name, content = next(iter(generated_files.items()))
            file_buffer = BytesIO(content.encode('utf-8'))
            file_buffer.seek(0)

            return {
                'buffer': file_buffer,
                'download_name': file_name,
                'mimetype': 'text/x-java-source'
            }

        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w', ZIP_DEFLATED) as zip_file:
            for file_name, content in generated_files.items():
                zip_file.writestr(file_name, content)
        zip_buffer.seek(0)

        return {
            'buffer': zip_buffer,
            'download_name': zip_file_name,
            'mimetype': 'application/zip'
        }

    def _build_llm_generated_files(self, generated_tests):
        if isinstance(generated_tests, dict):
            generated_tests = [generated_tests]

        if not isinstance(generated_tests, list):
            return {}

        generated_files = {}
        for test_class in generated_tests:
            if not isinstance(test_class, dict):
                continue

            class_name = (
                test_class.get('testClassName')
                or f"{test_class.get('className', 'Generated')}Test"
            )
            file_name = f"{class_name}.java"
            generated_files[file_name] = self._build_java_test_class(
                class_name,
                test_class
            )

        return {
            file_name: content
            for file_name, content in generated_files.items()
            if content
        }

    def _build_java_test_class(self, class_name, test_class):
        tests = test_class.get('tests') or []
        test_methods = [
            test.get('code')
            for test in tests
            if isinstance(test, dict) and test.get('code')
        ]

        if not test_methods:
            return ''

        package_name = test_class.get('packageName')
        imports = test_class.get('imports') or []

        lines = []
        if package_name:
            lines.extend([f"package {package_name};", ""])

        for import_line in self._normalize_java_imports(imports):
            lines.append(import_line)

        if not any('org.junit' in import_line for import_line in lines):
            lines.append("import org.junit.jupiter.api.Test;")

        lines.extend(["", f"public class {class_name} {{"])
        for test_method in test_methods:
            lines.append("")
            lines.append(self._indent_java_code(test_method, 4))
        lines.append("}")

        return "\n".join(lines)

    def _normalize_java_imports(self, imports):
        normalized_imports = []

        for import_line in imports:
            if not isinstance(import_line, str) or not import_line.strip():
                continue

            import_line = import_line.strip()
            if not import_line.startswith('import '):
                import_line = f"import {import_line}"
            if not import_line.endswith(';'):
                import_line = f"{import_line};"

            if import_line not in normalized_imports:
                normalized_imports.append(import_line)

        return normalized_imports

    def _indent_java_code(self, code, spaces):
        prefix = ' ' * spaces
        stripped_code = code.strip()

        if stripped_code.startswith('public class ') or ' class ' in stripped_code[:80]:
            return stripped_code

        return "\n".join(
            f"{prefix}{line}" if line.strip() else ""
            for line in stripped_code.splitlines()
        )

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
            normalized_method['equivClasses'] = self._extract_method_equiv_classes(method)
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
                self._append_equiv_class(target_method, equiv_class)
            elif len(normalized_methods) == 1:
                self._append_equiv_class(normalized_methods[0], equiv_class)

        return normalized_methods

    def _extract_method_equiv_classes(self, method):
        equiv_classes = (
            method.get('equivClasses')
            or method.get('equivalenceClasses')
            or method.get('classesEquivalence')
            or []
        )

        if not isinstance(equiv_classes, list):
            return []

        return [
            equiv_class
            for equiv_class in equiv_classes
            if isinstance(equiv_class, dict)
        ]

    def _append_equiv_class(self, method, equiv_class):
        method.setdefault('equivClasses', [])

        if any(self._is_same_equiv_class(existing, equiv_class)
               for existing in method['equivClasses']):
            return

        method['equivClasses'].append(equiv_class)

    def _is_same_equiv_class(self, first, second):
        first_identifier = first.get('identifier')
        second_identifier = second.get('identifier')

        if first_identifier and second_identifier:
            return first_identifier == second_identifier

        return (
            first.get('name') == second.get('name')
            and first.get('expectedOutputRange') == second.get('expectedOutputRange')
            and first.get('acceptableParamRanges') == second.get('acceptableParamRanges')
        )

    def _build_legacy_methods(self, methods_json):
        methods = []
        for method_json in methods_json:
            method = Method(
                identifier=method_json.get('identifier'),
                name=method_json.get('name'),
                package_name=method_json.get('packageName') if method_json.get('packageName') else '',
                class_name=method_json.get('className'),
                output_type=self._normalize_type_name(method_json.get('returnType'))
            )
            for parameter in method_json.get('parameters') or []:
                method.add_param_by_parameter(
                    Parameter(
                        identifier=parameter.get('identifier'),
                        name=parameter.get('name'),
                        type_name=self._normalize_type_name(parameter.get('type'))
                    )
                )
            for equiv_class in method_json.get('equivClasses') or []:
                output_json = equiv_class.get('expectedOutputRange') or {}
                output_range = ParamRange(
                    Parameter('saida_esperada', method.output_type),
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
                for param_range in self._build_ordered_param_ranges(
                    method,
                    equiv_class,
                    param_ranges_json
                ):
                    test_set.add_param_range(param_range)
                method.add_testset(test_set)
            if len(method.testsets) > 0:
                methods.append(method)

        return methods

    def _build_ordered_param_ranges(self, method, equiv_class, param_ranges_json):
        ranges_by_param_id = {
            param_range.get('param_id'): param_range
            for param_range in param_ranges_json
            if isinstance(param_range, dict) and param_range.get('param_id')
        }
        ranges_by_param_name = {
            param_range.get('paramName') or param_range.get('name'):
            param_range
            for param_range in param_ranges_json
            if isinstance(param_range, dict)
        }
        ordered_ranges = []

        for param in method.params:
            param_range_json = (
                ranges_by_param_id.get(param.identifier)
                or ranges_by_param_name.get(param.name)
            )

            if not param_range_json:
                raise ValueError(
                    f"Missing range for parameter '{param.name}' "
                    f"in equivalence class '{equiv_class.get('name')}'"
                )

            param_range = ParamRange(
                param,
                param_range_json.get('v1') or '',
                param_range_json.get('v2') or '',
                param_range_json.get('v3') or ''
            )
            self._normalize_param_range_for_generator(param_range)
            self._validate_param_range_for_generator(
                method,
                equiv_class,
                param_range
            )
            ordered_ranges.append(param_range)

        return ordered_ranges

    def _normalize_param_range_for_generator(self, param_range):
        if param_range.param.type_name == 'Date':
            if not self._is_date(param_range.v1):
                param_range.v1 = '01-01-2024'
            if not self._is_date(param_range.v2):
                param_range.v2 = '31-12-2024'

    def _validate_param_range_for_generator(self, method, equiv_class, param_range):
        type_name = param_range.param.type_name
        values = [param_range.v1, param_range.v2, param_range.v3]
        non_empty_values = [value for value in values if value != '']

        if not non_empty_values:
            raise self._invalid_range_error(method, equiv_class, param_range)

        if type_name == 'int':
            valid = (
                self._is_int(param_range.v1)
                and self._is_int(param_range.v2)
                and self._is_optional_number_list(param_range.v3, self._is_int)
            ) or (
                param_range.v1 == ''
                and param_range.v2 == ''
                and self._is_optional_number_list(param_range.v3, self._is_int)
            )
        elif type_name in ['double', 'float']:
            valid = (
                self._is_float(param_range.v1)
                and self._is_float(param_range.v2)
                and self._is_optional_number_list(param_range.v3, self._is_float)
            ) or (
                param_range.v1 == ''
                and param_range.v2 == ''
                and self._is_optional_number_list(param_range.v3, self._is_float)
            )
        elif type_name == 'Date':
            valid = self._is_date(param_range.v1) and self._is_date(param_range.v2)
        elif type_name == 'boolean':
            valid = param_range.v1.lower() in ['true', 'false']
        else:
            valid = True

        if not valid:
            raise self._invalid_range_error(method, equiv_class, param_range)

    def _invalid_range_error(self, method, equiv_class, param_range):
        return ValueError(
            "Invalid range for parameter "
            f"'{param_range.param.name}' ({param_range.param.type_name}) "
            f"in method '{method.name}', equivalence class "
            f"'{equiv_class.get('name')}': "
            f"v1='{param_range.v1}', v2='{param_range.v2}', v3='{param_range.v3}'"
        )

    def _normalize_type_name(self, type_name):
        normalized_type = (type_name or '').strip().lower()

        if normalized_type == 'string':
            return 'String'
        if normalized_type == 'date':
            return 'Date'

        return normalized_type

    def _is_int(self, value):
        return bool(re.fullmatch(r'-?\d+', value or ''))

    def _is_float(self, value):
        return bool(re.fullmatch(r'-?\d+(\.\d+)?', value or ''))

    def _is_optional_number_list(self, value, validator):
        if value == '':
            return True

        return all(
            validator(item)
            for item in value.replace(' ', '').split(';')
            if item != ''
        )

    def _is_date(self, value):
        parts = re.split(r'[-/]', value or '')
        return len(parts) == 3 and all(part.isdigit() for part in parts)
