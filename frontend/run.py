from pathlib import Path
import sys

# Añade la carpeta raíz del proyecto al sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Importa tu app principal
import funcion as app_main  # <-- este es tu funcion.py de siempre

if __name__ == "__main__":
    app_main.App().mainloop()
