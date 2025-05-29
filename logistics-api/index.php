<?php
require_once __DIR__ . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

header('Content-Type: application/json');

$method = $_SERVER['REQUEST_METHOD'];
$path   = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

$equipments = [
    ['id' => 1, 'name' => 'Bomba X1'],
    ['id' => 2, 'name' => 'Válvula V2'],
];

if ($method === 'GET' && $path === '/equipments') {
    echo json_encode($equipments);
    exit;
}

if ($method === 'POST' && $path === '/dispatch') {
    $data = json_decode(file_get_contents('php://input'), true);

    $url = getenv('RABBITMQ_URL');
    $parts = parse_url($url);

    $conn = new AMQPStreamConnection(
        $parts['host'],
        $parts['port'],
        $parts['user'],
        $parts['pass']
    );

    $ch = $conn->channel();
    $ch->queue_declare('logistics', false, true, false, false);

    $msg = new AMQPMessage(json_encode($data), ['delivery_mode' => 2]);
    $ch->basic_publish($msg, '', 'logistics');

    $ch->close();
    $conn->close();

    echo json_encode(['status' => 'dispatched']);
    exit;
}

http_response_code(404);
echo json_encode(['error' => 'not found']);
