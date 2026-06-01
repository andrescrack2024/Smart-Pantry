# Guía de Despliegue Gratis: Smart Pantry a Render.com con Dominio .com

Esta guía detalla los dos métodos más fáciles y rápidos para subir tu aplicación web recopilada en la carpeta `dist` a la nube de **Render** de forma 100% gratuita.

---

## Método A: Arrastrar y Soltar (El más rápido e instantáneo - 1 minuto)
Si no quieres usar Git o GitHub en este momento, puedes subir tu carpeta `dist` arrastrándola con el ratón:

1.  Abre tu navegador y entra a **[dashboard.render.com](https://dashboard.render.com/)** (inicia sesión con tu cuenta de GitHub, Google o correo electrónico).
2.  Haz clic en el botón azul **"New +"** (Nuevo) en la esquina superior derecha y selecciona **"Static Site"** (Sitio Estático).
3.  En la parte inferior de la pantalla de selección de repositorio, verás un recuadro que dice:
    *   **"Quickly deploy a pre-built static site... Drag and drop a folder here"**
4.  Abre el Explorador de archivos de Windows en la carpeta de tu proyecto:  
    👉 `C:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry`
5.  **Arrastra la carpeta llamada `dist`** y suéltala directamente en esa caja del navegador en Render.
6.  Asigna un nombre a tu proyecto (ej: `smart-pantry-fucla`) y haz clic en **"Deploy"**.
7.  ¡Listo! Render subirá tus archivos y en menos de 20 segundos tu aplicación estará activa en internet en una URL gratuita como:  
    👉 `https://smart-pantry-fucla.onrender.com`

---

## Método B: Conectar con GitHub (Sincronización Automática - Recomendado)
Si tienes el proyecto subido en un repositorio de GitHub:

1.  Entra a **[dashboard.render.com](https://dashboard.render.com/)** y haz clic en **"New +" > "Static Site"**.
2.  Conecta tu cuenta de GitHub y selecciona el repositorio de `smart-pantry`.
3.  Configura las siguientes opciones en el formulario:
    *   **Name:** `smart-pantry-fucla`
    *   **Build Command:** `npm run web` (o déjalo en blanco si ya tienes la carpeta `dist` en tu repositorio).
    *   **Publish Directory:** `dist` (muy importante: esto le dice a Render que sirva los archivos compilados).
4.  Haz clic en **"Create Static Site"**.
5.  ¡Listo! Cada vez que hagas un cambio en tu repositorio de GitHub, Render actualizará tu sitio web en vivo automáticamente.

---

## Paso C: Vincular tu Dominio `.com` en Render de forma Gratuita
Una vez que tu sitio esté desplegado en Render:

1.  En el panel lateral izquierdo de tu proyecto en Render, ve a **"Settings"** (Configuración).
2.  Busca la sección **"Custom Domains"** (Dominios Personalizados) y haz clic en **"Add Custom Domain"**.
3.  Escribe tu dominio comprado (ej: `smartpantry.com`) y haz clic en **"Save"**.
4.  Render te indicará que agregues dos sencillos registros DNS en tu registrador de dominio (Namecheap, GoDaddy, etc.):
    *   **Un registro CNAME** para `www.smartpantry.com` apuntando a tu subdominio de Render (ej. `smart-pantry-fucla.onrender.com`).
    *   **Un registro ANAME / ALIAS** para tu dominio raíz `smartpantry.com` apuntando a las IPs que Render te mostrará en pantalla.
5.  Render validará la conexión y generará automáticamente un certificado de seguridad SSL gratuito para que tu sitio sea seguro con **`https://smartpantry.com`**.
