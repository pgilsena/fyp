<!DOCTYPE html>
<html>
<head>
<title>Packet Info</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="http://www.w3schools.com/lib/w3.css">
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
<!--script type="text/javascript" src="csvtotable.js" id="data"></script-->
</head>

<body>

<h1>Hi</h1>

<?php
    $conn = mysqli_connect('localhost','pippa','','packets')
 	or die('Error connecting to MySQL server.');

 	$sql = "SELECT proto, srcIP, destIP, conn_status, timestmp FROM packet_info ORDER BY timestmp DESC LIMIT 20";
 	$result = mysqli_query($conn, $sql);

 	if (mysqli_num_rows($result) > 0) {
 		while($row = mysqli_fetch_assoc($result)) {
 			echo "proto: " . $row["proto"] . ", source ip: " . $row["srcIP"] . ", dest ip: " . $row["destIP"] . ", connection status: " . $row["conn_status"] . "<br>";
 		}
 	} else {
 		echo "0 results";
 	}

    mysql_close();
?>
</body>
</html>