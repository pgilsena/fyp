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

	<?php
	$conn = mysqli_connect('localhost','pippa','p1i2p3p4a5','packets')
	or die('Error connecting to MySQL server.');

	$sql = "SELECT proto, srcIP, destIP, conn_status, timestmp FROM packet_info ORDER BY timestmp DESC LIMIT 20";
	$result = mysqli_query($conn, $sql);

	echo "<div class='w3-container'>
        	<div class='page-header'>
            <h1>20 Most Recent IP Destinations</h1>
        	</div>
        <br>";

	if (mysqli_num_rows($result) > 0) {
		echo "<table class='table table-striped table-bordered'>";
		echo "<tr>
        	<th>#</th>
        	<th>Timestamp</th>
	        <th>Protocol</th>
	        <th>Source IP</th>
	        <th>Dest IP</th>
	        <th>Conn Status</th>
	        </tr>";

 		while($rowitem = mysqli_fetch_array($result)) {
		    echo "<tr>";
		    echo "<td>" . "</td>";
		    echo "<td>" . $rowitem['timestmp'] . "</td>";
		    echo "<td>" . $rowitem['proto'] . "</td>";
		    echo "<td>" . $rowitem['srcIP'] . "</td>";
		    echo "<td>" . $rowitem['destIP'] . "</td>";
		    echo "<td>" . $rowitem['conn_status'] . "</td>";
		    echo "</tr>";
		}
		echo "</table>"; //end table tag
	} else {
		echo "0 results";
	}

	mysql_close();
?>

</body>
</html>