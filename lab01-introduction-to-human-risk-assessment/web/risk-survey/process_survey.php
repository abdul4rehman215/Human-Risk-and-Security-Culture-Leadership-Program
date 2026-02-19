<?php
$db_path = '/home/ubuntu/human-risk-assessment/data/assessment.db';

function connectDb($db_path) {
    if (!file_exists($db_path)) {
        throw new Exception("Database not found at: " . htmlspecialchars($db_path));
    }
    $db = new SQLite3($db_path);
    $db->exec("PRAGMA foreign_keys = ON;");
    return $db;
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    try {
        $db = connectDb($db_path);

        $employee_id = trim($_POST['employee_id'] ?? '');
        $department = trim($_POST['department'] ?? '');
        $role = trim($_POST['role'] ?? '');
        $experience_years = (int)($_POST['experience_years'] ?? 0);

        if ($employee_id === '' || $department === '' || $role === '' || $experience_years <= 0) {
            throw new Exception("Missing or invalid participant information.");
        }

        $stmt = $db->prepare("
            INSERT INTO participants (employee_id, department, role, experience_years)
            VALUES (:employee_id, :department, :role, :experience_years)
        ");
        $stmt->bindValue(':employee_id', $employee_id, SQLITE3_TEXT);
        $stmt->bindValue(':department', $department, SQLITE3_TEXT);
        $stmt->bindValue(':role', $role, SQLITE3_TEXT);
        $stmt->bindValue(':experience_years', $experience_years, SQLITE3_INTEGER);
        $stmt->execute();

        echo "<h1>Thank You!</h1>";
        echo "<p>Your survey response has been recorded.</p>";

    } catch (Exception $e) {
        echo "<h1>Error</h1>";
        echo "<p>" . htmlspecialchars($e->getMessage()) . "</p>";
    }
}
?>
