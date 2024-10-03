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

    if (!isset($input['uploader'])) {
        http_response_code(400);
        echo json_encode(['message' => 'Uploader is required']);
        return;
    }
    $uploader = $input['uploader'];
    $sql = "SELECT filename, url FROM Photos WHERE uploader = :uploader";
    $stmt = $pdo->prepare($sql);
    
    try {
        $stmt->execute(['uploader' => $uploader]);
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
        http_response_code(200);
        echo json_encode($result);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error fetching photos', 'error' => $e->getMessage()]);
    }
}

function handlePost($pdo, $input) {
    if(!isset($input['user'], $input['filename'], $input['url'])) {
        http_response_code(400);
        echo json_encode(['message' => 'User, URL and filename is required']);
    } else {
        http_response_code(400);
        echo json_encode(['message' => 'Invalid filename/URL value']);
    }

    $user = $input['user'];
    $url = $input['url'];
    $filename = $input['filename'];

    try {
        $stmt->execute(['user' => $user, 'filename' => $filename, 'url' => $url]);
        http_response_code(201);
        echo json_encode(['message' => 'Photo uploaded successfully']);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error uploading photo', 'error' => $e->getMessage()]);
    }
}

function handlePut($pdo, $input) {
    if (!isset($input['photo_id'])) {
        http_response_code(400);
        echo json_encode(['message' => 'Photo ID is required']);
        return;
    }

    $photo_id = (int)$input['photo_id'];
    $updates = [];
    $params = ['photo_id' => $photo_id];

    if (isset($input['filename'])) {
        $updates[] = 'filename = :filename';
        $params['filename'] = $filename;
    }

    if (isset($input['url'])) {
        $url = filter_var($input['url'], FILTER_SANITIZE_URL);
        if(!filter_var($url, FILTER_SANITIZE_URL)) {
            http_response_code(400);
            echo json_encode(['message' => 'Invalid URL format']);
            return;
        }
        $updates[] = 'url = :url';
        $params['url'] = $url;
    }

    if (empty($updates)) {
        http_response_code(400);
        echo json_encode(['message' => 'No valid fields provided for update']);
        return;
    }

    $sql = "UPDATE Photos SET " . implode(', ', $updates) . " WHERE photo_id = :photo_id";
    $stmt = $pdo->prepare($sql);
    try {
        $stmt->execute($params);
        if ($stmt->rowCount() > 0) {
            echo json_encode(['message' => 'Photo updated successfully']);
        } else {
            http_response_code(404);
            echo json_encode(['message' => 'Photo not found or no changes made']);
        }
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error updating photo', 'error' => $e->getMessage()]);
    }
}

function handleDelete($pdo, $input) {
    if (!isset($input['user_id'])) {
        http_response_code(400);
        echo json_encode(['message' => 'User ID is required']);
        return;
    }

    $photo_id = (int)$input['photo_id'];
    $sql     = "DELETE FROM Photos WHERE photo_id = :photo_id";
    $stmt    = $pdo->prepare($sql);

    try {
        $stmt->execute(['photo_id' => $photo_id]);
        if ($stmt->rowCount() > 0) {
            echo json_encode(['message' => 'Photo deleted successfully']);
        } else {
            http_response_code(404);
            echo json_encode(['message' => 'Photo not found']);
        }
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error deleting photo', 'error' => $e->getMessage()]);
    }
}
?>