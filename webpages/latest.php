<!DOCTYPE html>
<html>
<head>
	<title>Latest</title>
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

	$sql = "SELECT proto, srcIP, destIP, conn_status, timestmp, sport, dport, pkt_count, dns_query, s_country, d_country, tcp_flag FROM packet_info ORDER BY timestmp DESC LIMIT 100";
	$result = mysqli_query($conn, $sql);

	echo "<div class='container'>
        	<div class='page-header'>
            	<h1>Latest Packet Activity <small>Uplink and Downlink</small></h1>
        	</div>
        </div>";

    echo "<div class='container'>
			<ul class='pager'>
				<li class='previous'><a href='http://34.249.128.106/'>Index</a></li>
		    	<li class='next'><a href='http://34.249.128.106/tcp.php'>Latest TCP Packets</a></li>
  			</ul>
		</div>";

	if (mysqli_num_rows($result) > 0) {
		echo "<div class='container'>
				<div class='table-responsive'>
	        		<table class='table table-striped table-bordered'>
			        	<thead>
					        <tr>
					        	<th>#</th>
					        	<th>Timestamp</th>
						        <th>Protocol</th>
						        <th>Source IP</th>
						        <th>Sport</th>
						        <th>Dest IP</th>
						        <th>Dport</th>
						        <th>DNS Query</th>
						        <th>Conn Status</th>
						        <th>Packet Count</th>
						        <th>Src Country</th>
						        <th>Dest Country</th>
						        <th>TCP Flag</th>
					        </tr>
			        	</thead>";

	    $counter = 1;
 		while($rowitem = mysqli_fetch_array($result)) {
		    echo "<tr>";
		    echo "<td>" . $counter . "</td>";
		    echo "<td>" . $rowitem['timestmp'] . "</td>";
		    echo "<td>" . $rowitem['proto'] . "</td>";
		    echo "<td>" . $rowitem['srcIP'] . "</td>";
		    echo "<td>" . $rowitem['sport'] . "</td>";
		    echo "<td>" . $rowitem['destIP'] . "</td>";
		    echo "<td>" . $rowitem['dport'] . "</td>";
		    echo "<td>" . $rowitem['dns_query'] . "</td>";
		    echo "<td>" . $rowitem['conn_status'] . "</td>";
		    echo "<td>" . $rowitem['pkt_count'] . "</td>";
		    echo "<td>" . $rowitem['s_country'] . "</td>";
		    echo "<td>" . $rowitem['d_country'] . "</td>";
		    echo "<td>" . $rowitem['tcp_flag'] . "</td>";
		    echo "</tr>";
		    $counter = $counter + 1;
		}
		echo "</table></div></div>";
	} else {
		echo "0 results";
	}

	echo "<div class='container'>
			<ul class='pager'>
				<li class='previous'><a href='http://34.249.128.106/'>Home</a></li>
		    	<li class='next'><a href='http://34.249.128.106/tcp.php'>Latest TCP Packets</a></li>
  			</ul>
		</div>";

	mysql_close();
?>

</body>
</html>