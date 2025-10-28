from pathlib import Path
import sys

# añade la carpeta raíz del proyecto al sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# intenta importar la App principal
try:
    from funcion import App        # funcion.py en la raíz del proyecto
except ModuleNotFoundError:
    # fallback: intentar desde paquete frontend.funcion
    from frontend.funcion import App

if __name__ == "__main__":
    App().mainloop()
