import tkinter as tk
from tkinter import messagebox, ttk

from .auth_client import (
    register_user, login_user, load_token, call_protected, delete_token, save_token
)

class AuthDialog(tk.Toplevel):
    def __init__(self, master: tk.Misc, mode: str = "login"):
        super().__init__(master)
        self.title("Cuenta")
        self.resizable(False, False)
        self.mode = mode  # "login" o "register"
        self.email_var = tk.StringVar()
        self.pass_var = tk.StringVar()
        self.pass2_var = tk.StringVar()

        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Email").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.email_var, width=32).grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(frm, text="Contraseña").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.pass_var, show="•", width=32).grid(row=1, column=1, sticky="ew", pady=4)

        if self.mode == "register":
            ttk.Label(frm, text="Repetir contraseña").grid(row=2, column=0, sticky="w", pady=4)
            ttk.Entry(frm, textvariable=self.pass2_var, show="•", width=32).grid(row=2, column=1, sticky="ew", pady=4)

        btn_text = "Registrarse" if self.mode == "register" else "Iniciar sesión"
        ttk.Button(frm, text=btn_text, command=self._submit).grid(row=99, column=0, columnspan=2, pady=8, sticky="ew")

        self.bind("<Return>", lambda _e: self._submit())
        self.grab_set()
        self.email_var.set("")
        self.pass_var.set("")
        self.pass2_var.set("")
        self._center(master)

    def _center(self, master):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = master.winfo_rootx() + (master.winfo_width() - w)//2
        y = master.winfo_rooty() + (master.winfo_height() - h)//3
        self.geometry(f"+{x}+{y}")

    def _submit(self):
        email = self.email_var.get().strip()
        pwd = self.pass_var.get()
        if not email or not pwd:
            messagebox.showwarning("Cuenta", "Completa email y contraseña.")
            return

        if self.mode == "register":
            if pwd != self.pass2_var.get():
                messagebox.showerror("Cuenta", "Las contraseñas no coinciden.")
                return
            ok, msg = register_user(email, pwd)
            if ok:
                messagebox.showinfo("Cuenta", msg)
                self.destroy()
            else:
                messagebox.showerror("Cuenta", msg)
            return

        # login
        ok, token_or_msg = login_user(email, pwd)
        if ok:
            messagebox.showinfo("Cuenta", "Inicio de sesión correcto.")
            # token ya se guardó en token.json dentro de login_user; por si acaso:
            save_token(token_or_msg)
            self.destroy()
        else:
            messagebox.showerror("Cuenta", token_or_msg)

def probe_protected(master: tk.Misc):
    from .auth_client import load_token
    token = load_token()
    ok, msg = call_protected(token)
    if ok:
        messagebox.showinfo("Protegido", msg)
    else:
        messagebox.showwarning("Protegido", msg)
