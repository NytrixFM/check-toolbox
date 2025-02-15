@echo off
echo Vérification de l'installation de Python...

:: Vérifie si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé. Installe-le avant de continuer.
    pause
    exit /b
)

echo Installation des dépendances...
pip install --upgrade pip
pip install setuptools psutil py-cpuinfo GPUtil numpy matplotlib

echo Installation terminée !
pause
