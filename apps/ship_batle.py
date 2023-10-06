from random import randint, seed

from time import sleep

seed(102)


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        """
        Конструктор класса Ship.
        """
        self._x = x
        self._y = y
        self._length = length
        self._tp = tp
        self._is_move = True  # метка возможно ли перемещение корабля
        # Список _cells будет сигнализировать о попадании соперником в какую-либо палубу корабля.
        # Если стоит 1, то попадания не было, а если стоит значение 2, то произошло попадание в соответствующую палубу.
        self._cells = [1] * length

    @property
    def tp(self):
        return self._tp

    @tp.setter
    def tp(self, value):
        self._tp = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, value):
        self._cells = value

    @property
    def is_move(self):
        return self._is_move

    @is_move.setter
    def is_move(self, value):
        self._is_move = value

    def set_start_coords(self, x, y):
        """
        Устанавливает начальные координаты корабля.
        Параметры:
            - x: координата x начальной позиции корабля
            - y: координата y начальной позиции корабля
        """
        self._x = x
        self._y = y

    def get_start_coords(self):
        """
        Возвращает начальные координаты корабля.
        Возвращает:
            - кортеж с координатами (x, y)
        """
        return self._x, self._y

    # is_collide(ship) - проверка на столкновение с другим кораблем ship
    # (столкновением считается, если другой корабль или пересекается с текущим или просто соприкасается,
    # в том числе и по диагонали); метод возвращает True, если столкновение есть и False - в противном случае;
    def is_collide(self, ship_0):
        """
        Проверка на столкновение с другим кораблем ship
        возвращает True если корабли пересекаются
        возвращает False если корабли не пересекаются
        Параметры:
        - self: корабль основной будет
        - ship: проверяемый корабль
        """
        if ship_0.x is not None and ship_0.y is not None:
            self_coordinates = self.get_coordinates(self)
            other_coordinates = ship_0.get_coordinates(ship_0)

            for self_coord in self_coordinates:
                for other_coord in other_coordinates:
                    dx = abs(self_coord[0] - other_coord[0])
                    dy = abs(self_coord[1] - other_coord[1])
                    if dx <= 1 and dy <= 1:
                        return True

        return False

    # вспомогательная функция для проверки
    @staticmethod
    def get_coordinates(ship_1):
        coordinates = []
        # создаем список координат если расположение горизонтальное
        if ship_1.tp == 1:
            for i in range(ship_1.length):
                coordinates.append((ship_1.x + i, ship_1.y))
            return coordinates
        # создаем список координат если расположение вертикальное
        if ship_1.tp == 2:
            for i in range(ship_1.length):
                coordinates.append((ship_1.x, ship_1.y + i))
            return coordinates

    def is_out_pole(self, size):
        """
        Проверяет, вышел ли корабль за пределы игрового поля.
        Параметры: - size: размер игрового поля
        Возвращает:- True, если корабль вышел за пределы игрового поля, иначе False
        """
        if self.x is not None and self.y is not None:
            if self.tp == 1:  # горизонтальная ориентация корабля
                # проверка на то что x y не выходят за пределы поля
                if (0 <= self.x <= size - 1) and (0 <= self.y <= size - 1):
                    # проверка с учетом длинны корабля
                    if self.x + (self.length - 1) <= size - 1:
                        return False

            else:  # вертикальная ориентация корабля
                # проверка на то что x y не выходят за пределы поля
                if (0 <= self.x <= size - 1) and (0 <= self.y <= size - 1):
                    # проверка с учетом длинны корабля
                    if self.y + (self.length - 1) <= size - 1:
                        return False
            return True

    # С помощью магических методов __getitem__() и __setitem__() обеспечить доступ к коллекции _cells следующим образом: 
    # value = ship[indx] # считывание значения из _cells по индексу indx (индекс отсчитывается от 0)
    # ship[indx] = value # запись нового значения в коллекцию _cells
    def __getitem__(self, key):
        return self.cells[key]

    def __setitem__(self, key, value):
        self.cells[key] = value


