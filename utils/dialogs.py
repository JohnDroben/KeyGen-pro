import customtkinter as ctk
from datetime import datetime

def ask_master_password(parent, title):
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.geometry("300x150")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()

    ctk.CTkLabel(dialog, text="Мастер-пароль:", font=("Arial", 12)).pack(pady=(20, 5))
    entry = ctk.CTkEntry(dialog, show="*", width=200)
    entry.pack(pady=5)

    result = {"value": None}

    def on_ok():
        result["value"] = entry.get()
        dialog.destroy()

    def on_cancel():
        dialog.destroy()

    btn_frame = ctk.CTkFrame(dialog)
    btn_frame.pack(pady=10)
    ctk.CTkButton(btn_frame, text="OK", width=60, command=on_ok).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Отмена", width=60, command=on_cancel).pack(side="left", padx=5)

    parent.wait_window(dialog)
    return result["value"]

def ask_yes_no(parent, title, message):
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.geometry("300x120")
    dialog.transient(parent)
    dialog.grab_set()

    ctk.CTkLabel(dialog, text=message, font=("Arial", 12)).pack(pady=20)
    btn_frame = ctk.CTkFrame(dialog)
    btn_frame.pack()

    result = {"value": False}

    def on_yes():
        result["value"] = True
        dialog.destroy()

    def on_no():
        dialog.destroy()

    ctk.CTkButton(btn_frame, text="Да", fg_color="red", width=60, command=on_yes).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Нет", width=60, command=on_no).pack(side="left", padx=10)

    parent.wait_window(dialog)
    return result["value"]

def show_info(parent, message):
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Информация")
    dialog.geometry("300x100")
    dialog.transient(parent)
    dialog.grab_set()

    ctk.CTkLabel(dialog, text=message, wraplength=250).pack(pady=20)
    ctk.CTkButton(dialog, text="ОК", command=dialog.destroy).pack()
