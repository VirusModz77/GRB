import os
import subprocess
import sys

# Obtener el directorio donde está guardado este archivo script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Cambiar el directorio de trabajo actual a esa carpeta
os.chdir(directorio_actual)

print(f"Iniciando servidor local en: {directorio_actual}")
print("Abre tu navegador en: http://localhost:8888")
print("Para cerrar el servidor, cierra esta ventana.")

# Ejecutar el comando de Python para levantar el servidor
try:
    subprocess.run([sys.executable, "-m", "http.server", "8888"])
except KeyboardInterrupt:
    print("\nServidor detenido por el usuario.")
