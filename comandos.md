# Carga KN-Store a Qase

El importador se ejecuta directamente desde terminal. El valor de `--project` debe ser el código del proyecto que devuelve Qase en `/v1/project`, no el token.

## Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install requests
curl -s "https://api.qase.io/v1/project" -H "Token: TU_TOKEN" -H "Accept: application/json"
python3 qase_import.py --token "TU_TOKEN" --project "TU_CODIGO_DE_PROYECTO"
```

## Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install requests
curl.exe -s "https://api.qase.io/v1/project" -H "Token: TU_TOKEN" -H "Accept: application/json"
python qase_import.py --token "TU_TOKEN" --project "TU_CODIGO_DE_PROYECTO"
```

Alternativa con variables de entorno:

Linux / macOS:
```bash
export QASE_API_TOKEN="TU_TOKEN"
export QASE_PROJECT_CODE="TU_CODIGO_DE_PROYECTO"
python3 qase_import.py
```

Windows PowerShell:
```powershell
$env:QASE_API_TOKEN = "TU_TOKEN"
$env:QASE_PROJECT_CODE = "TU_CODIGO_DE_PROYECTO"
python qase_import.py
```

**Requiere en la misma carpeta:** `qase_import.py`, `kn_store_suites.json`, `kn_store_test_cases.json`

**Errores comunes:**
- `401` → token inválido
- `404` → el código de proyecto no coincide con el resultado del `curl`
- `ModuleNotFoundError` → `requests` no está instalado o el entorno virtual no está activado