from flask import Flask, jsonify, request
from flask_cors import cross_origin
import traceback
from assets import generator
from assets.components import get_methods_from_test_cases, Method, Parameter, TestSet, ParamRange
from assets.ui import MethodCatcherService

app = Flask(__name__)


# Define a route for the API
@app.route('/api/greet', methods=['GET'])
@cross_origin()
def greet():
    """Endpoint for greeting."""
    response = {
        "message": "Hello, Welcome to the API!"
    }
    return jsonify(response)


@app.route('/api/generate_tests', methods=['POST'])
@cross_origin()
def generate_tests():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        if data is None:
            return jsonify({'error': "Invalid Json format provided."}), 400

        # Extract relevant fields
        methodsJson = data.get('methods')
        directory = data.get('directory')

        if methodsJson is None or methodsJson is []:
            errorMsg = "Invalid JSON body. Please provide a list of methods and a directory to save the result"
            return jsonify({'error': errorMsg}), 400

        #TODO: validar cada classe de equivalência fornecida: têm todos os campos necessários?
        #TODO: directory é um local válido?

        #Get methods from request body
        methods = []
        for methodJson in methodsJson:
            method = Method(
                            identifier=methodJson.get('identifier'),
                            name=methodJson.get('name'),
                            package_name=methodJson.get('packageName') if methodJson.get('packageName') else '',
                            class_name=methodJson.get('className'),
                            output_type=methodJson.get('returnType')
            )
            print(method)
            for parameter in methodJson.get('parameters'):
                method.add_param_by_parameter(
                    Parameter(
                        identifier=parameter.get('identifier'),
                        name=parameter.get('name'),
                        type_name=parameter.get('type')
                    )
                )
            for equivClass in methodJson.get('equivClasses'):
                outputJson = equivClass.get('expectedOutputRange')
                outputRange = ParamRange(
                    Parameter('saida_esperada', methodJson.get('returnType')),
                    outputJson.get('v1'),
                    outputJson.get('v2'),
                    outputJson.get('v3')
                )
                print('aqui')
                testSet = TestSet(
                    name=equivClass.get('name'),
                    number_of_cases=equivClass.get('numberOfCases'),
                    expected_range=outputRange,
                    identifier=equivClass.get('identifier'),
                )

                paramRangesJson = equivClass.get('acceptableParamRanges')
                for paramRangeJson in paramRangesJson:
                    param = method.findParamByIdentifier(paramRangeJson.get('param_id'))
                    testSet.add_param_range(
                        ParamRange(
                            param,
                            paramRangeJson.get('v1'),
                            paramRangeJson.get('v2'),
                            paramRangeJson.get('v3')
                        )
                    )
                    method.add_testset(testSet)
            if len(method.testsets) > 0:
                methods.append(method)

        # Process the user story
        for method in methods:
            generator.generate_tests(method, directory)

        #Build response
        return jsonify("Success generating tests"), 200

    except Exception as e:
        # Handle any exceptions (e.g., invalid JSON format)
        error_message = str(e)
        return jsonify({'error': error_message}), 500


@app.route('/api/process_user_story', methods=['POST'])
@cross_origin()
def process_user_story():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        if data is None:
            return jsonify({'error': "Invalid Json format provided."}), 400

        print(data)
        # Extract relevant fields
        lang = data.get('lang')
        user_story = data.get('userStory')

        if lang is None or (lang != 'pt' and lang != 'en'):
            errorMsg = "Invalid body. Please provide the field 'lang' with either the values: 'pt' or 'en'"
            return jsonify({'error': errorMsg}), 400

        if user_story is None or user_story == '':
            errorMsg = "Invalid body. Please provide the fields 'lang' and 'userStory' inside a json body"
            return jsonify({'error': errorMsg}), 400
        print('primeiro')
        # Process the user story
        methods = MethodCatcherService.get(user_story, lang)
        print('aquui')
        methods = get_methods_from_test_cases(methods)

        #Build response
        response_data = []

        for method in methods:
            methodJson = method.toJSON()
            if response_data.count(methodJson) == 0:
                response_data.append(methodJson)

        return jsonify(response_data), 200

    except Exception as e:
        # Handle any exceptions (e.g., invalid JSON format)
        print(e)
        traceback.print_exc()
        error_message = str(e)
        return jsonify({'error': error_message}), 400


if __name__ == '__main__':
    app.run(debug=True)