############################################################################
class GamePole:
    def __init__(self, size):
        """
        Конструктор класса GamePole.
        Параметры: - size: размер игрового поля
        """
        self._size = size
        self._ships = []  # список кораблей
        self._playing_field = None  # игровое поле с расставленными кораблями

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def ships(self):
        return self._ships

    @ships.setter
    def ships(self, value):
        self._ships = value

    @property
    def playing_field(self):
        return self._playing_field

    @playing_field.setter
    def playing_field(self, value):
        self._playing_field = value

    def init(self):  # метод работает только с полями 8х8, 9х9, 10х10 и больше
        """
        init() - начальная инициализация игрового поля;
        здесь создается список из кораблей (объектов класса Ship):
        однопалубных - 4; двухпалубных - 3; трехпалубных - 2; четырехпалубный - 1
        (ориентация этих кораблей должна быть случайной).
        
        Корабли формируются в коллекции _ships следующим образом:
        однопалубных - 4; двухпалубных - 3; трехпалубных - 2; четырехпалубный - 1.
        Ориентация этих кораблей должна быть случайной.
        Для этого можно воспользоваться функцией randint следующим образом:
        [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), ...]
        Начальные координаты x, y не расставленных кораблей равны None.
        После этого, выполняется их расстановка на игровом поле со случайными координатами так,
        чтобы корабли не пересекались между собой.
        """
        # список кораблей
        self.ships = [
            Ship(4, tp=randint(1, 2)),
            Ship(3, tp=randint(1, 2)),
            Ship(3, tp=randint(1, 2)),
            Ship(2, tp=randint(1, 2)),
            Ship(2, tp=randint(1, 2)),
            Ship(2, tp=randint(1, 2)),
            Ship(1, tp=randint(1, 2)),
            Ship(1, tp=randint(1, 2)),
            Ship(1, tp=randint(1, 2)),
            Ship(1, tp=randint(1, 2))
        ]

        try:
            # заведём временную переменную для того что-бы, в случае если на поле физически не хватает места для
            # размещения корабля откатимся на один шаг назад что-бы переместить предыдущий корабль
            # переместив предыдущий корабль есть вероятность, что на поле появится место для корабля которому физически
            # не хватало места
            temp_ship_prev = None  # предыдущий корабль
            # начинаем задавать координаты для расстановки кораблей
            # проходим циклом по списку кораблей - self._ships
            for ship_3 in self.ships:
                # задаем новые координаты кораблю
                ship_3.x = randint(0, self.size - 1)
                ship_3.y = randint(0, self.size - 1)

                # задав координаты начинаем проверять подходит ли размещение корабля на поле
                # если не подходят то повторяем цикл while до тех пор пока не будут найдены нужные координаты
                count = 0  # переменная счётчик попыток подбора координат
                while True:  # первый цикл
                    # проверяем выходит ли за пределы поля функцией - is_out_pole() True, если за пределами
                    # так же проверяем на столкновение кораблей функцией - is_collide() True, если столкновение есть
                    # создаю временный список кораблей с удаленным проверяемым кораблём
                    temp_lst = self.ships[:]
                    # удаляю из списка корабль который проверяется
                    temp_lst.remove(ship_3)
                    # проверка на столкновение и в поле ли корабль по отношению к другим
                    if ship_3.is_out_pole(self.size) or any(list(map(ship_3.is_collide, temp_lst))):
                        # если проверка не прошла то подбираем другие координаты
                        ship_3.x = randint(0, self.size - 1)
                        ship_3.y = randint(0, self.size - 1)
                        # считаем попытки подбора новых координат
                        count += 1
                        # если после 10 неудачных попыток координаты не подходят для размещения корабля
                        if count >= 10:
                            # запускаем второй цикл но откатившись на шаг назад
                            # берём предыдущий корабль от реального смещаем его для освобождения большего пространства
                            while True:  # второй цикл
                                count += 1  # счётчик попыток 
                                # print(count)
                                # меняем координаты предыдущего корабля для попытки освобождения места на поле
                                # для проблемного корабля
                                temp_ship_prev.x = randint(0, self.size - 1)
                                temp_ship_prev.y = randint(0, self.size - 1)
                                # создаю временный список кораблей с удаленным проверяемым кораблём
                                temp_lst = self.ships[:]  # временный список
                                temp_lst.remove(temp_ship_prev)  # удаляю из списка корабль который проверяется
                                # проверяем выходит ли за пределы поля функцией - is_out_pole() True, если за пределами
                                # так же проверяем на столкновение кораблей функцией - is_collide() True, если столкновение есть
                                if temp_ship_prev.is_out_pole(self.size) or any(
                                        list(map(temp_ship_prev.is_collide, temp_lst))):
                                    # если проверка не прошла то while запускаем снова
                                    if count >= self.size * 2:
                                        # если количество попыток превысило количество клеток всего игрового поля
                                        # генерируется ошибка превышения количества попыток, вся процедура повторяется снова
                                        # переходит в блок except
                                        raise Exception(
                                            "\nПодбор попыток исчерпан !!!!\nКорабли не могут быть расставлены на поле\n"
                                            "Перезапустите игру")
                                    else:
                                        # если проверка не прошла то подбираем другие координаты
                                        ship_3.x = randint(0, self.size - 1)
                                        ship_3.y = randint(0, self.size - 1)
                                else:  # если проверка прошла то выходим из второго цикла
                                    break  # выход из второго цикла while

                    # если проверка прошла выходим из цикла while (первый цикл)
                    else:
                        temp_ship_prev = ship_3
                        # print(ship_3)
                        break  # выход из второго цикла while
        except Exception as error:
            if error:
                # если произошла ошибка то процедура начинается с самого начала
                self.init()

        self.playing_field_coord()

    def playing_field_coord(self):
        """
        Функция генерации игрового поля в виде списка с расставленными кораблями
        """
        # ------ теперь создадим физически поле с учетом созданных кораблей - self._playing_field ----------------
        # создаем список нашего игрового поля заполняется весь в воде - 0
        field = list([0 for __ in range(self.size)] for _ in range(self.size))
        # теперь на поле нужно поставить корабли основываясь по координатам
        # сгенерируем список координат корабля и каждой палубы (учитывая его длину)
        coords_ship = [[*self.coord_ship(_), _.cells, _.tp] for _ in self.ships]
        #      пример    [(x, y),(x, y), (x, y),(x, y), _cells, _t] - координаты корабля 4 палубы
        # coords_ship = [[(0, 1), (0, 2), (0, 3), (0, 4), [1, 1, 1, 1], 2],
        #                [(2, 5), (3, 5), (4, 5), [1, 1, 1], 1],
        #                [(8, 3), (8, 4), (8, 5), [1, 1, 1], 2],
        #                [(6, 5), (6, 6), [1, 1], 2],
        #                [(4, 7), (4, 8), [1, 1], 2],
        #                [(2, 2), (3, 2), [1, 1], 1],
        #                [(5, 3), [1], 1],
        #                [(1, 8), [1], 2],
        #                [(6, 1), [1], 2],
        #                [(8, 8), [1], 2]
        #                ]
        # берем список координат наших кораблей по палубам - coords_ship
        # и вносим изменения в список пустого игрового роля - field
        # проходим по списку координат кораблей
        for i in coords_ship:
            # получаю срез координат каждой палубы
            for ind, vol in enumerate(i[:-2]):  # (7, 4), (), ()
                # в пустом поле - pole меняю воду(0) по координате, на обозначение палуб из списка _cells
                # учитывая есть ли попадание в палубу-(2) или нет попадания в палубу-(1)
                # вставляем в список по координате обозначение или 1 или 2 из списка _cells
                field[vol[1]].insert(vol[0], i[-2][ind])
                field[vol[1]].pop(vol[0] + 1)
        #
        self.playing_field = field

    def get_ships(self):
        """Возвращает коллекцию _ships"""
        return self.ships

    def show(self):
        """
        show() - отображение игрового поля в консоли
        (корабли должны отображаться значениями из коллекции _cells каждого корабля, вода - значением 0);
        """
        if self.playing_field is not None:
            [print(*_) for _ in self.playing_field]
        else:
            print("Поле не инициализировано, корабли не раcставленны\nНеобходимо инициализировать поле !!!")

    def coord_ship(self, ship_4):
        """"
        Функция возвращает кортеж координат всех палуб корабля в виде:
        - 1палуб 
        - 2палуб 
        - 3палуб 
        - 4палуб 
        """
        # если корабль горизонтального расположения _tp == 1
        if ship_4.tp == 1:  # увеличиваем по горизонтали x
            # координаты x,y 
            coord = [(ship_4.x + _, ship_4.y) for _ in range(ship_4.length)]

            return coord

            # если корабль вертикального расположения _tp == 2
        elif ship_4.tp == 2:  # увеличиваем по вертикали _y
            coord = [(ship_4.x, ship_4.y + _) for _ in range(ship_4.length)]
            return coord

    def get_pole(self):
        """
        get_pole() - получение текущего игрового поля в виде двумерного (вложенного) кортежа размерами size x size элементов.
        """
        # создаем список нашего игрового поля заполняется весь в воде - 0
        pole = list([0 for __ in range(self.size)] for _ in range(self.size))
        # вывод поля на печать
        # [print(_)for _ in pole]
        # теперь на поле нужно поставить корабли основываясь по координатам
        # сгенерируем список координаты корабля и каждой палубы
        # coords_ship = [[(x, y), len, tp], [(x, y), len, tp], ..., ...]
        coords_ship = [[*self.coord_ship(_), _.length, _.tp] for _ in self.ships]
        # print()
        # вывод координат кораблей на экран
        # [print(f"{_}")for _ in coords_ship]
        # print()
        # берем список координат наших кораблей по палубам - coords_ship
        # и вносим изменения в список пустого игрового роля - pole
        for i in coords_ship:  # [(7, 4), 1, '~']
            for j in i[:-2]:  # (7, 4)
                pole[j[1]].insert(j[0], 1)
                pole[j[1]].pop(j[0] + 1)

        # [print(_) for _ in pole]
        tpl = tuple(tuple(_) for _ in tuple(pole))
        return tpl


