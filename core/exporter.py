import os
from utils.dialogs import ask_master_password, show_info

def export_passwords(password_manager, parent):
    master = ask_master_password(parent, "Введите мастер-пароль для экспорта")
    if not master:
        return

    saved = password_manager.load_passwords(master)
    if saved is None:
        show_info(parent, "❌ Неверный мастер-пароль")
        return
    if not saved:
        show_info(parent, "Нет сохранённых паролей")
        return

    try:
        with open("export_passwords.txt", "w", encoding="utf-8") as f:
            f.write("=== Экспорт сохранённых паролей ===\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n")
            for item in saved:
                f.write(f"[{item['date']}] {item['password']}\n")
        show_info(parent, "Экспорт сохранён в export_passwords.txt")
    except Exception as e:
        show_info(parent, f"Ошибка экспорта: {e}")

def clear_all_passwords(password_manager, parent):
    master = ask_master_password(parent, "Подтвердите мастер-пароль")
    if not master:
        return

    confirm = ask_yes_no(parent, "Удалить все пароли?", "Вы уверены, что хотите удалить все сохранённые пароли?")
    if not confirm:
        return

    try:
        if os.path.exists(password_manager.enc_file):
            os.remove(password_manager.enc_file)
        if os.path.exists(password_manager.salt_file):
            os.remove(password_manager.salt_file)
        show_info(parent, "🗑️ Все пароли удалены")
    except Exception as e:
        show_info(parent, f"Ошибка удаления: {e}")
