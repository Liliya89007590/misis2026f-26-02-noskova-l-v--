#списки изменяются
#массивы не изменяются


#1) собирать предметы (append, extend)
#2) выбрасывать предметы (remove, pop)
#3) сортировать (sort,reverse)
#4) искать ключевые элементы(index, in)
#5) копировать и модифицировать (copy, siice)
#6) lise comp для генерации данных
#комнаты: пусто, сундук, монстр, ловушки(урон), ключ, порталы
#пользователь: здоровье hp = 100, инвентарь, (x, y) смена положение
#инвентарь: добавить, удалить, изменение свойств предмета

# x for x in iter
# x(результат (кружок))for x in iter(по чему бегаете(прямоугольник))пустота(фильтр(треугольник))
#s = [ (x ** 2) (for x in varge(10)) (if x != 5 and x % 2 == 0)]
#a = [-2, -1, 0, 1, 2]
#b = [(x**3 if x<0)( else x ** 2) (for x in a) (if x%2 =0)]
# если фильтр выполнится то мы попадем в результат
# начать с лабиринта


import random
from typing import List, Dict, Any, Optional

class ListMazeGame:
    "Игра 'Лабиринт Списков' - обучение работе со списками Python"
    
    def __init__(self):
        self.rooms = ["пусто", "сундук", "монстр", "ключ", "ловушка", "портал"]
        self.inventory: List[str] = []
        self.health = 100
        self.has_key = False
        self.visited_rooms: List[str] = []
        self.maze_size = (6, 6)
        self.player_pos = (0, 0)
        self.maze: List[List[Dict[str, Any]]] = []
        self.exit_pos = (5, 5)
        
    def generate_maze(self) -> None:
        "Генерация лабиринта со случайными комнатами"
        n, m = self.maze_size
        self.maze = []
        
        for i in range(n):
            row = []
            for j in range(m):
                room_type = random.choice(self.rooms)
                room = {
                    "type": room_type,
                    "visited": False,
                    "items": self._generate_room_items(room_type),
                    "description": self._get_room_description(room_type)
                }
                row.append(room)
            self.maze.append(row)
        
        # Стартовая позиция и выход
        self.maze[0][0]["type"] = "старт"
        self.maze[0][0]["visited"] = True
        self.maze[5][5]["type"] = "выход"
        self.visited_rooms.append("старт")
        
    def _generate_room_items(self, room_type: str) -> List[str]:
        "Генерация предметов в комнате в зависимости от типа"
        items_lists = {
            "сундук": [["золото", "серебро", "изумруд"], ["свиток", "карта", "ключ"]],
            "монстр": [["меч", "щит", "лук"], ["зелье", "броня"]],
            "ключ": [["ключ"], ["малый ключ", "большой ключ"]],
            "ловушка": [["капкан", "шипы"], ["яд", "газовая ловушка"]],
            "пусто": [[], ["камень", "ветка"]],
            "портал": [["магический кристалл"], ["древний артефакт"]]
        }
        if room_type in items_lists:
            possible_items = random.choice(items_lists[room_type])
            return possible_items[:random.randint(0, len(possible_items))]
        return []
    def _get_room_description(self, room_type: str) -> str:
        "Описание комнаты"
        descriptions = {
            "пусто": "Пустая комната. Ничего интересного.",
            "сундук": "Комната с сундуком! Возможно, внутри что-то есть.",
            "монстр": "Опасная комната! Здесь может быть монстр.",
            "ключ": "Комната с ключом! Это может помочь с выходом.",
            "ловушка": "Осторожно! Здесь могут быть ловушки.",
            "портал": "Магическая комната с порталом.",
            "старт": "Начальная точка вашего приключения.",
            "выход": "ВЫХОД ИЗ ЛАБИРИНТА! Но нужен ключ..."
        }
        return descriptions.get(room_type, "Неизвестная комната")
    def display_maze(self) -> None:
        "Отображение лабиринта"
        n, m = self.maze_size
        print("\n" + "="*50)
        print("ЛАБИРИНТ СПИСКОВ")
        print("="*50)
        for i in range(n):
            row = ""
            for j in range(m):
                if (i, j) == self.player_pos:
                    row += "🧍 "
                elif self.maze[i][j]["visited"]:
                    room_types = {
                        "пусто": "⬜", "сундук": "📦", "монстр": "👹", 
                        "ключ": "🔑", "ловушка": "⚠️ ", "портал": "🌀",
                        "выход": "🚪", "старт": "🏁"
                    }
                    row += room_types.get(self.maze[i][j]["type"], "? ") + " "
                else:
                    row += "❓ "
            print(row)
    def show_status(self) -> None:
        "Показать статус игрока"
        print(f"\n--- СТАТУС ---")
        print(f"Здоровье: {self.health}")
        print(f"Ключ: {'ЕСТЬ' if self.has_key else 'НЕТ'}")
        print(f"Инвентарь: {self.inventory}")
        print(f"Посещенные комнаты: {len(self.visited_rooms)}")
    def handle_room_event(self) -> None:
        "Обработка событий в текущей комнате"
        x, y = self.player_pos
        room = self.maze[x][y]
        
        if not room["visited"]:
            room["visited"] = True
            self.visited_rooms.append(room["type"])
            print(f"\n>>> {room['description']} <<<")
            
            # Обработка специфических событий комнаты
            if room["type"] == "монстр":
                self._fight_monster()
            elif room["type"] == "ловушка":
                self._trigger_trap()
            elif room["type"] == "портал":
                self._teleport()
            elif room["type"] == "выход":
                self._try_escape()
            
            # Сбор предметов из комнаты
            if room["items"]:
                print(f"Найдены предметы: {room['items']}")
                self._collect_items(room["items"])
                room["items"] = []
        else:
            print(f"\nВы уже были в этой комнате: {room['description']}")
    
    def _fight_monster(self) -> None:
        "Бой с монстром с использованием методов списков"
        monster_hp = random.randint(20, 50)
        print(f"На вас напал монстр с {monster_hp} HP!")
        
        # Используем методы списков для атаки
        attacks = ["удар", "выстрел", "заклинание"] * 3  # extend и умножение
        print(f"Доступные атаки: {attacks}")
        
        # Используем list comprehension для генерации урона
        damage_options = [random.randint(5, 15) for _ in range(3)]  # list comprehension
        print(f"Возможный урон: {damage_options}")
        
        while monster_hp > 0 and self.health > 0:
            print(f"\nМонстр HP: {monster_hp}, Ваше HP: {self.health}")
            action = input("Выберите действие (атака/инвентарь/бег): ").lower()
            
            if action == "атака":
                # Используем pop() для выбора атаки
                if attacks:
                    current_attack = attacks.pop()
                    damage = damage_options.pop() if damage_options else 10
                    monster_hp -= damage
                    print(f"Вы используете {current_attack} и наносите {damage} урона!")
                else:
                    print("Атаки закончились!")
                    break
            elif action == "инвентарь":
                self._use_inventory_in_combat()
            elif action == "бег":
                if random.random() < 0.5:
                    print("Вы успешно сбежали!")
                    return
                else:
                    print("Не удалось сбежать!")
            
            # Контратака монстра
            if monster_hp > 0:
                monster_damage = random.randint(5, 15)
                self.health -= monster_damage
                print(f"Монстр атакует и наносит {monster_damage} урона!")
        
        if monster_hp <= 0:
            print("Монстр побежден!")
            reward = ["золото", "опыт", "зелье здоровья"]
            print(f"Получено: {reward}")
            self.inventory.extend(reward)  # extend для добавления награды
    
    def _trigger_trap(self) -> None:
        "Активация ловушки"
        trap_damage = random.randint(10, 25)
        print(f"Активирована ловушка! Потеряно {trap_damage} HP")
        self.health -= trap_damage
        
        # Проверяем наличие защиты в инвентаре
        if "щит" in self.inventory:  # оператор in для поиска
            reduction = trap_damage // 2
            self.health += reduction
            print(f"Щит поглотил {reduction} урона!")
    
    def _teleport(self) -> None:
        "Телепортация в случайную комнату"
        print("Портал телепортирует вас в случайную комнату!")
        new_x = random.randint(0, self.maze_size[0] - 1)
        new_y = random.randint(0, self.maze_size[1] - 1)
        self.player_pos = (new_x, new_y)
    
    def _try_escape(self) -> None:
        "Попытка выйти из лабиринта"
        if self.has_key:
            print("ПОЗДРАВЛЯЮ! Вы использовали ключ и вышли из лабиринта!")
            return True
        else:
            print("Выход заперт. Нужен ключ!")
            return False
    
    def _collect_items(self, items: List[str]) -> None:
        "Сбор предметов из комнаты"
        if items:
            action = input("Собрать предметы? (да/нет): ").lower()
            if action == "да":
                # append для добавления по одному или extend для нескольких
                if len(items) == 1:
                    self.inventory.append(items[0])  # append
                    print(f"Добавлен: {items[0]}")
                else:
                    self.inventory.extend(items)  # extend
                    print(f"Добавлены: {items}")
                
                # Проверяем, не подобрали ли ключ
                if any("ключ" in item for item in items):
                    self.has_key = True
                    print(">>> Вы нашли КЛЮЧ! Теперь можно открыть выход! <<<")
    
    def _use_inventory_in_combat(self) -> None:
        "Использование инвентаря в бою"
        if not self.inventory:
            print("Инвентарь пуст!")
            return
        
        print(f"Инвентарь: {self.inventory}")
        item = input("Выберите предмет для использования: ")
        
        if item in self.inventory:  # оператор in для проверки
            if item == "зелье здоровья":
                heal = 30
                self.health += heal
                self.inventory.remove(item)  # remove для удаления
                print(f"Использовано зелье здоровья! +{heal} HP")
            elif item == "меч":
                print("Меч уже экипирован!")
            else:
                print(f"Предмет {item} нельзя использовать в бою")
        else:
            print("Предмет не найден в инвентаре!")
    
    def manage_inventory(self) -> None:
        "Управление инвентарем с использованием методов списков"
        if not self.inventory:
            print("Инвентарь пуст!")
            return
        
        print(f"\n--- УПРАВЛЕНИЕ ИНВЕНТАРЕМ ---")
        print(f"Текущий инвентарь: {self.inventory}")
        
        while True:
            print("\nДоступные действия:")
            print("1 - Просмотреть инвентарь")
            print("2 - Отсортировать инвентарь")
            print("3 - Выбросить предмет")
            print("4 - Найти предмет")
            print("5 - Копировать инвентарь")
            print("6 - Очистить инвентарь")
            print("0 - Назад")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                # Простой просмотр
                print(f"Инвентарь: {self.inventory}")
                
            elif choice == "2":
                # Сортировка
                print("Сортировка...")
                self.inventory.sort()  # sort
                print(f"Отсортированный инвентарь: {self.inventory}")
                
                # reverse
                reverse_choice = input("Развернуть порядок? (да/нет): ")
                if reverse_choice.lower() == "да":
                    self.inventory.reverse()
                    print(f"Развернутый инвентарь: {self.inventory}")
                    
            elif choice == "3":
                # Удаление предметов
                print(f"Инвентарь: {self.inventory}")
                remove_choice = input("Удалить по (1-имени / 2-индексу): ")
                
                if remove_choice == "1":
                    item = input("Введите название предмета: ")
                    if item in self.inventory:
                        self.inventory.remove(item)  # remove по значению
                        print(f"Удален: {item}")
                    else:
                        print("Предмет не найден!")
                elif remove_choice == "2":
                    try:
                        index = int(input(f"Введите индекс (0-{len(self.inventory)-1}): "))
                        removed = self.inventory.pop(index)  # pop по индексу
                        print(f"Удален: {removed}")
                    except (ValueError, IndexError):
                        print("Неверный индекс!")
                        
            elif choice == "4":
                # Поиск предметов
                search_term = input("Введите название для поиска: ")
                
                # Используем in и index
                if search_term in self.inventory:
                    index = self.inventory.index(search_term)  # index
                    print(f"Предмет '{search_term}' найден на позиции {index}")
                else:
                    print("Предмет не найден")
                    
                # List comprehension для поиска всех совпадений
                matches = [item for item in self.inventory if search_term.lower() in item.lower()]
                if matches:
                    print(f"Найдены совпадения: {matches}")
                    
            elif choice == "5":
                # Копирование и модификация
                inventory_copy = self.inventory.copy()  # copy
                print(f"Создана копия инвентаря: {inventory_copy}")
                
                # Slicing
                if len(inventory_copy) >= 3:
                    first_three = inventory_copy[:3]  # slicing
                    print(f"Первые три предмета: {first_three}")
                    
            elif choice == "6":
                # Очистка
                if input("Точно очистить инвентарь? (да/нет): ").lower() == "да":
                    self.inventory.clear()  # clear
                    print("Инвентарь очищен!")
                    
            elif choice == "0":
                break
            else:
                print("Неверный выбор!")
    
    def move_player(self) -> bool:
        "Перемещение игрока по лабиринту"
        x, y = self.player_pos
        
        print("\nКуда идти?")
        print("w - вверх, s - вниз, a - влево, d - вправо")
        print("i - управление инвентарем, q - выход")
        
        move = input("Ваш выбор: ").lower()
        
        if move == "q":
            return False
        elif move == "i":
            self.manage_inventory()
            return True
        
        new_x, new_y = x, y
        
        if move == "w" and x > 0:
            new_x -= 1
        elif move == "s" and x < self.maze_size[0] - 1:
            new_x += 1
        elif move == "a" and y > 0:
            new_y -= 1
        elif move == "d" and y < self.maze_size[1] - 1:
            new_y += 1
        else:
            print("Нельзя двигаться в этом направлении!")
            return True
        
        self.player_pos = (new_x, new_y)
        return True
    
    def play(self) -> None:
        "Основной игровой цикл"
        print("ДОБРО ПОЖАЛОВАТЬ В ЛАБИРИНТ СПИСКОВ!")
        print("Цель: найти выход из лабиринта, используя ключ.")
        print("Изучайте методы работы со списками Python по пути!")
        
        self.generate_maze()
        
        while self.health > 0:
            self.display_maze()
            self.show_status()
            self.handle_room_event()
            
            # Проверка победы
            if self.player_pos == self.exit_pos and self.has_key:
                print("\n🎉 ПОЗДРАВЛЯЮ! ВЫ ПОБЕДИЛИ! 🎉")
                print("Вы освоили методы работы со списками Python:")
                print("- append(), extend() - добавление элементов")
                print("- remove(), pop() - удаление элементов") 
                print("- sort(), reverse() - сортировка")
                print("- index(), in - поиск элементов")
                print("- copy(), slicing - копирование")
                print("- list comprehension - генерация списков")
                break
            
            if not self.move_player():
                print("Игра завершена.")
                break
        
        if self.health <= 0:
            print("\n💀 ВЫ ПРОИГРАЛИ! 💀")
            print("Ваше здоровье закончилось.")


if __name__ == "__main__":
    game = ListMazeGame()
    game.play()
