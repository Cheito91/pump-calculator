@echo off
REM Script de inicio rápido para Windows
REM Uso: run.bat

echo ╔══════════════════════════════════════════════════════════╗
echo ║  Sistema de Cálculo de Tuberías y Bombas - Inicio       ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado
    echo Por favor, instale Python 3.8 o superior
    pause
    exit /b 1
)

echo ✓ Python detectado
echo.

REM Verificar dependencias
echo 🔍 Verificando dependencias...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Las dependencias no están instaladas
    echo 📦 Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
    echo ✓ Dependencias instaladas correctamente
) else (
    echo ✓ Dependencias ya instaladas
)

echo.
echo 🚀 Iniciando la aplicación...
echo 📱 La aplicación se abrirá en su navegador en:
echo    http://localhost:8501
echo.
echo ⌨️  Presione Ctrl+C para detener la aplicación
echo.

REM Ejecutar Streamlit
streamlit run app.py