class SeaBattle:
    """
    Управления игровым процессом в целом.
    Игра должна осуществляться между человеком и компьютером.
    Выстрелы со стороны компьютера можно реализовать случайным образом в свободные клетки.
    Сыграйте в эту игру и выиграйте у компьютера.
    """

    def __init__(self):
        size_pole = int(10)  # ввод размера игрового поля

        COMP = GamePole(size_pole)
        COMP.init()
        self.COMP = COMP  # игровое поле компьютера
        self.COMP_shot_list = list()  # список выстрелов компа

        PLAYER = GamePole(size_pole)
        PLAYER.init()
        self.PLAYER = PLAYER  # игровое поле игрока
        self.PLAYER_shot_list = list()  # список выстрелов игрока

        # кто сейчас ходит COMP или PLAYER
        # если 1 тот и ходит
        # у кого 0 тот ожидает очереди
        self.initiative_move_comp = 0
        self.initiative_move_player = 1

    def coordinate_check(self, coord):
        """
        Проверка вводимых координат игроком или компьютером.
        Координаты должны быть в пределах размера игрового поля(_size).
        Координаты должны быть двух значным числом.
        """
        if coord == "stop":
            return "stop"
        else:
            try:
                if self.initiative_move_player:  # если ход игрока
                    x_coord, y_coord = tuple(map(int, coord))
                elif self.initiative_move_comp:  # если ход компьютера
                    x_coord, y_coord = tuple(map(int, str(coord)))
            except Exception:
                return False

            # если ход игрока
            if self.initiative_move_player and coord.isdigit() and len(coord) == 2 and \
                    type(x_coord) is int and type(y_coord) is int and \
                    0 <= x_coord < self.COMP.size and 0 <= y_coord < self.COMP.size:
                return True
            # если ход компьютера
            elif self.initiative_move_comp and str(coord).isdigit() and len(str(coord)) == 2 and \
                    type(x_coord) is int and type(y_coord) is int and \
                    0 <= x_coord < self.PLAYER.size and 0 <= y_coord < self.PLAYER.size:
                return True
            else:
                return False

    # TODO есть повторение кода, стоит переписать
    def checking_if_the_ship_was_hit(self, coord):
        """
        Проверка на попадание по кораблю
        Проверяем списки с координатами игрока или компьютера
        """
        # если ход ИГРОКА проверяем список компа
        if self.initiative_move_player:
            # создаем список координат всех кораблей с учётом длины палубы
            coords_ship_COMP = [[*self.COMP.coord_ship(_), _.cells, _.tp] for _ in self.COMP.ships]
            # проходим по кораблям в поиске нужной палубы
            for ind_ship, val in enumerate(coords_ship_COMP):
                if coord in val:  # если координаты есть в списке палуб корабля
                    ind = val.index(coord)  # находим индекс координаты
                    # в списке _cells меняем по индексу что есть попадание (если попали то 2)
                    self.COMP.ships[ind_ship].cells[ind] = 2

                    # перерисовываем _playing_field(игровое поле) в переменной объекта с учетом попадания в корабль
                    self.COMP.playing_field_coord()
                    # добавляем в поле COMP.playing_field выстрелы из списка PLAYER_shot_list
                    # игнорируем если по координатам есть палуба корабля цифры 1и2 но если стоит 0 то меняем на "*"
                    for _ in self.PLAYER_shot_list:
                        if self.COMP.playing_field[_[1]][_[0]] == 0:
                            self.COMP.playing_field[_[1]][_[0]] = "*"

                    # проверяем состояние корабля
                    if all(list(map(lambda x: True if x == 2 else False, self.COMP.ships[ind_ship].cells))):
                        return "убит"
                    elif any(list(map(lambda x: True if x == 1 else False, self.COMP.ships[ind_ship].cells))):
                        return "ранен"
                else:
                    continue

            # если по координатам нет палубы корабля в списке кораблей
            # отмечаем в списке объекта COMP._playing_field промах - *
            self.COMP.playing_field[coord[1]][coord[0]] = '*'
            return "мимо"

        # если ход КОМПА проверяем список игрока
        elif self.initiative_move_comp:
            # создаем список координат всех кораблей с учётом длины палубы
            coords_ship_PLAYER = [[*self.PLAYER.coord_ship(_), _.cells, _.tp] for _ in self.PLAYER.ships]
            # проходим по кораблям в поиске нужной палубы
            for ind_ship, val in enumerate(coords_ship_PLAYER):
                if coord in val:  # если координаты есть в списке палуб корабля
                    ind = val.index(coord)  # находим индекс координаты
                    # в списке _cells меняем по индексу что есть попадание (если попали то 2)
                    self.PLAYER.ships[ind_ship].cells[ind] = 2
                    # перерисовываем _playing_field(игровое поле) в переменной объекта
                    self.PLAYER.playing_field_coord()
                    # добавляем в поле PLAYER.playing_field выстрелы из списка COMP_shot_list
                    # игнорируем если по координатам есть палуба корабля цифры 1и2 но если стоит 0 то меняем на "*"
                    for _ in self.COMP_shot_list:
                        if self.PLAYER.playing_field[_[1]][_[0]] == 0:
                            self.PLAYER.playing_field[_[1]][_[0]] = "*"

                    # проверяем состояние корабля
                    if all(list(map(lambda x: True if x == 2 else False, self.PLAYER.ships[ind_ship].cells))):
                        return "убит"
                    elif any(list(map(lambda x: True if x == 1 else False, self.PLAYER.ships[ind_ship].cells))):
                        return "ранен"
                else:
                    continue

            # если по координатам нет палубы корабля
            # отмечаем в списке объекта COMP._playing_field промах - *
            self.PLAYER.playing_field[coord[1]][coord[0]] = '*'
            return "мимо"

    def checking_if_all_ships_are_hit(self):
        """
        Функция проверки игры, все ли корабли подбиты.
        """
        # создаем список с палубами кораблей
        ship_comp = [__ for _ in self.COMP.ships for __ in _.cells]
        ship_player = [__ for _ in self.PLAYER.ships for __ in _.cells]
        # если все палубы кораблей подбиты то сообщаем об окончании игры
        if all(map(lambda x: True if x == 2 else False, ship_comp)):
            return "player"
        elif all(map(lambda x: True if x == 2 else False, ship_player)):
            return "comp"

    def start_game(self):
        """
        Запуск игры
        """
        while True:
            # если все корабли подбиты то останавливаем игру
            if self.checking_if_all_ships_are_hit() == "player":
                print("\nПобеда ИГРОКА !!!\n")
                break
            elif self.checking_if_all_ships_are_hit() == "comp":
                print("\nПобеда КОМПЬЮТЕРА !!!\n")
                break

            # --------- если ход игрока ---------
            if self.initiative_move_player:
                x_y_cord = input(
                    f"\nВведите координаты для выстрела по кораблю двузначное число.\n"
                    f"Первая цифра это ось X по горизонтали от 0-{self.COMP.size - 1}\n"
                    f"Вторая цифра это ось Y по вертикали от 0-{self.COMP.size - 1}\n"
                    f"Ожидаю: ")

                if x_y_cord == "stop":
                    print("\nИгра остановлена...\n")
                    break

                if not self.coordinate_check(x_y_cord):  # Проверка координат
                    print("\nВы ввели неправильные координаты для выстрела\n")
                    continue
                else:
                    x_y_cord = tuple(map(int, x_y_cord))  # переводим введённые координаты в кортеж (x, y)

                    # проверяем что координат выстрела нет в списке выстрелов по противнику
                    if x_y_cord not in self.PLAYER_shot_list:  # если координат в списке выстрелов нет
                        # добавляем координаты в список выстрелов по кораблям противника
                        self.PLAYER_shot_list.append(x_y_cord)
                    else:  # если координаты выстрела есть в списке необходимо запросить новые координаты
                        print(
                            f"\nВы уже стреляли в эту точку по координатам - {x_y_cord}\nВведите другие координаты !!")
                        continue

                        # теперь нужно проверить выстрел на предмет ранен\убит\мимо по кораблю
                    if self.checking_if_the_ship_was_hit(x_y_cord) == "ранен":
                        # выводим поле в консоль что бы показать выстрел
                        [print(*_) for _ in self.COMP.playing_field]
                        # оповещение о результате выстрела
                        print("\nРанен !\n")
                        continue

                    if self.checking_if_the_ship_was_hit(x_y_cord) == "убит":
                        # выводим поле в консоль что бы показать выстрел
                        [print(*_) for _ in self.COMP.playing_field]
                        # оповещение о результате выстрела
                        print("\nУбит !\n")
                        continue

                    if self.checking_if_the_ship_was_hit(x_y_cord) == "мимо":
                        # выводим поле в консоль что бы показать выстрел
                        [print(*_) for _ in self.COMP.playing_field]
                        # оповещение о результате выстрела
                        print("Мимо !\n")
                        # меняем инициативу хода
                        self.initiative_move_player = 0
                        self.initiative_move_comp = 1
            # ----------- end ход игрока -----------

            # ----------- если ход компьютера  -----------
            elif self.initiative_move_comp:
                print("\nХод компьютера !")
                print("Ожидаю: ", end="")
                sleep(0.5)
                x_y_cord = str(randint(0, self.COMP.size - 1)) + str(randint(0, self.COMP.size - 1))
                print(x_y_cord)

                if not self.coordinate_check(x_y_cord):  # Проверка координат
                    print("\nВы ввели неправильные координаты для выстрела\n")
                    continue
                else:
                    x_y_cord = tuple(map(int, str(x_y_cord)))  # переводим введённые координаты в кортеж (x, y)

                    # проверяем что координат выстрела нет в списке выстрелов по противнику
                    if x_y_cord not in self.COMP_shot_list:  # если координат в списке выстрелов нет
                        # добавляем координаты в список выстрелов по кораблям противника
                        self.COMP_shot_list.append(x_y_cord)
                    else:  # если координаты выстрела уже есть в списке необходимо запросить новые координаты
                        print(
                            f"\nВы уже стреляли в эту точку по координатам - {x_y_cord}\nВведите другие координаты !!")
                        continue

                    # теперь нужно проверить выстрел на предмет ранен\убит\мимо по кораблю
                    if self.checking_if_the_ship_was_hit(x_y_cord) == "ранен":
                        print("\nРанен !\n")
                        continue
                    elif self.checking_if_the_ship_was_hit(x_y_cord) == "убит":
                        print("\nУбит !\n")
                        continue

                    elif self.checking_if_the_ship_was_hit(x_y_cord) == "мимо":
                        print("Мимо !\n")
                        # если мимо меняем инициативу хода
                        self.initiative_move_player = 1
                        self.initiative_move_comp = 0


