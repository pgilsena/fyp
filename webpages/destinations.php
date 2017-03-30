<!DOCTYPE html>
<html>
<head>
	<title>Destinations</title>
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

	$src = "SELECT destIP, count(1) as Total from packet_info GROUP BY destIP order by Total desc LIMIT 100";
	$src_result = mysqli_query($conn, $src);

	echo "<div class='container'>
        	<div class='page-header'>
            	<h1>Uplink</h1>
        	</div>
        </div>";

    echo "<div class='container'>
			<ul class='pager'>
				<li class='previous'><a href='http://34.249.128.106/sources.php'>Top Packet Sources</a></li>
		    	<li class='next'><a href='http://34.249.128.106/'>Home</a></li>
  			</ul>
		</div>";

	if (mysqli_num_rows($src_result) > 0) {
		echo "<div class='container'>
				<div class='table-responsive'>
	        		<table class='table table-striped'>
			        	<thead>
					        <tr>
					        	<th>#</th>
					        	<th>Destination</th>
					        	<th>Count</th>
					        </tr>
			        	</thead>";

		$counter = 1;

 		while($rowitem = mysqli_fetch_array($src_result)) {
		    echo "<tr>";
			    echo "<td>" . $counter . "</td>";
			    echo "<td>" . $rowitem['destIP'] . "</td>";
			    echo "<td>" . $rowitem['Total'] . "</td>";
		    echo "</tr>";
		    $counter = $counter + 1;
		}
		echo "</table></div></div>";
	} else {
		echo "0 results";
	}

	echo "<div class='container'>
			<ul class='pager'>
				<li class='previous'><a href='http://34.249.128.106/sources.php'>Top Packet Sources</a></li>
		    	<li class='next'><a href='http://34.249.128.106/'>Home</a></li>
  			</ul>
		</div>";

	mysql_close();
?>

</body>
</html>