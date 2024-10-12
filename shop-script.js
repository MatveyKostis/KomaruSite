// Инициализация переменных
let coins = 0;
let clicks = 0;
let clickPower = 1;
let clickUpgradeCost = 200;

// Функция для сохранения данных в localStorage
function saveData() {
    localStorage.setItem('komaruCoins', coins);
    localStorage.setItem('komaruClicks', clicks);
    localStorage.setItem('komaruClickPower', clickPower);
    localStorage.setItem('komaruClickUpgradeCost', clickUpgradeCost);
    console.log('Data saved:', { coins, clicks, clickPower, clickUpgradeCost });
}

// Функция для загрузки данных из localStorage
function loadData() {
    coins = parseInt(localStorage.getItem('komaruCoins')) || 0;
    clicks = parseInt(localStorage.getItem('komaruClicks')) || 0;
    clickPower = parseInt(localStorage.getItem('komaruClickPower')) || 1;
    clickUpgradeCost = parseInt(localStorage.getItem('komaruClickUpgradeCost')) || 200;
    console.log('Data loaded:', { coins, clicks, clickPower, clickUpgradeCost });
}

// Функция для обновления отображения монет и кликов
function updateDisplay() {
    const coinsElement = document.getElementById('coins');
    const countElement = document.getElementById('count');
    const upgradeCostElement = document.getElementById('click-upgrade-cost');

    if (coinsElement) coinsElement.textContent = coins;
    if (countElement) countElement.textContent = clicks;
    if (upgradeCostElement) upgradeCostElement.textContent = clickUpgradeCost;

    console.log('Display updated:', { coins, clicks, clickUpgradeCost });
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
    console.log('Before purchase:', { coins, clickPower, clickUpgradeCost });

    switch(upgradeId) {
        case 'click-upgrade':
            if (coins >= clickUpgradeCost) {
                coins -= clickUpgradeCost;
                clickPower *= 2;
                clickUpgradeCost *= 2;
                updateDisplay();
                saveData();
                alert('Улучшение куплено! Теперь каждый клик приносит в 2 раза больше монет.');
                console.log('Upgrade purchased successfully');
                console.log('After purchase:', { coins, clickPower, clickUpgradeCost });
            } else {
                alert('Недостаточно монет для покупки улучшения.');
                console.log('Not enough coins to purchase upgrade');
            }
            break;
        // Здесь можно добавить другие улучшения
    }
}

// Инициализация после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    loadData();
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

    console.log('Initialization complete');
});