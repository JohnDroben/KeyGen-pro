"""
Точка входа в приложение "Генератор паролей"
Запускает графический интерфейс.
"""

import os
import sys

# Добавляем корень проекта в sys.path, чтобы импорты работали правильно
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        from gui.app import PasswordGeneratorApp
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("Убедитесь, что структура проекта правильная и все файлы на месте.")
        sys.exit(1)

    app = PasswordGeneratorApp()
    app.mainloop()

if __name__ == "__main__":
    main()
