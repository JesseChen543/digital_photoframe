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
        handlePost($pdo, $input);
        break;
    case 'PUT':
        handlePut($pdo, $input);
        break;
    case 'DELETE':
        handleDelete($pdo, $input);
        break;
    default:
        http_response_code(405);
        echo json_encode(['message' => 'Method Not Allowed']);
        break;
}

function handleGet($pdo, $input) {

    $user_id = $input['user_id'];
    $sql = "SELECT first_name, status FROM Users WHERE user_id = :user_id";
    $stmt = $pdo->prepare($sql);

    try {
        $stmt->execute(['user_id' => $user_id]);
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
        http_response_code(200);
        echo json_encode($result);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error fetching users', 'error' => $e->getMessage()]);
    }
}

function handlePost($pdo, $input) {
    if (!isset($input['email'], $input['password'])) {
        http_response_code(400);
        echo json_encode(['message' => 'Email and password are required']);
        return;
    }
    $first_name = isset($input['first_name']) ? $input['first_name'] : 'No name';
    $email    = filter_var($input['email'], FILTER_SANITIZE_EMAIL);
    $password = $input['password'];
    $status   = isset($input['status']) ? $input['status'] : 'Chilling'; // Use default if not provided

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode(['message' => 'Invalid email format']);
        return;
    }

    $validStatuses = ['Chilling', 'Occupied', 'Do Not Disturb'];
    if (!in_array($status, $validStatuses)) {
        http_response_code(400);
        echo json_encode(['message' => 'Invalid status value']);
        return;
    }

    $passwordHash = password_hash($password, PASSWORD_DEFAULT);

    $sql  = "INSERT INTO Users (first_name, email, password, status) VALUES (:first_name, :email, :password, :status)";
    $stmt = $pdo->prepare($sql);

    try {
        $stmt->execute(['first_name' => $first_name, 'email' => $email, 'password' => $passwordHash, 'status' => $status]);
        http_response_code(201);
        echo json_encode(['message' => 'User created successfully']);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error creating user', 'error' => $e->getMessage()]);
    }
}

function handlePut($pdo, $input) {
    if (!isset($input['user_id'])) {
        http_response_code(400);
        echo json_encode(['message' => 'User ID is required']);
        return;
    }

    $user_id = (int)$input['user_id'];
    $updates = [];
    $params  = ['user_id' => $user_id];

    if (isset($input['email'])) {
        $email = filter_var($input['email'], FILTER_SANITIZE_EMAIL);
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            http_response_code(400);
            echo json_encode(['message' => 'Invalid email format']);
            return;
        }
        $updates[]       = 'email = :email';
        $params['email'] = $email;
    }

    if (isset($input['password'])) {
        $passwordHash        = password_hash($input['password'], PASSWORD_DEFAULT);
        $updates[]           = 'password = :password';
        $params['password']  = $passwordHash;
    }

    if (isset($input['status'])) {
        $validStatuses = ['Chilling', 'Occupied', 'Do Not Disturb'];
        if (!in_array($input['status'], $validStatuses)) {
            http_response_code(400);
            echo json_encode(['message' => 'Invalid status value']);
            return;
        }
        $updates[]        = 'status = :status';
        $params['status'] = $input['status'];
    }

    if (empty($updates)) {
        http_response_code(400);
        echo json_encode(['message' => 'No valid fields provided for update']);
        return;
    }

    $sql  = "UPDATE Users SET " . implode(', ', $updates) . " WHERE user_id = :user_id";
    $stmt = $pdo->prepare($sql);

    try {
        $stmt->execute($params);
        if ($stmt->rowCount() > 0) {
            echo json_encode(['message' => 'User updated successfully']);
        } else {
            http_response_code(404);
            echo json_encode(['message' => 'User not found or no changes made']);
        }
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error updating user', 'error' => $e->getMessage()]);
    }
}

function handleDelete($pdo, $input) {
    if (!isset($input['user_id'])) {
        http_response_code(400);
        echo json_encode(['message' => 'User ID is required']);
        return;
    }

    $user_id = (int)$input['user_id'];
    $sql     = "DELETE FROM Users WHERE user_id = :user_id";
    $stmt    = $pdo->prepare($sql);

    try {
        $stmt->execute(['user_id' => $user_id]);
        if ($stmt->rowCount() > 0) {
            echo json_encode(['message' => 'User deleted successfully']);
        } else {
            http_response_code(404);
            echo json_encode(['message' => 'User not found']);
        }
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error deleting user', 'error' => $e->getMessage()]);
    }
}
?>
