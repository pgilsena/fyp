<!DOCTYPE html>
<html>
<head>
	<title>DNS Queries</title>
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

	$dns = "SELECT dns_query, count(1) as Total from packet_info GROUP BY dns_query order by Total desc";
	$dns_result = mysqli_query($conn, $dns);

	echo "<div class='w3-container'>
        	<div class='page-header'>
            <h1>DNS Queries<small></small></h1>
        	</div>
        <br>";

	if (mysqli_num_rows($dns_result) > 0) {
		echo "<table class='table table-striped table-bordered'>";
		echo "<tr>
        	<th>#</th>
        	<th>Destination Country</th>
	        <th>Count</th>
	        </tr>";

	    $counter = 1;
 		while($rowitem = mysqli_fetch_array($dns_result) and $counter<100) {
		    echo "<tr>";
		    echo "<td>" . $counter . "</td>";
		    echo "<td>" . $rowitem['dns_query'] . "</td>";
		    echo "<td>" . $rowitem['Total'] . "</td>";
		    echo "</tr>";
		    $counter = $counter + 1;
		}
		echo "</table>"; //end table tag
	} else {
		echo "0 results";
	}

	mysql_close();
?>

</body>
</html>