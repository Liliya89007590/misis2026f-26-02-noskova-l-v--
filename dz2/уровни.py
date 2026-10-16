
class StringProcessor:
    "Класс для обработки строк с различными методами"
    
    
    def level_1(text: str, method: int) -> str:
        "Уровень 1: Базовые преобразования регистра"
        if method == 1:
            return text.upper()
        elif method == 2:
            return text.lower()
        elif method == 3:
            return text.capitalize()
        else:
            return "Неверный метод"
    
   
    def level_2(text: str, method: int, x: str = "", y: str = "") -> Union[int, str, None]:
        "Уровень 2: Поиск и замена в строках"
        if method == 1:
            return text.find(x)
        elif method == 2:
            return text.replace(x, y)
        elif method == 3:
            return text.count(x)
        else:
            return None
    
    
    def level_3(text: str, method: int, separator: str = "") -> Union[List[str], str, None]:
        "Уровень 3: Разделение и объединение строк"
        if method == 1:
            return text.split(separator) if separator else text.split()
        elif method == 2:
            return separator.join(text.split())
        else:
            return None
    
    
    def level_4(text: str, method: int) -> Union[bool, str, None]:
        "Уровень 4: Проверка и очистка строк"
        if method == 1:
            return text.isdigit()
        elif method == 2:
            return text.isalpha()
        elif method == 3:
            return text.strip()
        elif method == 4:
            return text.lstrip()  
        elif method == 5:
            return text.rstrip()
        else:
            return None
    
    
    def level_5(text: str) -> str:
        "Уровень 5: Комплексное преобразование строки"
        
        text = text.strip().capitalize()
        
        text = text.replace('-', ' ')
        text = text.replace('+', ' ')
        
        words = text.split()
        return ' '.join(words)


