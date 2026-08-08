# Comandos - Carga KN-Store a Qase

## Linux / macOS

```bash
# 1. Crear entorno virtual
python3 -m venv .venv

# 2. Activar entorno virtual
source .venv/bin/activate

# 3. Instalar dependencia
python3 -m pip install requests

# 4. Verificar acceso y código del proyecto en Qase
curl -s "https://api.qase.io/v1/project" \
	-H "Token: TU_TOKEN" \
	-H "Accept: application/json"

# 5. Variables de entorno
export QASE_API_TOKEN="tu_token"
export QASE_PROJECT_CODE="KNSTORE"

# 6. Ejecutar
python3 qase_import.py
```


## Windows PowerShell

```powershell
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependencia
python -m pip install requests

# 4. Verificar acceso y código del proyecto en Qase
curl.exe -s "https://api.qase.io/v1/project" `
	-H "Token: TU_TOKEN" `
	-H "Accept: application/json"

# 5. Variables de entorno
$env:QASE_API_TOKEN = "tu_token"
$env:QASE_PROJECT_CODE = "KNSTORE"

# 6. Ejecutar
python qase_import.py
```

**Requiere en la misma carpeta:** `qase_import.py`, `kn_store_suites.json`, `kn_store_test_cases.json`

**Errores comunes:**
- `401` → token inválido
- `404` → `QASE_PROJECT_CODE` mal escrito, verifica con el comando del paso 3
- `ModuleNotFoundError` → el entorno virtual no está activado o `requests` no está instalado

### Ejemplo de ingreso en terminal

#### Linux / macOS
```bash
#. esta api es falsa 
export QASE_API_TOKEN="7d62165041bfe11ba4078d7df4872083f83702f46cddf0bdb7ba15b396c"
export QASE_PROJECT_CODE="KNSTORE"
python3 qase_import.py
```

#### Windows PowerShell
```powershell
#. esta api es falsa 
$env:QASE_API_TOKEN = "7d62165041bfe11b6b821a4078d7df483f83702f46cddf0bdb7ba15b396c"
$env:QASE_PROJECT_CODE = "KNSTORE"
python qase_import.py
```