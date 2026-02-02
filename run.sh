#!/bin/bash

# Script de inicio rápido para la aplicación
# Uso: ./run.sh

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Sistema de Cálculo de Tuberías y Bombas - Inicio       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "Por favor, instale Python 3.8 o superior"
    exit 1
fi

echo "✓ Python 3 detectado: $(python3 --version)"
echo ""

# Verificar si las dependencias están instaladas
echo "🔍 Verificando dependencias..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "⚠️  Las dependencias no están instaladas"
    echo "📦 Instalando dependencias..."
    pip3 install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar dependencias"
        exit 1
    fi
    echo "✓ Dependencias instaladas correctamente"
else
    echo "✓ Dependencias ya instaladas"
fi

echo ""
echo "🚀 Iniciando la aplicación..."
echo "📱 La aplicación se abrirá en su navegador en:"
echo "   http://localhost:8501"
echo ""
echo "⌨️  Presione Ctrl+C para detener la aplicación"
echo ""

# Ejecutar Streamlit
streamlit run app.py
