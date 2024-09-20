import subprocess
import sys
import webbrowser
import time
import os

def install_and_run_jupyter():
    try:
        # Проверка, установлен ли Jupyter
        __import__('notebook')
    except ImportError:
        print("Jupyter не установлен. Установка...")
        # Установка Jupyter
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'notebook'])

    # После установки или если уже установлено, запуск Jupyter
    print("Запуск Jupyter Notebook...")
    jupyter_process = subprocess.Popen([sys.executable, '-m', 'notebook'])

    # Ждем немного, чтобы Jupyter запустился и обслужил адрес
    time.sleep(3)

    # Открытие Jupyter Notebook в браузере
    print("Открытие Jupyter Notebook в браузере...")
    webbrowser.open('http://localhost:8888')

    try:
        # Ожидаем, пока браузер закрывается
        while True:
            time.sleep(1)  # Проверяем каждую секунду
            if jupyter_process.poll() is not None:
                break  # Если Jupyter завершился, выходим из цикла

            # Проверяем, открыт ли браузер
            if not is_browser_open():
                print("Браузер закрыт. Закрытие терминала...")
                jupyter_process.terminate()  # Закрываем процесс Jupyter
                sys.exit(0)  # Немедленно завершаем программу и закрываем терминал

    except KeyboardInterrupt:
        print("Завершение работы...")
        jupyter_process.terminate()  # Закрываем процесс Jupyter
        sys.exit(0)  # Немедленно завершаем программу и закрываем терминал

def is_browser_open():
    # Проверка, есть ли запущенные процессы браузера.
    # Подходящие названия процессов для Chrome, Firefox и Edge могут быть изменены по желанию.
    browser_processes = ["chrome.exe", "firefox.exe", "msedge.exe"]
    
    for proc in browser_processes:
        try:
            # Подсчитываем количество процессов с заданными именами
            if len([p for p in os.popen('tasklist') if proc in p]) > 0:
                return True
        except Exception as e:
            print(f"Ошибка при проверке процесса {proc}: {e}")
    return False

if __name__ == "__main__":
    install_and_run_jupyter()