# My test
# play = SeaBattle()
# play.start_game()

# # TEST #####################################
# ship1 = Ship(2)
# ship2 = Ship(2, 1)
# ship = Ship(3, 2, 0, 0)
#
# assert ship._length == 3 and ship._tp == 2 and ship._x == 0 and ship._y == 0, "неверные значения атрибутов объекта класса Ship"
# assert ship._cells == [1, 1, 1], "неверный список _cells"
# assert ship._is_move, "неверное значение атрибута _is_move"
#
# ship.set_start_coords(1, 2)
# assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
# assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"
# #
# ship.move(1)
# # ## Ship(length, tp, x, y)
# s1 = Ship(4, 1, 0, 0)
# s2 = Ship(3, 2, 0, 0)
# s3 = Ship(3, 2, 0, 2)
# s4 = Ship(4, 2, 0, 1)
# s5 = Ship(3, 2, 1, 0)
# #
# assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
# assert s1.is_collide(
#     s3) == False, "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"
# assert s1.is_collide(s4), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(4, 2, 0, 1)"
# #
# s2 = Ship(3, 2, 1, 1)
# assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"
# assert s2.is_collide(s2) == True, "неверно работает метод is_collide() для кораблей Ship(3, 2, 1, 1) и Ship(3, 2, 1, 1)"
# assert s2.is_collide(s5) == True, "неверно работает метод is_collide() для кораблей Ship(3, 2, 1, 1) и Ship(3, 2, 1, 0)"
#
# #
# # Ship(length, tp, x, y)
# s2 = Ship(3, 1, 8, 1)
# assert s2.is_out_pole(10), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"
# #
# s2 = Ship(3, 2, 1, 5)
# assert s2.is_out_pole(10) == False, "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"
# #
# s2[0] = 2
# assert s2[0] == 2, "неверно работает обращение ship[indx]"
# #
# p = GamePole(10)
# p.init()

# for nn in range(5):
#     for s in p._ships:
#         assert s.is_out_pole(10) == False, "корабли выходят за пределы игрового поля"
#
#         for ship in p.get_ships():
#             if s != ship:
#                 assert s.is_collide(ship) == False, "корабли на игровом поле соприкасаются"
#     p.move_ships()
#
# gp = p.get_pole()
# assert type(gp) == tuple and type(gp[0]) == tuple, "метод get_pole должен возвращать двумерный кортеж"
# assert len(gp) == 10 and len(gp[0]) == 10, "неверные размеры игрового поля, которое вернул метод get_pole"
# p.show()
