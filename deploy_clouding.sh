#!/bin/bash

# ==============================================================================
# Script de Despliegue Automatizado para Smart Pantry en Clouding.io (Ubuntu)
# Creado por Antigravity para Sharly Andres Mosquera Rodriguez
# ==============================================================================

# Colores para salida elegante
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}      INICIANDO CONFIGURACIÓN DE SMART PANTRY EN TU SERVIDOR CLOUD${NC}"
echo -e "${BLUE}======================================================================${NC}"

# 1. Actualización de paquetes
echo -e "\n${YELLOW}[1/5] Actualizando el sistema operativo...${NC}"
sudo apt update && sudo apt upgrade -y

# 2. Instalación de Nginx
echo -e "\n${YELLOW}[2/5] Instalando el servidor web Nginx...${NC}"
sudo apt install nginx -y

# 3. Creación del directorio para la aplicación
echo -e "\n${YELLOW}[3/5] Creando rutas de almacenamiento de producción...${NC}"
sudo mkdir -p /var/www/smart-pantry/dist
sudo chown -R ubuntu:ubuntu /var/www/smart-pantry

# 4. Creación del archivo de configuración de Nginx
echo -e "\n${YELLOW}[4/5] Creando archivo de configuración en Nginx...${NC}"
cat << 'EOF' | sudo tee /etc/nginx/sites-available/smart-pantry
server {
    listen 80;
    server_name smartpantry.com www.smartpantry.com;

    # Ruta de los archivos web compilados de Smart Pantry
    root /var/www/smart-pantry/dist;
    index index.html;

    # Soporte para rutas de Single Page Application (Expo/React Native)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Optimización con compresión Gzip para redes móviles 3G/4G
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied any;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/x-javascript application/xml application/xml+rss;

    error_page 404 /index.html;
}
EOF

# Habilitar la configuración y remover la por defecto
echo -e "\n${YELLOW}[5/5] Activando la configuración del sitio web...${NC}"
sudo ln -sf /etc/nginx/sites-available/smart-pantry /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Probar la sintaxis y reiniciar Nginx
sudo nginx -t
if [ $? -eq 0 ]; then
    sudo systemctl restart nginx
    echo -e "\n${GREEN}✔ ¡Nginx ha sido configurado con éxito!${NC}"
else
    echo -e "\n${RED}✘ Error en la sintaxis de configuración de Nginx. Por favor revisa nginx.conf.${NC}"
    exit 1
fi

echo -e "\n${BLUE}======================================================================${NC}"
echo -e "${GREEN}🎉 ¡CONFIGURACIÓN INICIAL DE TU SERVIDOR CLOUD COMPLETADA!${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo -e "Próximos pasos recomendados:"
echo -e " 1. Sube tu carpeta '${YELLOW}dist${NC}' a '${YELLOW}/var/www/smart-pantry/dist/${NC}' desde tu PC usando SCP."
echo -e " 2. (Opcional) Activa el certificado SSL (HTTPS) con Let's Encrypt ejecutando:"
echo -e "    ${GREEN}sudo apt install certbot python3-certbot-nginx -y${NC}"
echo -e "    ${GREEN}sudo certbot --nginx -d smartpantry.com -d www.smartpantry.com${NC}"
echo -e "${BLUE}======================================================================${NC}"
