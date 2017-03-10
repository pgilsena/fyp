<!DOCTYPE html>
<html>
<head>
	<title>Countries</title>
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

	$dest = "SELECT d_country, count(1) as Total from packet_info GROUP BY d_country order by Total desc";
	$dst_result = mysqli_query($conn, $dest);

	$src = "SELECT s_country, count(1) as Total from packet_info GROUP BY s_country order by Total desc";
	$src_result = mysqli_query($conn, $src);

	echo "<div class='w3-container'>
        	<div class='page-header'>
            <h1>Packet Counts per Country <small>Source and Destination</small></h1>
        	</div>
        <br>";

	if (mysqli_num_rows($dst_result) > 0) {
		echo "<table class='table table-striped table-bordered'>";
		echo "<tr>
        	<th>#</th>
        	<th>Destination Country</th>
	        <th>Count</th>
	        </tr>";

	    $counter = 1;
 		while($rowitem = mysqli_fetch_array($dst_result)) {
		    echo "<tr>";
		    echo "<td>" . $counter . "</td>";
		    echo "<td>" . $rowitem['d_country'] . "</td>";
		    echo "<td>" . $rowitem['Total'] . "</td>";
		    echo "</tr>";
		    $counter = $counter + 1;
		}
		echo "</table>"; //end table tag
	} else {
		echo "0 results";
	}

	echo "<br>";

	if (mysqli_num_rows($src_result) > 0) {
		echo "<table class='table table-striped table-bordered'>";
		echo "<tr>
        	<th>#</th>
        	<th>Source Country</th>
	        <th>Count</th>
	        </tr>";

	    $counter = 1;
 		while($rowitem = mysqli_fetch_array($src_result)) {
		    echo "<tr>";
		    echo "<td>" . $counter . "</td>";
		    echo "<td>" . $rowitem['s_country'] . "</td>";
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