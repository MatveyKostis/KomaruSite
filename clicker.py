from browser import document, window, alert, html
from browser.local_storage import storage
import json
import time


# Инициализация переменных
class GameState:
    def __init__(self):
        self.coins = 0
        self.clicks = 0
        self.click_power = 1
        self.click_upgrade_cost = 200
        self.auto_clicker_count = 0
        self.auto_clicker_cost = 500
        self.rebith_cost = 50000000
        self.rebiths = 1
        self.rebith_click = self.rebiths * 2
        self.last_update_time = time.time() * 1000


game = GameState()


def save_data():
    save_object = {
        'coins': game.coins,
        'clicks': game.clicks,
        'click_power': game.click_power,
        'click_upgrade_cost': game.click_upgrade_cost,
        'auto_clicker_count': game.auto_clicker_count,
        "rebith_cost": game.rebith_cost,
        "rebiths": game.rebiths,
        "rebith_click": game.rebith_click,
        'auto_clicker_cost': game.auto_clicker_cost,
        'last_update_time': time.time() * 1000
    }
    storage['komaruGameData'] = json.dumps(save_object)


def load_data():
    try:
        if 'komaruGameData' in storage:
            saved_data = json.loads(storage['komaruGameData'])
            game.coins = saved_data.get('coins', 0)
            game.clicks = saved_data.get('clicks', 0)
            game.click_power = saved_data.get('click_power', 1)
            game.click_upgrade_cost = saved_data.get('click_upgrade_cost', 200)
            game.auto_clicker_count = saved_data.get('auto_clicker_count', 0)
            game.auto_clicker_cost = saved_data.get('auto_clicker_cost', 500)
            game.rebith_cost = saved_data.get('rebith_cost', 50000000)
            game.rebiths = saved_data.get('rebiths', 1)
            game.rebith_click = saved_data.get('rebith_click', 1)
            game.last_update_time = saved_data.get('last_update_time', time.time() * 1000)
    except Exception as e:
        print('Error loading data:', e)


def update_display():
    # Обновляем только те элементы, которые существуют на странице
    if 'coins' in document:
        document['coins'].text = str(int(game.coins))
    if 'count' in document:
        document['count'].text = str(int(game.clicks))
    if 'click-upgrade-cost' in document:
        document['click-upgrade-cost'].text = str(game.click_upgrade_cost)
    if 'auto-clicker-cost' in document:
        document['auto-clicker-cost'].text = str(game.auto_clicker_cost)


def handle_click(evt):
    game.rebith_click = game.rebiths * 2
    if game.rebith > 1:
        game.clicks += game.click_power * game.rebith_click
        game.coins += game.click_power  * game.rebith_click
    else:
        game.clicks += game.click_power
        game.coins += game.click_power
    update_display()
    save_data()


def calculate_offline_progress():
    current_time = time.time() * 1000
    time_diff = (current_time - game.last_update_time) / 1000
    offline_clicks = game.auto_clicker_count * game.click_power * time_diff
    game.coins += offline_clicks
    game.clicks += offline_clicks
    game.last_update_time = current_time


def auto_click():
    if game.auto_clicker_count > 0:
        clicks_to_add = game.auto_clicker_count * game.click_power
        game.coins += clicks_to_add
        game.clicks += clicks_to_add
        update_display()
        save_data()


def init():
    # Загружаем сохранённые данные
    load_data()
    calculate_offline_progress()
    update_display()

    # Привязываем обработчик к изображению кликера
    if 'clicker-img' in document:
        document['clicker-img'].bind('click', handle_click)

    # Запускаем автокликер
    window.setInterval(auto_click, 1000)

    # Сохраняем данные каждые 10 секунд
    window.setInterval(save_data, 10000)


# Запускаем инициализацию при загрузке страницы
init()