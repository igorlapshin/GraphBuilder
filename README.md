# GraphBuilder - приложение для построения графиков математических функций
Это учебный проект по созданию desktop-приложения для Windows на основе Python и Tkinter. Все материалы взяты с курса "Python + Tkinter: создание desktop-приложений для Windows". Автор курса: Василий Белай. Описание курса: https://stepik.org/course/297997/info  
## Установка
1.  Клонируйте репозиторий:
    ```bash
    git clone https://github.com/igorlapshin/GtaphBuilder.git
    cd GtaphBuilder
    ```
2.  Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  Установите необходимые библиотеки:
    ```bash
    pip install -r requirements.txt
    ```
4.  Сборка в exe:
    ```pyinstaller --onefile --windowed --name="GraphBuilder" --icon=logarithm.ico --hidden-import=matplotlib.backends.backend_tkagg main.py
    ```
## Использование
### Запуск программы
    Запустите:
    ```bash
    python main.py
    ```
## Структура проекта
-   `main.py`: Точка входа.
-   `gui.py`: Интерфейс (Tkinter).
-   `math_engine.py`: Математическая логика.
-   `plotter.py`:Построение графиков
-   `history.py`: Логирование действий.
-   `requirements.txt`: Список зависимостей.
## Лицензия
Этот проект распространяется под лицензией MIT.
