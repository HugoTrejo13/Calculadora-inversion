import json
import os
from typing import Optional, Tuple

import requests

from .config import API_URL, TOKEN_FILE

def _token_path() -> str:
    # token.json se guarda en la raíz del proyecto
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(root, TOKEN_FILE)

def save_token(token: str) -> None:
    path = _token_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"access_token": token}, f)

def load_token() -> Optional[str]:
    path = _token_path()
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("access_token")
    except Exception:
        return None

def delete_token() -> None:
    path = _token_path()
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def register_user(email: str, password: str) -> Tuple[bool, str]:
    url = f"{API_URL}/auth/register"
    try:
        r = requests.post(url, json={"email": email, "password": password}, timeout=10)
        if r.status_code == 201:
            return True, r.json().get("message", "Usuario registrado.")
        return False, r.json().get("message", r.text)
    except Exception as exc:
        return False, f"Error de red: {exc}"

def login_user(email: str, password: str) -> Tuple[bool, str]:
    url = f"{API_URL}/auth/login"
    try:
        r = requests.post(url, json={"email": email, "password": password}, timeout=10)
        if r.status_code == 200:
            token = r.json().get("access_token")
            if token:
                save_token(token)
                return True, token
            return False, "Respuesta sin token."
        return False, r.json().get("message", r.text)
    except Exception as exc:
        return False, f"Error de red: {exc}"

def call_protected(token: Optional[str]) -> Tuple[bool, str]:
    if not token:
        return False, "No hay sesión. Inicia sesión primero."
    url = f"{API_URL}/protected"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return True, r.json().get("message", "OK")
        if r.status_code == 401:
            return False, "Sesión inválida o expirada. Vuelve a iniciar sesión."
        return False, r.text
    except Exception as exc:
        return False, f"Error de red: {exc}"
