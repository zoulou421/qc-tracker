@echo off
echo Starting Odoo and Dash services...
:: Définir les chemins
set ODOO_PATH=C:\Users\EDY\Desktop\qc-dash\qc-tracker\
set ADDONS_PATH=C:\Users\EDY\Desktop\qc-dash\qc-tracker\addons,C:\Users\EDY\Desktop\qc-dash\qc-tracker\qc_addons
set DB_NAME=db-qc
set DASH_PATH=C:\Users\EDY\Desktop\qc-dash\qc-tracker\dash_app\
set NGINX_PATH=C:\Users\EDY\Desktop\qc-dash\qc-tracker\qc_addons\qctracker\setup\nginx-1.27.4
set PYTHON_EXE=C:\Users\EDY\Desktop\qc-dash\venv\Scripts\python.exe
set MODULE_NAME=qctracker
set CONFIG_FILE=%ODOO_PATH%debian\odoo.conf

:: Vérifier que les chemins existent
if not exist "%ODOO_PATH%" (
    echo Le chemin d'Odoo n'existe pas: %ODOO_PATH%
    goto :error
)
if not exist "%DASH_PATH%" (
    echo Le chemin de Dash n'existe pas: %DASH_PATH%
    goto :error
)
if not exist "%NGINX_PATH%" (
    echo Le chemin de Nginx n'existe pas: %NGINX_PATH%
    goto :error
)
if not exist "%PYTHON_EXE%" (
    echo Python du venv introuvable: %PYTHON_EXE%
    goto :error
)
if not exist "%CONFIG_FILE%" (
    echo Fichier de configuration introuvable: %CONFIG_FILE%
    goto :error
)

:: Mise à jour du module Odoo
cd /d %ODOO_PATH%
%PYTHON_EXE% odoo-bin -c debian\odoo.conf -d %DB_NAME% --stop-after-init -u %MODULE_NAME% --log-level=debug
if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors de la mise à jour du module
    goto :error
)

:: Démarrer Odoo avec Python du venv en utilisant uniquement le fichier de configuration
start cmd /k "cd /d %ODOO_PATH% && %PYTHON_EXE% odoo-bin -c debian\odoo.conf"

:: Attendre que Odoo démarre complètement
echo Attente de démarrage d'Odoo...
timeout /t 5 /nobreak > nul

:: Démarrer Dash avec Python du venv avec des variables d'environnement pour la connexion à PostgreSQL
start cmd /k "cd /d %DASH_PATH% && set PGHOST=localhost && set PGPORT=5432 && set PGUSER=openpg && set PGPASSWORD=openpgpwd && set PGDATABASE=db-qc && %PYTHON_EXE% app.py"

:: Démarrer Nginx si ce n'est pas déjà fait
tasklist /FI "IMAGENAME eq nginx.exe" 2>NUL | find /I /N "nginx.exe">NUL
if "%ERRORLEVEL%"=="1" (
    cd /d %NGINX_PATH%
    start nginx.exe
)

echo Services started successfully!
echo Odoo: http://localhost:80
echo Dash: http://localhost:80/dash/
goto :end

:error
echo Une erreur s'est produite lors du démarrage des services.
pause
exit /b 1

:end