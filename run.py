import hmac
import os
import traceback

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from flask_cors import cross_origin, CORS
from assets.components import get_methods_from_test_cases
from app.services.GenerateTestsService import GenerateTestsService
from app.services.MethodCatcherService import MethodCatcherService
from app.services.EquivalenceClassService import EquivalenceClassService
from flasgger import Swagger

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SWAGGER'] = {
    'title': 'API AutomTest Generator',
    'uiversion': 3
}
swagger = Swagger(app)


def get_configured_api_key():
    return os.getenv('AUTOMTEST_API_KEY') or os.getenv('API_KEY')


def get_request_api_key():
    authorization = request.headers.get('Authorization', '')
    if authorization.lower().startswith('bearer '):
        return authorization[7:].strip()

    return request.headers.get('X-API-Key', '').strip()


@app.before_request
def validate_api_key():
    if request.method == 'OPTIONS' or not request.path.startswith('/api/'):
        return None

    configured_api_key = get_configured_api_key()
    if not configured_api_key:
        return jsonify({'error': 'API key is not configured on the server'}), 503

    request_api_key = get_request_api_key()
    if not request_api_key or not hmac.compare_digest(request_api_key, configured_api_key):
        return jsonify({'error': 'Invalid or missing API key'}), 401

    return None


# Define a route for the API
@app.route('/api/health', methods=['GET'])
@cross_origin()
def health():
    """
    Endpoint Health Check
    ---
    responses:
      200:
        description: Retorna o status de saúde da API
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
    """
    return {"status": "ok"}, 200


@app.route('/api/generate_tests', methods=['POST'])
@cross_origin()
def generate_tests():
    """
    Endpoint Generate Tests - Gera casos de teste com base nas classes de equivalência fornecidas
    ---
    responses:
      200:
        description: Retorna os testes gerados com sucesso
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
    """
    try:
        result, status = GenerateTestsService().generate_tests_archive(request.get_json())
        if status != 200:
            return jsonify(result), status

        response = send_file(
            result.get('buffer'),
            mimetype=result.get('mimetype'),
            as_attachment=True,
            download_name=result.get('download_name')
        )
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    except Exception as e:
        # Handle any exceptions (e.g., invalid JSON format)
        traceback.print_exc()
        error_message = str(e)
        return jsonify({'error': error_message}), 500


@app.route('/api/generate_tests_llm', methods=['POST'])
@cross_origin()
def generate_tests_llm():
    """
    Endpoint Generate Tests LLM - recebe métodos/classes de equivalência e retorna testes em JSON
    ---
    responses:
      200:
        description: Retorna os testes gerados pelo LLM em JSON
    """
    try:
        result, status = GenerateTestsService().generate_tests_with_llm(request.get_json())
        if status != 200:
            return jsonify(result), status

        response = send_file(
            result.get('buffer'),
            mimetype=result.get('mimetype'),
            as_attachment=True,
            download_name=result.get('download_name')
        )
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate_tests_file', methods=['POST'])
@cross_origin()
def generate_tests_file():
    """
    Endpoint legado - gera arquivos Java localmente sem LLM
    ---
    responses:
      200:
        description: Retorna sucesso após salvar os testes gerados em arquivo
    """
    try:
        result, status = GenerateTestsService().generate_tests_file(request.get_json())
        return jsonify(result), status

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/process_user_story', methods=['POST'])
@cross_origin()
def process_user_story():
    """
    Endpoint Process User Story - processa a user story e retorna os métodos identificados
    ---
    responses:
      200:
        description: Retorna os métodos identificados com sucesso
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()

        if data is None:
            return jsonify({'error': "Invalid Json format provided."}), 400

        # Extract relevant fields
        lang = data.get('lang')
        user_story = data.get('userStory')
        selected_ia = data.get('selectedIA')

        if lang is None or (lang != 'pt' and lang != 'en'):
            errorMsg = "Invalid body. Please provide the field 'lang' with either the values: 'pt' or 'en'"
            return jsonify({'error': errorMsg}), 400

        if user_story is None or user_story == '':
            errorMsg = "Invalid body. Please provide the fields 'lang' and 'userStory' inside a json body"
            return jsonify({'error': errorMsg}), 400
        # Process the user story
        methodsService = MethodCatcherService(user_story, lang, selected_ia)
        methods = methodsService.get()
        methods = get_methods_from_test_cases(methods)

        response_data = []

        for method in methods:
            methodJson = method.toJSON()
            if response_data.count(methodJson) == 0:
                response_data.append(methodJson)

        return jsonify(response_data), 200

    except Exception as e:
        # Handle any exceptions (e.g., invalid JSON format)
        traceback.print_exc()
        error_message = str(e)
        return jsonify({'error': error_message}), 400


@app.route('/api/process_class_equivalence', methods=['POST'])
@cross_origin()
def process_class_equivalence():
    try:
        data = request.get_json()

        if data is None:
            return jsonify({'error': "Invalid Json format provided."}), 400

        lang = data.get('lang')
        methods = data.get('methods')
        selected_ia = data.get('selectedIA')

        if lang not in ['pt', 'en']:
            return jsonify({'error': "Field 'lang' must be 'pt' or 'en'"}), 400

        if not methods:
            return jsonify({'error': "Field 'methods' is required"}), 400

        service = EquivalenceClassService(methods, lang, selected_ia)
        result = service.get()

        # Aqui você pode fazer um parser caso queira transformar o JSON retornado pelo LLM em objetos
        return jsonify(result), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
