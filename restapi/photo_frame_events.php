<?php
header("Content-Type: application/json");
include 'db.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method == 'POST' && isset($_REQUEST['_method'])) {
    $method = strtoupper($_REQUEST['_method']);
}

$input = json_decode(file_get_contents('php://input'), true);

switch ($method) {
    case 'GET':
        handleGet($pdo, $input);
        break;
    case 'POST':
        http_response_code(405);
        echo json_encode(['message' => 'Method Not Allowed']);
        break;
    case 'PUT':
        http_response_code(405);
        echo json_encode(['message' => 'Method Not Allowed']);
        break;
    case 'DELETE':
        http_response_code(405);
        echo json_encode(['message' => 'Method Not Allowed']);
        break;
    default:
        http_response_code(405);
        echo json_encode(['message' => 'Method Not Allowed']);
        break;
}

function handleGet($pdo, $input) {

    if (!isset($input['user'])) {
        http_response_code(400);
        echo json_encode(['message' => 'User is required']);
        return;
    }
    $user = $input['user'];
    $sql = "SELECT event_name, start_time, end_time, location, description, privacy, story, users_attending FROM Events JOIN Event_users ON event_id = event WHERE user=:user AND privacy = 'Not Private'";
    $stmt = $pdo->prepare($sql);

    try {
        $stmt->execute(['user' => $user]);
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
        http_response_code(200);
        echo json_encode($result);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error fetching events', 'error' => $e->getMessage()]);
    }
}
?>