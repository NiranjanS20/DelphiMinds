param(
  [switch]$ml
)

if(!(Test-Path .venv)){ python -m venv .venv }
.\.venv\Scripts\python -m pip install --upgrade pip | Out-Null
.\.venv\Scripts\python -m pip install -r requirements.base.txt | Out-Null
if($ml){ .\.venv\Scripts\python -m pip install -r requirements.ml.txt | Out-Null }
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py runserver


