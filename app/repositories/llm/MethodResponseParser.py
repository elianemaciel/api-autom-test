import json

from assets.components import Method


def extract_methods_from_result(result_json, language):
    methods = []
    labels = _labels_for(language)

    data = json.loads(_clean_json(result_json))
    if isinstance(data, dict):
        data = data.get("methods") or data.get("metodos") or []

    for method_data in data:
        name = str(method_data.get(labels["method"], "")).strip()
        return_type = str(method_data.get(labels["return_type"], "")).lower().strip()
        class_name = str(method_data.get(labels["class_name"], "")).strip()

        new_method = Method(
            name=name,
            class_name=class_name,
            package_name="",
            output_type=return_type,
            params=[]
        )

        for param in method_data.get(labels["parameters"], []):
            param_name = str(param.get(labels["name"], "")).strip()
            param_type = str(param.get(labels["type"], "")).lower().strip()
            new_method.add_param_by_arg(param_name, param_type)

        new_method.suggested_equivalence_classes = _normalize_equivalence_classes(
            method_data.get(labels["equivalence_classes"], []),
            labels
        )
        methods.append(new_method)

    return methods


def _normalize_equivalence_classes(equivalence_classes, labels):
    normalized = []

    for index, equivalence_class in enumerate(equivalence_classes or []):
        attributes = []
        for attribute in equivalence_class.get(labels["attributes"], []):
            attributes.append({
                "atributo": str(attribute.get(labels["attribute"], "")).strip(),
                "tipo": str(attribute.get(labels["type"], "valid")).strip() or "valid",
                "intervalo": str(attribute.get(labels["range"], "")).strip()
            })

        normalized.append({
            "nome": str(
                equivalence_class.get(labels["name"], f"classe_equivalencia_{index + 1}")
            ).strip(),
            "quantidadeCasos": _positive_int(
                equivalence_class.get(labels["number_of_cases"], 1)
            ),
            "saidaEsperada": str(
                equivalence_class.get(labels["expected_output"], "")
            ).strip(),
            "atributos": attributes
        })

    return normalized


def _positive_int(value):
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return 1


def _clean_json(result_json):
    return result_json.replace("```json", "").replace("```", "").strip()


def _labels_for(language):
    if language == "en":
        return {
            "method": "method",
            "return_type": "returnType",
            "class_name": "className",
            "parameters": "parameters",
            "name": "name",
            "type": "type",
            "equivalence_classes": "equivalenceClasses",
            "number_of_cases": "numberOfCases",
            "expected_output": "expectedOutput",
            "attributes": "attributes",
            "attribute": "attribute",
            "range": "range"
        }

    return {
        "method": "metodo",
        "return_type": "tipoRetorno",
        "class_name": "nomeClasse",
        "parameters": "parametros",
        "name": "nome",
        "type": "tipo",
        "equivalence_classes": "classesEquivalencia",
        "number_of_cases": "quantidadeCasos",
        "expected_output": "saidaEsperada",
        "attributes": "atributos",
        "attribute": "atributo",
        "range": "intervalo"
    }
