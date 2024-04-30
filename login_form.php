<?php
function sanitize($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

function hashPassword($password) {
    return hash('sha256', $password);
}

function handleDataStorage($username, $hashedPassword){
    $data = array($username, $hashedPassword);
    $file = 'userdata.csv';

    // Check if file exists, if not, create it
    if (!file_exists($file)) {
        $fp = fopen($file, 'w');
        // Add header to CSV file
        fputcsv($fp, array('Username', 'Password'));
        fclose($fp);
    }

    // Open file in append mode
    $fp = fopen($file, 'a');

    // Write data to CSV file
    $success = fputcsv($fp, $data);

    // Close file
    fclose($fp);

    return $success;
}

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = sanitize($_POST['username']);
    $password = sanitize($_POST['password']);

    $hashedPassword = hashPassword($password);
    
    $success = handleDataStorage($username, $hashedPassword);
    if($success){
        echo "<p>Data saved successfully.</p>";
    } else {
        echo "<p>Data could not be saved successfully.</p>";

    }
}
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Form</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                form {
                    width: 300px;
                    margin: 0 auto;
                }
                input[type="text"], input[type="password"], input[type="submit"] {
                    width: 100%;
                    padding: 10px;
                    margin-top: 5px;
                    margin-bottom: 10px; 
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
            </style>
    </head>
    <body>

    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br>
        
        <input type="submit" value="Login">
    </form>

    </body>
</html>
