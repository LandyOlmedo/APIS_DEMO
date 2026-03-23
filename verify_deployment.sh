#!/bin/bash

# Script de verificación local antes de desplegar en Render
# Uso: bash verify_deployment.sh

echo "🔍 Verificando configuración para despliegue en Render..."
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de errores
ERRORS=0

# 1. Verificar requirements.txt
echo -n "✓ Verificando requirements.txt... "
if [ -f "requirements.txt" ]; then
    if grep -q "fastapi" requirements.txt && grep -q "uvicorn" requirements.txt; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}FALTA uvicorn o fastapi${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}NO EXISTE${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 2. Verificar render.yaml
echo -n "✓ Verificando render.yaml... "
if [ -f "render.yaml" ]; then
    if grep -q "apis.contactos.main:app" render.yaml; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}Configuración incorrecta${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}NO EXISTE${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 3. Verificar Procfile
echo -n "✓ Verificando Procfile... "
if [ -f "Procfile" ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}NO EXISTE${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 4. Verificar main.py
echo -n "✓ Verificando main.py... "
if [ -f "apis/contactos/main.py" ]; then
    if grep -q "DB_PATH = os.path.join" apis/contactos/main.py; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}No usa rutas dinámicas${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}NO EXISTE${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 5. Verificar init_db.py
echo -n "✓ Verificando init_db.py... "
if [ -f "apis/contactos/init_db.py" ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}NO EXISTE${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 6. Verificar .gitignore
echo -n "✓ Verificando .gitignore... "
if [ -f ".gitignore" ]; then
    if grep -q "\.env" .gitignore && grep -q "__pycache__" .gitignore; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}Incompleto${NC}"
    fi
else
    echo -e "${RED}NO EXISTE${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 7. Verificar .env.example
echo -n "✓ Verificando .env.example... "
if [ -f ".env.example" ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}NO EXISTE (recomendado)${NC}"
fi

# 8. Verificar DEPLOY_RENDER.md
echo -n "✓ Verificando DEPLOY_RENDER.md... "
if [ -f "DEPLOY_RENDER.md" ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}NO EXISTE (recomendado)${NC}"
fi

echo ""
echo "═══════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ ¡Todo está listo para desplegar en Render!${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "1. Apunta a https://render.com"
    echo "2. Crea un nuevo Web Service"
    echo "3. Conecta tu repositorio de GitHub"
    echo "4. Configura:"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: uvicorn apis.contactos.main:app --host 0.0.0.0 --port \$PORT"
    echo "5. Despliega y espera a que esté Live"
    echo ""
    echo "Para más detalles, ve: DEPLOY_RENDER.md"
else
    echo -e "${RED}❌ Hay $ERRORS error(es) a corregir${NC}"
fi
