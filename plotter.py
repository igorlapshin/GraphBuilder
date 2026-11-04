# plotter.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Optional, List, Tuple

class Plotter:
    """
    Класс для построения графиков в Tkinter.
    Отвечает за визуализацию данных и отображение результатов.
    """
    
    def __init__(self, master):
        """
        Инициализация построителя графиков.
        
        Args:
            master: Родительский виджет Tkinter
        """
        self.master = master
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.widget = self.canvas.get_tk_widget()
        
        # Настройки по умолчанию
        self.default_style = {
            "line_color": "blue",
            "line_width": 2,
            "grid": True,
            "grid_style": "--",
            "grid_alpha": 0.7
        }
    
    def plot(self, x: np.ndarray, y: np.ndarray, 
             title: str = "График функции",
             xlabel: str = "x",
             ylabel: str = "f(x)",
             color: Optional[str] = None,
             line_width: Optional[int] = None,
             show_grid: Optional[bool] = None,
             show_axes: bool = True) -> None:
        """
        Строит график функции.
        
        Args:
            x: Массив значений x
            y: Массив значений y
            title: Заголовок графика
            xlabel: Подпись оси X
            ylabel: Подпись оси Y
            color: Цвет линии
            line_width: Ширина линии
            show_grid: Показывать сетку
            show_axes: Показывать оси
        """
        # Очищаем предыдущий график
        self.ax.clear()
        
        # Используем настройки по умолчанию или переданные
        color = color or self.default_style["line_color"]
        line_width = line_width or self.default_style["line_width"]
        show_grid = show_grid if show_grid is not None else self.default_style["grid"]
        
        # Строим график
        self.ax.plot(x, y, color=color, linewidth=line_width)
        
        # Настройка осей
        if show_axes:
            self.ax.axhline(y=0, color="black", linewidth=0.5)
            self.ax.axvline(x=0, color="black", linewidth=0.5)
        
        # Настройка сетки
        if show_grid:
            self.ax.grid(
                True, 
                linestyle=self.default_style["grid_style"],
                alpha=self.default_style["grid_alpha"]
            )
        
        # Подписи
        self.ax.set_title(title, fontsize=14)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        
        # Обновляем холст
        self.canvas.draw()
    
    def plot_with_roots(self, x: np.ndarray, y: np.ndarray, 
                        roots: List[float],
                        title: str = "График функции с корнями",
                        **kwargs) -> None:
        """
        Строит график с отмеченными корнями.
        
        Args:
            x: Массив значений x
            y: Массив значений y
            roots: Список корней
            title: Заголовок графика
            **kwargs: Дополнительные параметры для plot()
        """
        # Строим основной график
        self.plot(x, y, title=title, **kwargs)
        
        # Отмечаем корни
        if roots:
            # Находим значения y для корней
            y_roots = [0] * len(roots)
            
            # Рисуем точки корней
            self.ax.scatter(roots, y_roots, color="red", s=60, zorder=5)
            
            # Добавляем подписи для корней
            for root in roots:
                self.ax.annotate(
                    f"x={root:.3f}",
                    (root, 0),
                    xytext=(0, 15),
                    textcoords="offset points",
                    ha="center",
                    fontsize=9,
                    color="red"
                )
            
            self.canvas.draw()
    
    def clear(self) -> None:
        """Очищает график."""
        self.ax.clear()
        self.ax.set_title("График очищен")
        self.canvas.draw()
    
    def save(self, filename: str = "graph.png", dpi: int = 300) -> None:
        """
        Сохраняет график в файл.
        
        Args:
            filename (str): Имя файла
            dpi (int): Разрешение сохранения
        """
        self.fig.savefig(filename, dpi=dpi, bbox_inches="tight")
    
    def set_style(self, **kwargs) -> None:
        """
        Изменяет стиль графика.
        
        Args:
            **kwargs: Параметры стиля (line_color, line_width, grid, grid_style)
        """
        for key, value in kwargs.items():
            if key in self.default_style:
                self.default_style[key] = value
    
    def get_widget(self):
        """
        Возвращает виджет холста для размещения в Tkinter.
        
        Returns:
            tkinter.Widget: Виджет холста
        """
        return self.widget