"""
Importa a Qase.io los archivos:
  - kn_store_suites.json
  - kn_store_test_cases.json

Uso:
  export QASE_API_TOKEN="tu_token"
  export QASE_PROJECT_CODE="KNS"     # código de tu proyecto en Qase
  python3 qase_import.py

Qué hace:
  1. Crea la jerarquía de suites: KN-Store > (RF/RNF) > Módulo
  2. Crea los test cases (bulk) dentro de cada suite, con severity/priority
     y el código de requerimiento (RF-xxx / RNF-xxx) como tag, para poder
     filtrarlos y vincularlos manualmente a los Requirements desde la UI
     (Properties > Requirements, o el campo custom "requirement_code" si
     lo creas antes en Workspace > Fields).

Nota importante sobre "kn_store_requirements.json":
  No encontré un endpoint público y documentado en developers.qase.io para
  crear Requirements por API en bulk (solo se documenta la creación manual
  vía UI, +Requirement). Si tu plan es Business/Enterprise, revisa en
  developers.qase.io/reference si tu workspace expone /v2/requirement o
  similar; si no, usa kn_store_requirements.json como maestro para copiar/
  pegar o para generar un CSV de importación (Import Data > Requirements,
  si tu instancia lo ofrece).
"""

import json
import os
import sys
import requests

TOKEN = os.environ.get("QASE_API_TOKEN")
PROJECT = os.environ.get("QASE_PROJECT_CODE")
BASE_URL = "https://api.qase.io/v1"

if not TOKEN or not PROJECT:
    sys.exit("Define QASE_API_TOKEN y QASE_PROJECT_CODE como variables de entorno.")

HEADERS = {
    "Token": TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def create_suite(title, parent_id=None):
    payload = {"title": title}
    if parent_id:
        payload["parent_id"] = parent_id
    r = requests.post(f"{BASE_URL}/suite/{PROJECT}", json=payload, headers=HEADERS)
    r.raise_for_status()
    return r.json()["result"]["id"]


def build_suite_tree(suites):
    """suites: lista de {"title": ..., "parent_title": ...} en orden padre->hijo"""
    id_by_title = {}
    for s in suites:
        parent_id = id_by_title.get(s["parent_title"]) if s["parent_title"] else None
        suite_id = create_suite(s["title"], parent_id)
        id_by_title[s["title"]] = suite_id
        print(f'Suite creada: {s["title"]} (id={suite_id})')
    return id_by_title


def bulk_create_cases(cases_payload):
    r = requests.post(f"{BASE_URL}/case/{PROJECT}/bulk", json={"cases": cases_payload}, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def main():
    with open("kn_store_suites.json", encoding="utf-8") as f:
        suites = json.load(f)
    with open("kn_store_test_cases.json", encoding="utf-8") as f:
        test_cases = json.load(f)

    suite_ids = build_suite_tree(suites)

    payload = []
    for tc in test_cases:
        leaf_suite_title = tc["suite_path"][-1]
        suite_id = suite_ids.get(leaf_suite_title)
        payload.append({
            "title": tc["title"],
            "description": tc["description"],
            "preconditions": tc["preconditions"],
            "severity": tc["severity"],
            "priority": tc["priority"],
            "suite_id": suite_id,
            "tags": tc["tags"] + [tc["requirement_code"]],
        })

    # Qase recomienda lotes moderados; aquí se envía en bloques de 50
    for i in range(0, len(payload), 50):
        chunk = payload[i:i + 50]
        result = bulk_create_cases(chunk)
        print(f"Lote {i}-{i+len(chunk)} creado:", result.get("status"))


if __name__ == "__main__":
    main()
