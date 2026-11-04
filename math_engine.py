# math_engine.py
import numpy as np

class MathEngine:
    """
    Класс для математических вычислений.
    Отвечает за вычисление функций, поиск корней и валидацию.
    """
    
    def __init__(self):
        # Доступные функции для eval (безопасный набор)
        self.functions = {
            "np": np,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "log": np.log,
            "log10": np.log10,
            "sqrt": np.sqrt,
            "abs": np.abs,
            "pi": np.pi,
            "e": np.e
        }
        
        # Список разрешённых операций
        self.allowed_ops = ["+", "-", "*", "/", "**", "(", ")"]
    
    def evaluate(self, func_str, x):
        """
        Вычисляет значение функции в точке x.
        
        Args:
            func_str (str): Строка с функцией (например, "x**2 + 2")
            x (float): Значение x
            
        Returns:
            float: Значение функции в точке x
            
        Raises:
            ValueError: Если функция некорректна или вычисление невозможно
        """
        try:
            # Проверяем безопасность выражения
            self._validate_expression(func_str)
            
            # Вычисляем
            result = eval(func_str, {"x": x, **self.functions})
            
            # Проверяем, что результат — число
            if not isinstance(result, (int, float, np.number)):
                raise ValueError("Результат должен быть числом")
            
            return float(result)
            
        except ZeroDivisionError:
            raise ValueError("Деление на ноль")
        except Exception as e:
            raise ValueError(f"Ошибка вычисления: {str(e)}")
    
    def evaluate_array(self, func_str, x_array):
        """
        Вычисляет функцию для массива значений.
        
        Args:
            func_str (str): Строка с функцией
            x_array (numpy.ndarray): Массив значений x
            
        Returns:
            numpy.ndarray: Массив значений функции
        """
        try:
            self._validate_expression(func_str)
            result = eval(func_str, {"x": x_array, **self.functions})
            return np.array(result, dtype=float)
        except Exception as e:
            raise ValueError(f"Ошибка вычисления массива: {str(e)}")
    
    def find_roots(self, func_str, start, end, num_points=10000):
        """
        Находит корни уравнения f(x) = 0 на интервале [start, end].
        
        Args:
            func_str (str): Строка с функцией
            start (float): Начало интервала
            end (float): Конец интервала
            num_points (int): Количество точек для поиска
            
        Returns:
            list: Список корней (уникальные, отсортированные)
        """
        if start >= end:
            raise ValueError("Начало интервала должно быть меньше конца")
        
        # Генерируем точки
        x = np.linspace(start, end, num_points)
        y = self.evaluate_array(func_str, x)
        
        roots = []
        
        # Ищем пересечения с осью X
        for i in range(len(y) - 1):
            # Проверяем смену знака
            if y[i] * y[i+1] < 0:
                # Линейная интерполяция для уточнения корня
                x_root = x[i] - y[i] * (x[i+1] - x[i]) / (y[i+1] - y[i])
                roots.append(x_root)
            elif abs(y[i]) < 1e-10:
                # Точное попадание в ноль
                roots.append(x[i])
        
        # Убираем дубликаты и сортируем
        if roots:
            roots = sorted(set([round(r, 6) for r in roots]))
        
        return roots
    
    def _validate_expression(self, expr):
        """
        Проверяет выражение на безопасность.
        
        Args:
            expr (str): Строка с выражением
            
        Raises:
            ValueError: Если выражение содержит неразрешённые символы
        """
        # Проверяем наличие запрещённых символов
        allowed_chars = set(
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            "+-*/()., "
        )
        
        # Разрешаем названия функций
        func_names = set(self.functions.keys())
        
        for char in expr:
            if char not in allowed_chars and char not in " ".join(func_names):
                raise ValueError(f"Недопустимый символ: '{char}'")
        
        # Проверяем, что выражение содержит x
        if "x" not in expr:
            raise ValueError("Выражение должно содержать переменную x")
        
        return True
    
    def is_valid_function(self, func_str):
        """
        Проверяет, является ли строка корректной функцией.
        
        Args:
            func_str (str): Строка с функцией
            
        Returns:
            bool: True если функция корректна
        """
        try:
            self.evaluate(func_str, 0)
            return True
        except:
            return False