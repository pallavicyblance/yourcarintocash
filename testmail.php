<?php
if(isset($_POST)){
    
    //print_r($_POST);

    $host = "localhost"; // Hostname or IP address of your database server
    $username = "carintocash1"; // Your database username
    $password = "zkY$$}_vtXO="; // Your database password
    $database = "carintocash1"; // The name of your database

    // Create a database connection
    $mysqli = new mysqli($host, $username, $password, $database);

    // Check the connection
    if ($mysqli->connect_error) {
        die("Connection failed: " . $mysqli->connect_error);
    }

    // Your SELECT query
    $query = "SELECT * FROM accepted_aps where id='".$_POST['record_id']."'";


    // Execute the query
    $result = $mysqli->query($query);

    // Check if the query was successful
    if (!$result) {
        die("Query failed: " . $mysqli->error);
    }

    // Process the query results
    while ($row = $result->fetch_assoc()) {
        
        $recipient = "cyblance.nigam@gmail.com";
    
        $subject = "User Accepted Offer ";
        
        $message .= "<p>Dear Admin,</p>". "\r\n";
        $message .= "<p>We are writing to inform you that a user has accepted an offer from our YourCarIntoCash platform. User has accepted offer for ".$row['year'].' '.$row['make'].' '.$row['model'].". The offer ID is #".$row['id']." and the offer amount is ".$row['revised_price']." </p>". "\r\n";
        $message .= "<p>Here are more details:</p>". "\r\n";

        // $message .= "<h3>User Details:</h3>";
        // $message .= "<table border='2'>";
        //     $message .= "<tr>";
        //         $message .= "<td>Offer ID: </td>";
        //         $message .= "<td>".$row['id']."</td>";
        //     $message .= "</tr>";
        //     $message .= "<tr>";
        //         $message .= "<td>Full name: </td>";
        //         $message .= "<td>".$row['fname']."</td>";
        //     $message .= "</tr>";
        //     $message .= "<tr>";
        //         $message .= "<td>Phone: </td>";
        //         $message .= "<td>".$row['phone']."</td>";
        //     $message .= "</tr>";
        //     $message .= "<tr>";
        //         $message .= "<td>Alternate phone: </td>";
        //         $message .= "<td>".$row['alternatephone']."</td>";
        //     $message .= "</tr>";
        //     $message .= "<tr>";
        //         $message .= "<td>Owner name: </td>";
        //         $message .= "<td>".$row['ownerfname']."</td>";
        //     $message .= "</tr>";
        //     $message .= "<tr>";
        //         $message .= "<td>Payee name: </td>";
        //         $message .= "<td>".$row['payeefname']."</td>";
        //     $message .= "</tr>";
        // $message .= "</table>";
        $message .= "<h3>Offer Details:  </h3>";
        $message .= "<table border='2'>";
            $message .= "<tr>";
                $message .= "<td>Year: </td>";
                $message .= "<td>".$row['year']."</td>";
            $message .= "</tr>";
            $message .= "<tr>";
                $message .= "<td>Make: </td>";
                $message .= "<td>".$row['make']."</td>";
            $message .= "</tr>";
            $message .= "<tr>";
                $message .= "<td>Model: </td>";
                $message .= "<td>".$row['model']."</td>";
            $message .= "</tr>";
            $message .= "<tr>";
                $message .= "<td>Mileage: </td>";
                $message .= "<td>".$row['mileage']."</td>";
            $message .= "</tr>";
            if( $row['damage1'] == 'MN'){ $d1 = 'Minor dent/Scratches'; }elseif($row['damage1'] == 'AO'){ $d1 = 'All Over'; }elseif($row['damage1'] == 'BN'){ $d1 = 'Burn'; }elseif($row['damage1'] == 'FR'){ $d1 = 'Front End'; }elseif($row['damage1'] == 'RE'){ $d1 = 'Rear End'; }elseif($row['damage1'] == 'SD'){ $d1 = 'Side Damage'; }elseif($row['damage1'] == 'TP'){ $d1 = 'Top/Roof'; }elseif($row['damage1'] == 'RR'){ $d1 = 'Rear End'; }else{ $d1 = 'Option Not Selected'; }
            $message .= "<tr>";
                $message .= "<td>Body damage: </td>";
                $message .= "<td>".$d1."</td>";
            $message .= "</tr>";
            if( $row['airbag'] == 'Y'){ $a1 = "The air bags are deployed"; }elseif($row['airbag'] == "N"){ $a1 ="Air bags aren't deployed"; }else{ $a1 ="Option Not Selected"; }
            $message .= "<tr>";
                $message .= "<td>Airbag: </td>";
                $message .= "<td>".$a1."</td>";
            $message .= "</tr>";
            if($row['drive']=='D'){ $d = 'It starts and drives'; }elseif($row['drive']=='S'){ $d = 'It starts but does not drive'; }elseif($row['drive']=='N'){ $d = "It doesn't start"; }else{ $d = ''; }
            $message .= "<tr>";
                $message .= "<td>Drive status: </td>";
                $message .= "<td>".$d."</td>";
            $message .= "</tr>";
            $message .= "<tr>";
                $message .= "<td>Mechanical issues: </td>";
                $message .= "<td>".$row['sdamage']."</td>";
            $message .= "</tr>";
            if($row['car_key']=='Y'){ $k = 'Yes, I have the key'; }elseif($row['car_key']=='N'){ $k = 'No, I do not have a key'; }else{ $k = ''; }
            $message .= "<tr>";
                $message .= "<td>Key: </td>";
                $message .= "<td>".$k."</td>";
            $message .= "</tr>";
            if($row['title']=='clean title'){ $t = 'Yes, I have a clean title'; }elseif($row['title']=='Salvage Rebuilt'){ $t = 'No, my title is branded (Salvage, rebuilt, lemon law, etc.)'; }elseif($row['title']=='Unknown'){ $t = "No, I don’t have a title"; }else{ $t = ''; }
            $message .= "<tr>";
                $message .= "<td>Title: </td>";
                $message .= "<td>".$t."</td>";
            $message .= "</tr>";
            if($row['fire_damage']=='no'){ $f = 'No, it has never had any fire or water damage '; }elseif($row['fire_damage']=='W'){ $f = 'Yes, it had fire or water damage '; }else{
                $f = ''; }
            $message .= "<tr>";
                $message .= "<td>Water or fire damage: </td>";
                $message .= "<td>".$f."</td>";
            $message .= "</tr>";
        $message .= "</table>";

        // $message .= "<h3>User Location Details: </h3>";
        // $message .= "<table border='2'>";
        //     $message .= "<tr>";
        //         $message .= "<td>Location name: </td>";
        //         $message .= "<td>".$row['locationname']."</td>";
        //     $message .= "</tr>";
        //     $message .= "<tr>";
        //         $message .= "<td>Street name: </td>";
        //         $message .= "<td>".$row['address1']."</td>";
        //     $message .= "</tr>";
        //     $message .= "<tr>";
        //         $message .= "<td>Address line 2: </td>";
        //         $message .= "<td>".$row['address2']."</td>";
        //     $message .= "</tr>";
        //     $message .= "<tr>";
        //         $message .= "<td>City: </td>";
        //         $message .= "<td>".$row['city']."</td>";
        //     $message .= "</tr>";
        //     $message .= "<tr>";
        //         $message .= "<td>State: </td>";
        //         $message .= "<td>".$row['state']."</td>";
        //     $message .= "</tr>";
        //     $message .= "<tr>";
        //         $message .= "<td>Zip: </td>";
        //         $message .= "<td>".$row['zip']."</td>";
        //     $message .= "</tr>";
        // $message .= "</table>";
        

        $message .= "<p>Thank you for your continued support in managing our platform effectively.</p>". "\r\n \r\n";
        $message .= "<p>Best regards,</p>". "\r\n";
        $message .= "<p>Your car into cash</p>". "\r\n";
        $message .= "<p><img src='https://yourcarintocash.com/dev-carcash/static/images/car-logo.png' alt='logo' width='69' height='51'></p>". "\r\n";
            
        //$message .= "</table>";
        $to = 'cyblance.nigam@gmail.com';
        $subject = 'User Accepted Offer';
        $from = 'ben@yourcarintocash.com';
 
        // To send HTML mail, the Content-type header must be set
        $headers  = 'MIME-Version: 1.0' . "\r\n";
        $headers .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n";
 
        // Create email headers
        $headers .= 'From: '.$from."\r\n".'Reply-To: '.$from."\r\n" .
        'X-Mailer: PHP/' . phpversion();
        if(mail($to, $subject, $message, $headers)){echo 1;}else{echo 2;}exit();}
    }

    // Close the database connection
    $mysqli->close();

    
?>