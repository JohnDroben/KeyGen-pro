import customtkinter as ctk
from datetime import datetime
from core.generator import generate_secure_password, check_password_strength
from core.encryption import PasswordManager
from core.exporter import export_passwords, clear_all_passwords
from utils.dialogs import ask_master_password, show_info

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.password_manager = PasswordManager()

        self.title("Генератор паролей 🔐")
        self.geometry("400x600")
        self.resizable(False, False)

        self.title_label = ctk.CTkLabel(self, text="Генератор паролей", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        self.length_label = ctk.CTkLabel(self, text="Длина: 12", font=ctk.CTkFont(size=14))
        self.length_label.pack(pady=(10, 0))

        self.length_slider = ctk.CTkSlider(self, from_=8, to=32, number_of_steps=24, command=self.update_length_label)
        self.length_slider.set(12)
        self.length_slider.pack(pady=(5, 10), padx=50, fill="x")

        self.upper_var = ctk.BooleanVar(value=True)
        self.lower_var = ctk.BooleanVar(value=True)
        self.digits_var = ctk.BooleanVar(value=True)
        self.symbols_var = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(self, text="Прописные (A-Z)", variable=self.upper_var).pack(pady=5)
        ctk.CTkCheckBox(self, text="Строчные (a-z)", variable=self.lower_var).pack(pady=5)
        ctk.CTkCheckBox(self, text="Цифры (0-9)", variable=self.digits_var).pack(pady=5)
        ctk.CTkCheckBox(self, text="Спецсимволы (!@#$%)", variable=self.symbols_var).pack(pady=5)

        self.generate_button = ctk.CTkButton(self, text="Сгенерировать", command=self.generate_password)
        self.generate_button.pack(pady=(20, 10))

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Пароль", height=40, font=("Consolas", 14))
        self.password_entry.pack(pady=(0, 10), padx=50, fill="x")

        self.strength_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.strength_label.pack(pady=(0, 10))

        self.copy_button = ctk.CTkButton(self, text="Скопировать", command=self.copy_to_clipboard, state="disabled")
        self.copy_button.pack(pady=(0, 10))

        self.save_button = ctk.CTkButton(self, text="Сохранить пароль", command=self.save_password, state="disabled")
        self.save_button.pack(pady=(0, 10))

        self.view_button = ctk.CTkButton(self, text="Просмотреть сохранённые", command=self.view_saved_passwords)
        self.view_button.pack(pady=(0, 10))

        self.export_button = ctk.CTkButton(self, text="Экспорт в .txt", command=self.export_passwords_action)
        self.export_button.pack(pady=(0, 10))

        self.clear_button = ctk.CTkButton(self, text="Удалить все", fg_color="red", command=self.clear_all_action)
        self.clear_button.pack(pady=(0, 10))

        self.feedback_label = ctk.CTkLabel(self, text="", text_color="gray", font=ctk.CTkFont(size=12))
        self.feedback_label.pack(pady=(5, 0))

    def update_length_label(self, value):
        length = int(float(value))
        self.length_label.configure(text=f"Длина: {length}")

    def generate_password(self):
        length = int(self.length_slider.get())
        use_upper = self.upper_var.get()
        use_lower = self.lower_var.get()
        use_digits = self.digits_var.get()
        use_symbols = self.symbols_var.get()

        password = generate_secure_password(length, use_upper, use_lower, use_digits, use_symbols)
        if not password:
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, "Выберите символы!")
            self.copy_button.configure(state="disabled")
            self.save_button.configure(state="disabled")
            return

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)
        self.copy_button.configure(state="normal")
        self.save_button.configure(state="normal")

        strength = check_password_strength(password)
        self.strength_label.configure(text=strength[0], text_color=strength[1])
        self.feedback_label.configure(text="")

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password and "Выберите символы!" not in password:
            import pyperclip
            pyperclip.copy(password)
            self.feedback_label.configure(text="✅ Скопировано")
            self.after(2000, lambda: self.feedback_label.configure(text=""))

    def save_password(self):
        password = self.password_entry.get()
        if not password or "Выберите символы!" in password:
            return

        master = ask_master_password(self, "Введите мастер-пароль")
        if not master:
            return

        if self.password_manager.save_password(password, master):
            self.feedback_label.configure(text="💾 Сохранено (зашифровано)")
            self.after(2000, lambda: self.feedback_label.configure(text=""))
        else:
            self.feedback_label.configure(text="❌ Ошибка сохранения")

    def view_saved_passwords(self):
        master = ask_master_password(self, "Введите мастер-пароль")
        if not master:
            return

        passwords = self.password_manager.load_passwords(master)
        if passwords is None:
            self.feedback_label.configure(text="❌ Неверный мастер-пароль")
            self.after(3000, lambda: self.feedback_label.configure(text=""))
            return

        if not passwords:
            show_info(self, "Нет сохранённых паролей")
            return

        top = ctk.CTkToplevel(self)
        top.title("Сохранённые пароли")
        top.geometry("500x300")
        top.transient(self)
        top.grab_set()

        ctk.CTkLabel(top, text="Сохранённые пароли", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        frame = ctk.CTkScrollableFrame(top, height=200)
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        for item in reversed(passwords):
            label = ctk.CTkLabel(frame, text=f"{item['date']} | {item['password']}", font=("Consolas", 12))
            label.pack(pady=2)

    def export_passwords_action(self):
        export_passwords(self.password_manager, self)

    def clear_all_action(self):
        clear_all_passwords(self.password_manager, self)
