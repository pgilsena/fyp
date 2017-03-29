<!DOCTYPE html>
<html>
<head>
	<title>Trackers</title>
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
	$conn = mysqli_connect('localhost','pippa','','packets')
	or die('Error connecting to MySQL server.');


	$tkr_query = "SELECT packet_info.srcIP, packet_info.destIP, packet_info.timestmp, packet_info.dns_query, packet_info.proto, packet_info.s_country, packet_info.d_country FROM packet_info WHERE packet_info.timestmp > '2017-01-01' AND EXISTS (SELECT tkr_ips.ip FROM tkr_ips WHERE tkr_ips.ip LIKE CONCAT(packet_info.srcIP, '%') OR tkr_ips.ip LIKE CONCAT(packet_info.destIP, '%')) ORDER BY packet_info.timestmp DESC LIMIT 100";

	$tkr_result = mysqli_query($conn, $tkr_query);

	echo "<div class='container'>
        	<div class='page-header'>
            <h1>Trackers</h1>
        	</div>
        	</div>
        <br>";

	if (mysqli_num_rows($tkr_result) > 0) {
        echo "<div class='container'>
        	<table class='table table-striped'>
	        	<thead>
			        <tr>
			        	<th>#</th>
			        	<th>Time</th>
			        	<th>Protocol</th>
			        	<th>Source IP</th>
			        	<th>Dest IP</th>
			        	<th>DNS</th>
			        	<th>Dest Country</th>
			        	<th>Src Country</th>
			        </tr>
	        	</thead>
        	";

        $counter = 1;

        while($rowitem = mysqli_fetch_array($tkr_result)) {
		    echo "<tr>";
			    echo "<td>" . $counter . "</td>";
			    echo "<td>" . $rowitem['timestmp'] . "</td>";
			    echo "<td>" . $rowitem['proto'] . "</td>";
			    echo "<td>" . $rowitem['srcIP'] . "</td>";
			    echo "<td>" . $rowitem['destIP'] . "</td>";
			    echo "<td>" . $rowitem['dns_query'] . "</td>";
			    echo "<td>" . $rowitem['d_country'] . "</td>";
			    echo "<td>" . $rowitem['s_country'] . "</td>";
			echo "</tr>";
			$counter = $counter + 1;
		}
		echo "</table";
	} else {
		echo "0 tracker results";
	}

	mysql_close();
?>

</body>
</html>