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
        self.rebith_click = 1
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
    if 'click-upgrade-cost' in document:
        document['click-upgrade-cost'].text = str(game.click_upgrade_cost)
    if 'auto-clicker-cost' in document:
        document['auto-clicker-cost'].text = str(game.auto_clicker_cost)
    if "rebith-cost" in document:
        document["rebith-cost"].text = str(game.rebith_cost)

def buy_upgrade(evt):
    # Получаем ID улучшения из атрибута кнопки
    button = evt.target
    upgrade_div = button.parent
    upgrade_id = upgrade_div.attrs.get('upgrade-id')

    if upgrade_id == 'click-upgrade':
        if game.coins >= game.click_upgrade_cost:
            game.coins -= game.click_upgrade_cost
            game.click_power *= 2
            game.click_upgrade_cost *= 2
            update_display()
            save_data()
            alert('Улучшение куплено! Теперь каждый клик приносит в 2 раза больше монет.')
        else:
            alert('Недостаточно монет для покупки улучшения.')

    elif upgrade_id == 'auto-clicker':
        if game.coins >= game.auto_clicker_cost:
            game.coins -= game.auto_clicker_cost
            game.auto_clicker_count += 1
            game.auto_clicker_cost = int(game.auto_clicker_cost * 1.5)
            update_display()
            save_data()
            alert(f'Автокликер куплен! Теперь у вас {game.auto_clicker_count} автокликер(ов).')
        else:
            alert('Недостаточно монет для покупки автокликера.')
    elif upgrade_id == 'rebith':
        if game.coins >= game.rebith_cost:
            game.coins -= game.rebith_cost
            game.coins += 1000000
            game.rebiths += 1
            game.rebith_cost *= 2
            game.coins = 0
            game.auto_clicker_count = 0
            game.click_power = 0
            update_display()
            save_data()
            alert('Перерождение успешно завершено!')
        else:
            alert('Недостаточно монет для перерождения.')


def init():
    # Загружаем сохранённые данные
    load_data()
    update_display()

    # Привязываем обработчики к кнопкам
    for upgrade_div in document.select('.upgrade'):
        button = upgrade_div.select_one('button')
        if button:
            button.bind('click', buy_upgrade)
            # Убираем атрибут onclick, так как теперь используем bind
            if 'onclick' in button.attrs:
                del button.attrs['onclick']

# Запускаем инициализацию при загрузке страницы
init()