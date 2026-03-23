# Guía de instalación

Resumen rápido de pasos para poner en marcha el backend (Flask) y el frontend (Angular 19). Se sugiere usar Node.js v20.

## Prerrequisitos
- Python (3.8+ recomendado)
- Node.js v20 (recomendado). En Windows se puede usar nvm-windows:
    - Instalar nvm-windows desde su instalador oficial.
    - Luego:
        ```
        nvm install 20
        nvm use 20
        ```

## Backend (Flask)

1. Crear y activar entorno virtual (Windows CMD):
     ```
     python -m venv .venv
     .venv\Scripts\activate
     ```

     PowerShell:
     ```
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```

2. Instalar dependencias:
     ```
     pip install -r requirements.txt
     ```

3. Configurar variables de entorno (ejemplo, ajustar según tu proyecto):
     - CMD:
         ```
         set FLASK_APP=run.py
         set FLASK_ENV=development
         ```
     - PowerShell:
         ```
         $env:FLASK_APP = "run.py"
         $env:FLASK_ENV = "development"
         ```

4. Crear archivo .env a partir de .env.ejemplo y editar valores necesarios:
     - Windows (CMD):
         ```
         copy .env.ejemplo .env
         notepad .env
         ```
     - PowerShell:
         ```
         Copy-Item .env.ejemplo -Destination .env
         notepad .env
         ```
     - macOS/Linux (bash):
         ```
         cp .env.ejemplo .env
         nano .env
         ```
     Edita las variables (base de datos, secret key, etc.) según tu entorno.

5. Migraciones (Flask-Migrate)
     - Inicializar (si no está inicializado):
         ```
         flask db init
         ```
     - Crear migración:
         ```
         flask db migrate -m "Initial migration"
         ```
     - Aplicar migraciones:
         ```
         flask db upgrade
         ```
     - Poblar BD:
         ```
         flask seed-db
         ```

6. Ejecutar la app:
     ```
     flask run --host 0.0.0.0 --port 5000
     ```
     o
     ```
     python -m flask run --host 0.0.0.0 --port 5000
     ```

## Frontend (Angular 19)

1. Cambiar a la carpeta del frontend:
     ```
     cd frontend
     ```

2. Asegurarse de usar Node 20:
     ```
     nvm use 20
     ```

3. Instalar dependencias:
     ```
     npm install
     ```

4. Levantar el servidor de desarrollo:
     - Si hay script en package.json:
         ```
         npm run start
         ```
     - O usar Angular CLI (local):
         ```
         npx ng serve --open
         ```
