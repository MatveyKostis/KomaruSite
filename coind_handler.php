<?php
$file = 'coins.txt';

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Чтение количества монет
    $coins = file_get_contents($file);
    echo $coins;
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Обновление количества монет
    $coins = $_POST['coins'];
    file_put_contents($file, $coins);
    echo "OK";
}
?>