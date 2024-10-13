// Инициализация переменных
let coins = 0;
let clicks = 0;
let clickPower = 1;
let clickUpgradeCost = 200;
let autoClickerCount = 0;
let autoClickerCost = 500;
let lastUpdateTime = Date.now();

// Функция для сохранения данных в localStorage
function saveData() {
    const saveObject = {
        coins,
        clicks,
        clickPower,
        clickUpgradeCost,
        autoClickerCount,
        autoClickerCost,
        lastUpdateTime: Date.now()
    };
    localStorage.setItem('komaruGameData', JSON.stringify(saveObject));
    console.log('Data saved:', saveObject);
}

// Функция для загрузки данных из localStorage
function loadData() {
    const savedData = JSON.parse(localStorage.getItem('komaruGameData'));
    if (savedData) {
        coins = savedData.coins || 0;
        clicks = savedData.clicks || 0;
        clickPower = savedData.clickPower || 1;
        clickUpgradeCost = savedData.clickUpgradeCost || 200;
        autoClickerCount = savedData.autoClickerCount || 0;
        autoClickerCost = savedData.autoClickerCost || 500;
        lastUpdateTime = savedData.lastUpdateTime || Date.now();
        console.log('Data loaded:', savedData);
    }
}

// Функция для обновления отображения монет и кликов
function updateDisplay() {
    const coinsElement = document.getElementById('coins');
    const countElement = document.getElementById('count');
    const upgradeCostElement = document.getElementById('click-upgrade-cost');
    const autoClickerCostElement = document.getElementById('auto-clicker-cost');

    if (coinsElement) coinsElement.textContent = Math.floor(coins);
    if (countElement) countElement.textContent = Math.floor(clicks);
    if (upgradeCostElement) upgradeCostElement.textContent = clickUpgradeCost;
    if (autoClickerCostElement) autoClickerCostElement.textContent = autoClickerCost;

    console.log('Display updated:', { coins, clicks, clickUpgradeCost, autoClickerCost });
}

// Функция для обработки клика по изображению
function handleClick() {
    clicks += clickPower;
    coins += clickPower;
    updateDisplay();
    saveData();
    console.log('Click handled:', { coins, clicks });
}

// Функция для покупки улучшения
function buyUpgrade(upgradeId) {
    console.log('Attempting to buy upgrade:', upgradeId);
    console.log('Before purchase:', { coins, clickPower, clickUpgradeCost, autoClickerCount, autoClickerCost });

    switch(upgradeId) {
        case 'click-upgrade':
            // Проверка наличия монет для улучшения клика
            if (coins >= clickUpgradeCost) {
                coins -= clickUpgradeCost; // Списываем стоимость улучшения
                clickPower *= 2; // Увеличиваем силу клика
                clickUpgradeCost *= 2; // Увеличиваем стоимость следующего улучшения
                updateDisplay(); // Обновляем отображение
                saveData(); // Сохраняем данные
                alert('Улучшение куплено! Теперь каждый клик приносит в 2 раза больше монет.');
                console.log('Click upgrade purchased successfully');
            } else {
                alert('Недостаточно монет для покупки улучшения.');
                console.log('Not enough coins to purchase click upgrade');
            }
            break;
        case 'auto-clicker':
            // Проверка наличия монет для улучшения автокликера
            if (coins >= autoClickerCost) {
                coins -= autoClickerCost; // Списываем стоимость улучшения
                autoClickerCount++; // Увеличиваем счетчик автокликеров
                autoClickerCost = Math.floor(autoClickerCost * 1.5); // Увеличиваем стоимость следующего автокликера
                updateDisplay(); // Обновляем отображение
                saveData(); // Сохраняем данные
                alert('Автокликер куплен! Теперь у вас ' + autoClickerCount + ' автокликер(ов).');
                console.log('Auto-clicker purchased successfully');
            } else {
                alert('Недостаточно монет для покупки автокликера.');
                console.log('Not enough coins to purchase auto-clicker');
            }
            break;
        default:
            console.log('Unknown upgrade ID:', upgradeId);
            break;
    }
    console.log('After purchase:', { coins, clickPower, clickUpgradeCost, autoClickerCount, autoClickerCost });
}

// Функция для расчета офлайн прогресса
function calculateOfflineProgress() {
    const currentTime = Date.now();
    const timeDiff = (currentTime - lastUpdateTime) / 1000; // разница в секундах
    const offlineClicks = autoClickerCount * clickPower * timeDiff;
    coins += offlineClicks;
    clicks += offlineClicks;
    console.log('Offline progress calculated:', { timeDiff, offlineClicks });
    lastUpdateTime = currentTime;
}

// Функция автокликера
function autoClick() {
    const clicksToAdd = autoClickerCount * clickPower;
    coins += clicksToAdd;
    clicks += clicksToAdd;
    updateDisplay();
    saveData();
    console.log('Auto-click performed:', { coins, clicks, autoClickerCount });
}

// Инициализация после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    calculateOfflineProgress();
    updateDisplay();
    
    // Привязка обработчика к изображению кликера
    const clickerImg = document.getElementById('clicker-img');
    if (clickerImg) {
        clickerImg.addEventListener('click', handleClick);
    }
    
    // Привязка обработчиков к кнопкам улучшений
    const upgradeButtons = document.querySelectorAll('#upgrades [upgrade-id]');
    upgradeButtons.forEach(button => {
        button.addEventListener('click', () => buyUpgrade(button.getAttribute('upgrade-id')));
    });

    // Запуск автокликера
    setInterval(autoClick, 1000);

    // Сохранение данных каждые 10 секунд
    setInterval(saveData, 10000);

    console.log('Initialization complete');
});
