@echo off
title Stop FoodExpress Servers
echo Stopping FoodExpress servers...
taskkill /FI "WINDOWTITLE eq FoodExpress - Backend :8000" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq FoodExpress - Frontend :3000" /F >nul 2>&1
echo Done! Both servers stopped.
pause
