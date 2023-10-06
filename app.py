from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages, g
from apps.ship_batle import SeaBattle
from apps.alerts import alert  # словарь оповещений
from random import randint, seed
import sqlite3
import os

# конфигурация приложения
# DATABASE = 'db/btl_ship.db'  # Путь к базе данных
DEBUG = True  # Включение режима отладки
SECRET_KEY = "ssdfnsmn"  # генерация ключа для работы функции flash()- оповещения на странице

app = Flask(__name__)
app.config.from_object(__name__)

# Переопределяем путь к базе данных относительно нашего приложения
# (так как приложений может быть много и базы данных могут быть разные)
# app.config.update(dict(DATABASE=os.path.join(app.root_path, 'db', 'btl_ship.db')))
# print(app.config['DATABASE'])

# Ключ для проверки
seed(102)
play = SeaBattle()


# Маршрут главная страница
@app.route('/')
def index():
    return render_template('index.html', title="Морской бой")


# Маршрут основная игра
@app.route('/start', methods=['GET', 'POST'])
def start():
    """Запуск игры"""
    # db = connect_db()  # соединение с базой данных
    player_pole = play.PLAYER.playing_field  # поле игрока с кораблями
    comp_pole = play.COMP.playing_field  # поле компа с открытыми кораблями для подглядывания на странице шаблона

    comp_pole_hide_ship = play.COMP.playing_field[:]  # поле компа с скрытыми кораблями но с учётом попадания и промаха
    #  обновляем поле с скрытыми кораблями что бы вывести в шаблоне после хода игрока
    comp_pole_hide_ship = [[0 if i == 1 else i for i in _] for _ in comp_pole_hide_ship]

    crd = None  # координаты выстрела (инициализация переменной crd)

    # если все корабли подбиты то останавливаем игру
    if play.checking_if_all_ships_are_hit() == "player":
        flash(alert["win_player"])

    elif play.checking_if_all_ships_are_hit() == "comp":
        flash(alert["win_comp"])

    elif play.initiative_move_player:  # если ход игрока:
        # проверяем чей сейчас ход
        if request.method == 'POST':  # если координаты были отправлены (был отправлен метод post)
            crd = request.form['coord_input']  # присваиваем введённые координаты переменной crd
            if play.coordinate_check(crd) == "stop":
                flash(alert["stop"])  # -Вы ввели stop.
            elif not play.coordinate_check(crd):  # Проверка координат
                flash(alert["error_coord"])  # -Вы ввели неправильные координаты для выстрела.
            else:
                x_y_cord = tuple(map(int, crd))  # переводим введённые координаты в кортеж (x, y)
                # проверяем что координат выстрела нет в списке выстрелов по противнику
                if x_y_cord not in play.PLAYER_shot_list:  # если координат в списке выстрелов нет
                    # добавляем координаты в список выстрелов по кораблям противника
                    play.PLAYER_shot_list.append(x_y_cord)
                    # теперь нужно проверить выстрел на предмет ранен\убит\мимо по кораблю
                    # при любом исходе поле с координатами перезаписывается
                    if play.checking_if_the_ship_was_hit(x_y_cord) == "ранен":
                        # обновляем поле противника для фиксации выстрела
                        comp_pole = play.COMP.playing_field
                        #  обновляем поле с скрытыми кораблями что бы вывести в шаблоне после хода игрока
                        comp_pole_hide_ship = [[0 if i == 1 else i for i in _] for _ in comp_pole_hide_ship]
                        # оповещение о результате выстрела
                        flash(alert["wounded"])
                        flash(alert["move_again"])
                        return redirect(url_for('start'))

                    elif play.checking_if_the_ship_was_hit(x_y_cord) == "убит":
                        # выводим поле в консоль что бы показать выстрел
                        comp_pole = play.COMP.playing_field
                        #  обновляем поле с скрытыми кораблями что бы вывести в шаблоне после хода игрока
                        comp_pole_hide_ship = [[0 if i == 1 else i for i in _] for _ in comp_pole_hide_ship]
                        # оповещение о результате выстрела
                        flash(alert["killed"])
                        flash(alert["move_again"])
                        return redirect(url_for('start'))

                    elif play.checking_if_the_ship_was_hit(x_y_cord) == "мимо":
                        # обновляем поле компа с фиксацией выстрела
                        comp_pole = play.COMP.playing_field
                        #  обновляем поле с скрытыми кораблями что-бы вывести в шаблоне после хода игрока

                        comp_pole_hide_ship = [[0 if i == 1 else i for i in _] for _ in comp_pole]
                        # оповещение о результате выстрела
                        flash(f'{alert["player_move"]}{crd}')  # выводим сообщение что ходе игрока
                        flash(alert["miss"])
                        # меняем инициативу хода
                        play.initiative_move_player = 0
                        play.initiative_move_comp = 1
                        # перезагружаем страницу для того что бы на поле появился выстрел
                else:  # если координаты выстрела есть в списке необходимо запросить новые координаты
                    flash(f'{alert["again-shot"]}{crd}')

    elif play.initiative_move_comp:  # если ход компьютера
        # messages = get_flashed_messages()
        # генерируем координаты для компьютера
        crd = str(randint(0, play.COMP.size - 1)) + str(randint(0, play.COMP.size - 1))
        # выводим на странице координаты хода компа
        flash(f'{alert["computer_move"]}{crd}')  # выводим сообщение что ход компьютера
        # Проверка координат что не выходят за пределы поля
        if not play.coordinate_check(crd):
            flash(alert["error_coord"])
        else:
            x_y_cord = tuple(map(int, str(crd)))  # переводим введённые координаты в кортеж (x, y)

            # проверяем что координат выстрела нет в списке выстрелов по противнику
            if x_y_cord not in play.COMP_shot_list:  # если координат в списке выстрелов нет
                # добавляем координаты в список выстрелов по кораблям противника
                play.COMP_shot_list.append(x_y_cord)
                # flash(f'Комп ввёл: {crd} (x-{crd[0]} y-{crd[1]})')
                # теперь нужно проверить выстрел на предмет ранен\убит\мимо по кораблю
                if play.checking_if_the_ship_was_hit(x_y_cord) == "ранен":
                    # обновляем поле противника для фиксации выстрела
                    comp_pole = play.PLAYER.playing_field
                    flash(alert["wounded"])
                    return redirect(url_for('start'))
                elif play.checking_if_the_ship_was_hit(x_y_cord) == "убит":
                    # обновляем поле противника для фиксации выстрела
                    comp_pole = play.PLAYER.playing_field
                    flash(alert["killed"])
                    return redirect(url_for('start'))

                elif play.checking_if_the_ship_was_hit(x_y_cord) == "мимо":
                    flash(alert["miss"])
                    flash("Теперь ВАШ ход ))")
                    # если мимо меняем инициативу хода
                    play.initiative_move_player = 1
                    play.initiative_move_comp = 0
                    return redirect(url_for('start'))
            else:  # если координаты выстрела уже есть в списке необходимо запросить новые координаты
                flash(f"Компьютер уже стрелял в эту точку - {crd}<br>Подбирает другие координаты !!")

    return render_template('start-game.html',
                           title="Морской Бой",
                           player_pole=player_pole,
                           comp_pole=comp_pole,
                           crd=crd,
                           move_comp=play.initiative_move_comp,
                           move_player=play.initiative_move_player,
                           win=play.checking_if_all_ships_are_hit(),
                           comp_pole_hide_ship=comp_pole_hide_ship,
                           )


