# Guía de Despliegue: Smart Pantry a Clouding.io con Dominio .com

Esta guía detalla los pasos para alquilar tu servidor virtual en Clouding.io, configurar tu dominio `.com` y desplegar los archivos compilados de la carpeta `dist` usando el servidor Nginx.

---

## Paso 1: Alquilar tu Servidor Virtual en Clouding.io
1. Ingresa a [Clouding.io](https://clouding.io/) y crea una cuenta.
2. Ve al panel de control y haz clic en **"Crear Servidor"**.
3. Selecciona la configuración del servidor:
   *   **Sistema Operativo:** Ubuntu 22.04 LTS (Recomendado y muy estable).
   *   **Recursos:** Con la opción más económica (1 vCPU, 1 GB RAM, 5 GB SSD) es más que suficiente para servir el Catálogo Web de Smart Pantry.
4. Descarga tu clave SSH (archivo `.pem`) y anota la **Dirección IP Pública** de tu nuevo servidor (ej. `185.253.150.12`).

---

## Paso 2: Adquirir tu Dominio `.com` y Configurar las DNS
1. Compra tu dominio `.com` (ej: `smartpantry.com`) en un proveedor registrador de dominios como **Namecheap, GoDaddy o Cloudflare**.
2. Ingresa a la sección de administración de **DNS** de tu dominio y agrega dos registros clave apuntando a la IP pública de tu servidor de Clouding.io:
   *   **Registro A:** Nombre: `@` -> Valor: `IP_DE_TU_SERVIDOR` (ej: `185.253.150.12`)
   *   **Registro A:** Nombre: `www` -> Valor: `IP_DE_TU_SERVIDOR` (ej: `185.253.150.12`)

---

## Paso 3: Instalar Nginx en tu Servidor de Clouding.io
1. Conéctate a tu servidor mediante una terminal (PowerShell o Git Bash) usando SSH:
   ```bash
   ssh -i ruta_a_tu_clave.pem ubuntu@IP_DE_TU_SERVIDOR
   ```
2. Una vez dentro de tu servidor, actualiza los paquetes e instala Nginx:
   ```bash
   sudo apt update
   sudo apt install nginx -y
   ```

---

## Paso 4: Subir los Archivos de Smart Pantry (`dist`) al Servidor
1. En tu computadora local (desde la terminal PowerShell dentro de la carpeta `smart-pantry`), copia la carpeta `dist` compilada a tu servidor usando SCP:
   ```powershell
   scp -r -i ruta_a_tu_clave.pem ./dist ubuntu@IP_DE_TU_SERVIDOR:/home/ubuntu/
   ```
2. En la terminal de tu servidor de Clouding, mueve la carpeta `dist` al directorio de producción `/var/www/smart-pantry/`:
   ```bash
   sudo mkdir -p /var/www/smart-pantry
   sudo mv /home/ubuntu/dist /var/www/smart-pantry/
   sudo chown -R www-data:www-data /var/www/smart-pantry
   ```

---

## Paso 5: Configurar Nginx con el Archivo `nginx.conf`
1. Sube el archivo `nginx.conf` de configuración que te preparé a tu servidor, o edítalo directamente en él:
   ```bash
   sudo nano /etc/nginx/sites-available/smart-pantry
   ```
2. Pega el contenido de tu archivo local `nginx.conf`. Asegúrate de que `server_name` tenga tu dominio comprado (ej: `smartpantry.com`).
3. Activa la configuración creando un enlace simbólico y reinicia Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/smart-pantry /etc/nginx/sites-enabled/
   sudo rm /etc/nginx/sites-enabled/default # Remueve la pantalla de bienvenida por defecto
   sudo nginx -t # Valida que la sintaxis sea correcta
   sudo systemctl restart nginx
   ```

---

## Paso 6 (Opcional): Instalar SSL Gratuito (HTTPS) con Let's Encrypt
Para que tu sitio web tenga el candado verde de seguridad (`https://`):
1. Ejecuta los siguientes comandos en tu servidor:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d smartpantry.com -d www.smartpantry.com
   ```
2. Sigue las instrucciones breves en pantalla. Certbot reconfigurará Nginx automáticamente para que tu dominio `.com` sea 100% seguro.

¡Felicidades! Tu aplicación Smart Pantry estará en vivo y en directo bajo tu propio servidor virtual y dominio `.com`!
