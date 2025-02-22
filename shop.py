from browser import document, window, alert, html
from browser.local_storage import storage
import json
import time
# этот код запускается и используется через Brython, заранее спасибо

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
        'rebith_cost': game.rebith_cost,
        'rebiths': game.rebiths,
        'rebith_click': game.rebith_click,
        'auto_clicker_cost': game.auto_clicker_cost,
        'last_update_time': time.time() * 1000
    }
    storage['komaruGameData'] = json.dumps(save_object)

def load_data():
    try:
        if 'komaruGameData' in storage:
            saved_data = json.loads(storage['komaruGameData'])
            for attr, default in vars(game).items():
                setattr(game, attr, saved_data.get(attr, default))
    except Exception as e:
        print('Error loading data:', e)

def update_display():
    display_elements = {
        'click-upgrade-cost': game.click_upgrade_cost,
        'auto-clicker-cost': game.auto_clicker_cost,
        'rebith-cost': game.rebith_cost
    }

    for element_id, value in display_elements.items():
        if element_id in document:
            document[element_id].text = str(value)

def handle_click_upgrade():
    if game.coins >= game.click_upgrade_cost:
        game.coins -= game.click_upgrade_cost
        game.click_power *= 2
        game.click_upgrade_cost *= 2
        return True, 'Улучшение куплено! Теперь каждый клик приносит в 2 раза больше монет.'
    return False, 'Недостаточно монет для покупки улучшения.'

def handle_auto_clicker():
    if game.coins >= game.auto_clicker_cost:
        game.coins -= game.auto_clicker_cost
        game.auto_clicker_count += 1
        game.auto_clicker_cost = int(game.auto_clicker_cost * 1.5)
        return True, f'Автокликер куплен! Теперь у вас {game.auto_clicker_count} автокликер(ов).'
    return False, 'Недостаточно монет для покупки автокликера.'

def handle_rebirth():
    if game.coins >= game.rebith_cost:
        # Сохраняем количество перерождений и увеличиваем его
        old_rebirths = game.rebiths
        game.rebiths += 1

        # Сбрасываем все значения на дефолтные
        game.coins = 0
        game.click_power = 1
        game.click_upgrade_cost = 200  # Сброс на начальную стоимость
        game.auto_clicker_count = 0
        game.auto_clicker_cost = 500   # Сброс на начальную стоимость
        game.rebith_cost *= 2

        return True, f'Перерождение успешно завершено! Теперь у вас {game.rebiths} перерождений!'
    return False, 'Недостаточно монет для перерождения.'

def buy_upgrade(evt):
    button = evt.target
    upgrade_div = button.parent
    upgrade_id = upgrade_div.attrs.get('upgrade-id')

    upgrade_handlers = {
        'click-upgrade': handle_click_upgrade,
        'auto-clicker': handle_auto_clicker,
        'rebith': handle_rebirth
    }

    if upgrade_id in upgrade_handlers:
        success, message = upgrade_handlers[upgrade_id]()
        if success:
            update_display()
            save_data()
        alert(message)

def init():
    load_data()
    update_display()

    for upgrade_div in document.select('.upgrade'):
        button = upgrade_div.select_one('button')
        if button:
            button.bind('click', buy_upgrade)
            if 'onclick' in button.attrs:
                del button.attrs['onclick']

init()