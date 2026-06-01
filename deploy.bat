@echo off
title Despliegue de Smart Pantry a Internet
color 0b
echo ==========================================================
echo   DESPLIEGUE AUTOMATICO DE SMART PANTRY A INTERNET
echo ==========================================================
echo.
echo  Paso 1: Iniciando sesion en tu cuenta de Firebase...
echo  (Se abrira una ventana en tu navegador de Chrome para iniciar sesion)
echo.
call npx firebase login
echo.
echo  Paso 2: Subiendo tu aplicacion a Firebase Hosting...
echo  (Subiendo archivos compilados de la carpeta dist)
echo.
call npx firebase deploy
echo.
echo ==========================================================
echo   APLICACION EN VIVO Y EN DIRECTO!
echo.
echo   Tu sitio web ya esta en vivo en internet:
echo   https://smart-pantry-e60df.web.app
echo ==========================================================
echo.
pause
