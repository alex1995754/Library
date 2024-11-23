import os
import subprocess
import sys

# Проверка и установка модулей
required_modules = ['Flask', 'sqlite3']
missing_modules = []

# Проверяем, установлены ли необходимые модули
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    print(f"Отсутствуют следующие модули: {', '.join(missing_modules)}")
    install = input("Хотите установить недостающие модули? (y/n): ").strip().lower()
    if install == 'y':
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_modules])
        print("Модули успешно установлены.")
    else:
        print("Программа завершена.")
        sys.exit(1)

# Запуск сервера app.py
print("Запускаем сервер...")
try:
    subprocess.Popen(['python', 'app.py'])
    print("Сервер успешно запущен!")
except Exception as e:
    print(f"Ошибка при запуске сервера: {e}")
    sys.exit(1)

# Открытие главной страницы в браузере
try:
    if os.name == 'nt':  # Для Windows
        os.startfile("http://127.0.0.1:5000/")
    elif os.name == 'posix':  # Для Linux/macOS
        subprocess.run(['xdg-open', 'http://127.0.0.1:5000/'])
    print("Открываем главную страницу...")
except Exception as e:
    print(f"Не удалось открыть страницу в браузере: {e}")

# Финальное сообщение
print("\nПрограмма завершена. Нажмите Enter, чтобы закрыть окно.")
input()