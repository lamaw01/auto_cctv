<?php
$servername = "172.21.3.25";
$username = "autocctv";
$password = "autocctv123";
$dbname = "autocctv";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM logs";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    echo "date: " . $row["date"]. " -ip " . $row["ip"]. " name: " . $row["name"]. " rebooted " . $row["rebooted"]. " nvr " . $row["nvr"]."<br>";
  }
} else {
  echo "0 results";
}
$conn->close();
?>