# gui.py
import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np

from math_engine import MathEngine
from plotter import Plotter
from history import History

class App:
    """
    Главное приложение Tkinter.
    Объединяет все модули в единый интерфейс.
    """
    
    def __init__(self, master):
        self.master = master
        master.geometry("1000x700")
        master.title("Построитель графиков")
        master.minsize(800, 600)
        
        # Инициализация модулей
        self.math_engine = MathEngine()
        self.history = History()
        
        # Настройка сетки
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_columnconfigure(0, weight=0)
        master.grid_columnconfigure(1, weight=1)
        
        # Создание интерфейса
        self._create_control_panel()
        self._create_graph_area()
        self._create_info_panel()
        
        # Строим график по умолчанию
        self.plot()
    
    def _create_control_panel(self):
        """Создаёт панель управления"""
        control_frame = tk.Frame(self.master, width=250)
        control_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        control_frame.grid_propagate(False)
        
        # Поле ввода функции
        tk.Label(control_frame, text="Введите функцию f(x):", 
                 font=("Arial", 12, "bold")).pack(pady=5)
        
        self.func_entry = tk.Entry(control_frame, font=("Courier", 12))
        self.func_entry.insert(0, "x**2 - 4*x + 3")
        self.func_entry.pack(fill=tk.X, pady=5)
        
        # Диапазон X
        tk.Label(control_frame, text="Диапазон X:", 
                 font=("Arial", 12, "bold")).pack(pady=5)
        
        range_frame = tk.Frame(control_frame)
        range_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(range_frame, text="От:").pack(side=tk.LEFT, padx=5)
        self.start_entry = tk.Entry(range_frame, width=8)
        self.start_entry.insert(0, "-10")
        self.start_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(range_frame, text="До:").pack(side=tk.LEFT, padx=5)
        self.end_entry = tk.Entry(range_frame, width=8)
        self.end_entry.insert(0, "10")
        self.end_entry.pack(side=tk.LEFT, padx=5)
        
        # Точка для вычисления
        tk.Label(control_frame, text="Точка X для вычисления:", 
                 font=("Arial", 12, "bold")).pack(pady=5)
        
        self.x_entry = tk.Entry(control_frame)
        self.x_entry.insert(0, "0")
        self.x_entry.pack(fill=tk.X, pady=5)
        
        # Кнопки
        btn_frame = tk.Frame(control_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Построить", command=self.plot, 
                  bg="lightblue", width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Очистить", command=self.clear, 
                  bg="lightgray", width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Найти корни", command=self.find_roots, 
                  bg="lightgreen", width=10).pack(side=tk.LEFT, padx=2)
        
        tk.Button(control_frame, text="Вычислить f(x)", 
                  command=self.calc_value, bg="lightyellow").pack(fill=tk.X, pady=5)
        
        tk.Button(control_frame, text="Показать историю", 
                  command=self.show_history, bg="lightpink").pack(fill=tk.X, pady=5)
    
    def _create_graph_area(self):
        """Создаёт область для графика"""
        graph_frame = tk.Frame(self.master)
        graph_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        graph_frame.grid_rowconfigure(0, weight=1)
        graph_frame.grid_columnconfigure(0, weight=1)
        
        self.plotter = Plotter(graph_frame)
        self.plotter.widget.grid(row=0, column=0, sticky="nsew")
    
    def _create_info_panel(self):
        """Создаёт информационную панель"""
        info_frame = tk.Frame(self.master, height=80)
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        info_frame.grid_propagate(False)
        
        self.info_label = tk.Label(info_frame, 
            text="Введите функцию и нажмите 'Построить'", 
            font=("Arial", 11))
        self.info_label.pack(pady=5)
        
        self.result_label = tk.Label(info_frame, 
            text="", font=("Courier", 11), fg="blue")
        self.result_label.pack(pady=5)
    
    def plot(self):
        """Строит график функции"""
        try:
            func_str = self.func_entry.get().strip()
            start = float(self.start_entry.get())
            end = float(self.end_entry.get())
            
            if start >= end:
                messagebox.showerror("Ошибка", 
                    "Начало диапазона должно быть меньше конца")
                return
            
            # Проверяем валидность функции
            if not self.math_engine.is_valid_function(func_str):
                messagebox.showerror("Ошибка", 
                    "Некорректная функция. Проверьте синтаксис.")
                return
            
            # Генерируем данные
            x = np.linspace(start, end, 500)
            y = self.math_engine.evaluate_array(func_str, x)
            
            # Строим график
            self.plotter.plot(x, y, title=f"f(x) = {func_str}")
            
            # Обновляем информацию
            self.info_label.config(text=f"График построен: f(x) = {func_str}")
            self.result_label.config(text="")
            
            # Добавляем в историю
            self.history.add(f"Построен график: {func_str}, диапазон [{start}, {end}]")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{str(e)}")
            self.info_label.config(text=f"Ошибка: {str(e)}")
    
    def calc_value(self):
        """Вычисляет значение функции в точке"""
        try:
            func_str = self.func_entry.get().strip()
            x_val = float(self.x_entry.get())
            
            if not self.math_engine.is_valid_function(func_str):
                messagebox.showerror("Ошибка", 
                    "Некорректная функция. Проверьте синтаксис.")
                return
            
            y_val = self.math_engine.evaluate(func_str, x_val)
            
            self.result_label.config(text=f"f({x_val}) = {y_val:.4f}")
            self.history.add(f"Вычислено: f({x_val}) = {y_val:.4f}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось вычислить значение:\n{str(e)}")
    
    def find_roots(self):
        """Находит корни уравнения"""
        try:
            func_str = self.func_entry.get().strip()
            start = float(self.start_entry.get())
            end = float(self.end_entry.get())
            
            if start >= end:
                messagebox.showerror("Ошибка", 
                    "Начало диапазона должно быть меньше конца")
                return
            
            if not self.math_engine.is_valid_function(func_str):
                messagebox.showerror("Ошибка", 
                    "Некорректная функция. Проверьте синтаксис.")
                return
            
            # Находим корни
            roots = self.math_engine.find_roots(func_str, start, end)
            
            if roots:
                # Перестраиваем график с корнями
                x = np.linspace(start, end, 500)
                y = self.math_engine.evaluate_array(func_str, x)
                self.plotter.plot_with_roots(x, y, roots, 
                    title=f"f(x) = {func_str} (корни отмечены красным)")
                
                roots_str = ", ".join([f"x = {r:.4f}" for r in roots])
                self.result_label.config(text=f"Корни: {roots_str}")
                self.history.add(f"Найдены корни: {roots_str}")
                self.info_label.config(text=f"Найдено {len(roots)} корней")
            else:
                self.result_label.config(text="Корней не найдено на заданном интервале")
                self.history.add("Корней не найдено")
                self.info_label.config(text="Корней не найдено")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось найти корни:\n{str(e)}")
    
    def clear(self):
        """Очищает график и информацию"""
        self.plotter.clear()
        self.info_label.config(text="График очищен")
        self.result_label.config(text="")
        self.history.add("График очищен")
    
    def show_history(self):
        """Показывает историю в отдельном окне"""
        history_window = tk.Toplevel(self.master)
        history_window.geometry("500x400")
        history_window.title("История действий")
        
        frame = tk.Frame(history_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Courier", 10))
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scroll = tk.Scrollbar(frame, command=text_widget.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scroll.set)
        
        # Загружаем историю
        text_widget.insert(tk.END, self.history.export_to_text())
        text_widget.config(state=tk.DISABLED)
        
        # Кнопка очистки
        def clear_history():
            self.history.clear()
            text_widget.config(state=tk.NORMAL)
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, "История очищена")
            text_widget.config(state=tk.DISABLED)
        
        tk.Button(history_window, text="Очистить историю", 
                 command=clear_history).pack(pady=5)