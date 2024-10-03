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

function validateDate($date, $format = 'Y-m-d H:i:s')
{
    $d = DateTime::createFromFormat($format, $date);
    return $d && $d->format($format) == $date;
}
//Only for app
function handleGet($pdo, $input) {

    if (!isset($input['user'])) {
        http_response_code(400);
        echo json_encode(['message' => 'User is required']);
        return;
    }

    $user = $input['user'];
    $sql = "SELECT event_name, start_time, end_time, location, description, privacy, story, users_attending FROM Events JOIN Event_users ON event_id = event WHERE user = :user";
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

function handlePost($pdo, $input) {
    if (!isset($input['event_name'], $input['user'], $input['start_time'], $input['end_time'])) {
        http_response_code(400);
        echo json_encode(['message' => 'Event name, user, start time and end time are required']);
        return;
    }

    $event_name = $input['event_name'];
    $user = $input['user'];
    if(validateDate($input['start_time'])) {
        $start_time = $input['start_time'];
    } else {
        http_response_code(400);
        echo json_encode(['message' => 'Invalid date value']);
    }

    if(validateDate($input['end_time'])) {
        $end_time = $input['end_time'];
    } else {
        http_response_code(400);
        echo json_encode(['message' => 'Invalid date value']);
    }

    $location = isset($input['location']) ? $input['location'] : NULL;
    $description = isset($input['description']) ? $input['description'] : NULL;
    $privacy = isset($input['privacy']) ? $input['privacy'] : 'Not Private';
    $story = isset($input['story']) ? $input['story'] : NULL;
    $repeat_event = isset($input['repeat_event']) ? $input['repeat_event'] : 'No Repeat';
    
    $validPrivacy = ['Private', 'Not Private'];
    if (!in_array($privacy, $validPrivacy)) {
        http_response_code(400);
        echo json_encode(['message' => 'Invalid privacy value']);
        return;
    }

    $validRepeat = ['No Repeat','Daily','Weekly','Monthly','Yearly'];
    if (!in_array($repeat_event, $validRepeat)) {
        http_response_code(400);
        echo json_encode(['message' => 'Invalid repeat value']);
        return;
    }

    $sql = "INSERT INTO Events (event_name, user, start_time, end_time, location, description, privacy, story, repeat_event) VALUES (:event_name, :user, :start_time, :end_time, :location, :description, :privacy, :story, :repeat_event)";
    $stmt = $pdo->prepare($sql);

    try {
        $stmt->execute(['event_name' => $event_name, 'user' => $user, 'start_time' => $start_time, 'end_time' => $end_time, 'location' => $location, 'description' => $description, 'privacy' => $privacy, 'story' => $story, 'repeat_event' => $repeat_event]);
        http_response_code(201);
        echo json_encode(['message' => 'Event created successfully']);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error creating event', 'error' => $e->getMessage()]);
    }
}

function handlePut($pdo, $input) {
    if (!isset($input['event_id'])) {
        http_response_code(400);
        echo json_encode(['message' => 'Event ID is required']);
        return;
    }

    $event_id = (int)$input['event_id'];
    $updates = [];
    $params  = ['event_id' => $event_id];

    if (isset($input['event_name'])) {
        $updates[] = 'event_name = :event_name';
        $params['event_name'] = $input['event_name'];
    }

    if (isset($input['start_time'])) {
        if(validateDate($input['start_time'])) {
            $updates[] = 'start_time = :start_time';
            $params['start_time'] = $input['start_time'];
        } else {
            http_response_code(400);
            echo json_encode(['message' => 'Invalid date value']);
        }
    }

    if (isset($input['end_time'])) {
        if(validateDate($input['end_time'])) {
            $updates[] = 'end_time = :end_time';
            $params['end_time'] = $input['end_time'];
        } else {
            http_response_code(400);
            echo json_encode(['message' => 'Invalid date value']);
        }
    }

    if (isset($input['location'])) {
        $updates[] = 'location = :location';
        $params['location'] = $input['location'];
    }

    if (isset($input['description'])) {
        $updates[] = 'description = :description';
        $params['description'] = $input['description'];
    }

    if (isset($input['privacy'])) {
        $validPrivacy = ['Private', 'Not Private'];
        if (!in_array($privacy, $validPrivacy)) {
            http_response_code(400);
            echo json_encode(['message' => 'Invalid privacy value']);
            return;
        }
        $updates[] = 'privacy = :privacy';
        $params['privacy'] = $input['privacy'];
    }

    if (isset($input['story'])) {
        $updates[] = 'story = :story';
        $params['story'] = $input['story'];
    }

    if (isset($input['repeat_event'])) {
        $validRepeat = ['No Repeat','Daily','Weekly','Monthly','Yearly'];
        if (!in_array($repeat_event, $validRepeat)) {
            http_response_code(400);
            echo json_encode(['message' => 'Invalid repeat value']);
            return;
        }
        $updates[] = 'repeat_event = :repeat_event';
        $params['repeat_event'] = $input['repeat_event'];
    }

    if (empty($updates)) {
        http_response_code(400);
        echo json_encode(['message' => 'No valid fields provided for update']);
        return;
    }

    $sql  = "UPDATE Events SET " . implode(', ', $updates) . " WHERE event_id = :event_id";
    $stmt = $pdo->prepare($sql);

    try {
        $stmt->execute($params);
        if ($stmt->rowCount() > 0) {
            echo json_encode(['message' => 'Event updated successfully']);
        } else {
            http_response_code(404);
            echo json_encode(['message' => 'Event not found or no changes made']);
        }
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error updating event', 'error' => $e->getMessage()]);
    }
}

function handleDelete($pdo, $input) {
    if (!isset($input['event_id'])) {
        http_response_code(400);
        echo json_encode(['message' => 'Event ID is required']);
        return;
    }

    $event_id = (int)$input['event_id'];
    $sql = "DELETE FROM Events WHERE event_id = :event_id";
    $stmt = $pdo->prepare($sql);

    try {
        $stmt->execute(['event_id' => $event_id]);
        if ($stmt->rowCount() > 0) {
            echo json_encode(['message' => 'Event deleted successfully']);
        } else {
            http_response_code(404);
            echo json_encode(['message' => 'Event not found']);
        }
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['message' => 'Error deleting event', 'error' => $e->getMessage()]);
    }
}
?>