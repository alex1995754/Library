import os
import subprocess
import sys

# Функция для проверки и установки необходимых модулей
def install_missing_modules(required_modules):
    missing_modules = []
    
    for module in required_modules:
        if module == 'sqlite3':
            # sqlite3 не нужно устанавливать, так как это стандартный модуль
            continue

        # Проверяем, установлен ли модуль с помощью pip show
        result = subprocess.run([sys.executable, "-m", "pip", "show", module], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            # Если pip show не находит модуль, то он отсутствует
            missing_modules.append(module)

    if missing_modules:
        print(f"Отсутствуют следующие модули: {', '.join(missing_modules)}")
        install = input("Хотите установить недостающие модули? (y/n): ").strip().lower()
        if install == 'y':
            # Установка недостающих модулей
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_modules])
            print("Модули успешно установлены.")
        else:
            print("Программа завершена.")
            sys.exit(1)

# Список обязательных модулей для работы приложения
required_modules = ['Flask', 'sqlite3']

# Проверяем и устанавливаем недостающие модули
install_missing_modules(required_modules)

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