# Маршрут для перезапуска игры
@app.route('/restart', methods=['POST'])
def restart_game():
    seed(102)
    # Ваш код для перезапуска игры
    global play
    play = SeaBattle()
    flash(f"Игра перезапущена !!")
    return redirect('/start')


# # Маршрут для регистрации
# @app.route('/login')
# def login():
#     return render_template('login.html', title="Авторизация")


# # Маршрут для авторизации на сайте
# @app.route('/authorization')
# def authorization():
#     return render_template('authorization.html', title="Регистрация")


# # --------------------------- работа с базой данных ----------------------------
# # функция соединения с базой данных
# def connect_db():
#     conn = sqlite3.connect(app.config['DATABASE'])  # устанавливаем соединение с бд
#     # DATABASE - C:\flaskProject\db\btl_ship.db
#     conn.row_factory = sqlite3.Row  # то что будет в базе данных будет предоставлено в виде словаря
#     # print("отработало")
#     return conn
#
#
# # функция создания таблиц в базе данных из некоего файла
# def creat_db():
#     db = connect_db()
#     with app.open_resource('db/add_table_db_from_app.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()  # записываем изменения в базу данных
#     db.close()  # закрываем базу данных
#
#
# #  соединение с бд если оно ещё не установлено
# def get_db():
#     if not hasattr(g, 'link_db'):  # если нет такого свойства в g значит устанавливаем соединение
#         g.link_db = connect_db()  # устанавливаем соединение через функцию connect_db()
#     return g.link_db  # если такое свойство есть в g то просто возвращаем
#
#
# # срабатывает автоматически когда идет уничтожение контекста приложения
# # в основном это происходит при завершении некоего запроса к серверу
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, "link_db"):  # если в g есть свойство "link_db" то закрыть соединение с бд
#         g.link_db.close()
#
#
# # --------------------------- работа с базой данных ----------------------------


if __name__ == '__main__':
    app.run()
    #app.run(host='0.0.0.0')

