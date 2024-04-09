<?php


//if(isset($_POST)){
    
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
    
    //
    $query1 = "SELECT * FROM admin where email_noti='yes'";


    // Execute the query
    $result1 = $mysqli->query($query1);

    // Check if the query was successful
    if (!$result1) {
        die("Query failed: " . $mysqli->error);
    }
    
    //
    
    
    $message = '';
    while ($row = $result->fetch_assoc()) {
        $message .= "<html lang='en-US'>"."\r\n";
            $message .= "<head>"."\r\n";
                $message .= "<title>New Account Email Template</title>"."\r\n";
            $message .= "</head>"."\r\n";
            $message .= "<body marginheight='0' topmargin='0' marginwidth='0' style='margin: 0px; background-color: #f2f3f8; padding: 50px 0;font-family: sans-serif;' leftmargin='0'>"."\r\n";
                $message .= "<table cellspacing='0' border='0' cellpadding='0' width='100%' bgcolor='#f2f3f8'>"."\r\n";
                    $message .= "<tr>"."\r\n";
                        $message .= "<td colspan='2' style='text-align:center;padding-bottom:15px;'>"."\r\n";
                            $message .= "<a href='#' title='logo' target='_blank'>"."\r\n";
                                $message .= "<img width='92' src='https://yourcarintocash.com/wp-content/uploads/2022/06/car-logo.png' title='logo' alt='logo'>"."\r\n";
                            $message .= "</a>"."\r\n";
                        $message .= "</td>"."\r\n";
                    $message .= "</tr>"."\r\n";
                    $message .= "<tr>"."\r\n";
                        $message .= "<td>"."\r\n";
                           $message .= "<table width='100%' border='0' align='center' cellpadding='0' cellspacing='5' style='max-width:670px; background:#fff; border-radius:3px; text-align:start;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06); padding: 40px 20px 20px; border-top: 5px solid #22b573; font-size:14px; font-family:sans-serif;'>"."\r\n";
                              
                              
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td colspan='2'>"."\r\n";
                                        $message .= "<h1 style='color:#1e1e2d; font-weight:500; margin:0;font-size:14px;font-family:Rubik,sans-serif;'>Dear Admin</h1>"."\r\n";
                                        $message .= "<p style='font-size:14px; color:#455056; margin:8px 0 0; line-height:24px;'>"."\r\n";
                                        $message .= "We are writing to inform you that a user has accepted an offer from our YourCarIntoCash platform."."\r\n"; 
                                        $message .= "User has accepted offer for ".$row['year']." ".$row['make']." ".$row['model']."\r\n";
                                        $message .= "The offer ID is #YC".$row['id']." and the offer amount is <strong>$".$row['revised_price'].".</strong></p>"."\r\n";
                                    $message .= "</td>"."\r\n";
                                $message .= "</tr>"."\r\n";
                                $message .= "<tr>"."\r\n";
                                    $message .= "<th style='text-align: start; padding: 20px 0px 5px 0px;' colspan='2'><strong>User Details:</strong></th>"."\r\n";
                                $message .= "</tr>"."\r\n";
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td style='width: 50%;'><strong>Offer ID:</strong> #YC".$row['id']."</td>"."\r\n";
                                    $message .= "<td style='width: 50%;'><strong>Full name:</strong>". $row['fname']."</td>"."\r\n";
                                    
                                $message .= "</tr>"."\r\n";
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Payee amount:</strong> $".$row['revised_price']."</td>"."\r\n";
                                    $message .= "<td style='width: 50%;'><strong>Phone:</strong> ".$row['phone']."</td>"."\r\n";
                                    
                                    
                                $message .= "</tr>"."\r\n";
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Payee name:</strong> ".$row['payeefname']."</td>"."\r\n";
                                    $message .= "<td><strong>Alternate phone:</strong> ".$row['alternatephone']."</td>"."\r\n";
                                    
                                $message .= "</tr>"."\r\n";
        
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<th style='text-align: start; padding: 20px 0px 5px 0px;' colspan='2'><strong>Offer Details:</strong></th>"."\r\n";
                                $message .= "</tr>"."\r\n";
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Year</strong>: ".$row['year']."</td>"."\r\n";
                                    $message .= "<td><strong>Mileage</strong>: ".$row['mileage']."</td>"."\r\n";
                                $message .= "</tr>"."\r\n";
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Make</strong>: ".$row['make']."</td>"."\r\n";
                                    if( $row['damage1'] == 'MN'){
                                        $d1 = 'Minor dent/Scratches';
                                    }elseif($row['damage1'] == 'AO'){
                                        $d1 = 'All Over';
                                    }elseif($row['damage1'] == 'BN'){
                                        $d1 = 'Burn';
                                    }elseif($row['damage1'] == 'FR'){
                                        $d1 = 'Front End';
                                    }elseif($row['damage1'] == 'RE'){
                                        $d1 = 'Rear End';
                                    }elseif($row['damage1'] == 'SD'){
                                        $d1 = 'Side Damage';
                                    }elseif($row['damage1'] == 'TP'){
                                        $d1 = 'Top/Roof';
                                    }elseif($row['damage1'] == 'RR'){
                                       $d1 = 'Rear End';
                                    }else{
                                       $d1 = 'Option Not Selected';
                                    }
                                    $message .= "<td><strong>Body damage</strong>: ".$d1."</td>"."\r\n";
                                $message .= "</tr>"."\r\n";
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Model</strong>: ".$row['model']."</td>"."\r\n";
                                    if( $row['airbag'] == 'Y'){
                                        $a1 = "The air bags are deployed";
                                    }elseif($row['airbag'] == "N"){
                                        $a1 ="Air bags aren't deployed";
                                    }else{
                                        $a1 ="Option Not Selected";
                                    }
                                    $message .= "<td><strong>Airbag:</strong> ".$a1."</td>"."\r\n";
                                $message .= "</tr>"."\r\n";
                                
                                //
                                //if($row['drive']=='D'){
                                if($row['drive']=='D'){
                                    $d = 'It starts and drives';
                                }elseif($row['drive']=='S'){
                                    $d = 'It starts but does not drive';
                                }elseif($row['drive']=='N'){
                                    $d = "It doesn't start";
                                }else{
                                    $d = '';
                                }
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Drive status</strong>: ".$d."</td>"."\r\n";
                                    
                                    $message .= "<td><strong>Mechanical issues:</strong> ".$row['sdamage']."</td>"."\r\n";
                                $message .= "</tr>"."\r\n";
                                
                                if($row['car_key']=='Y'){
                                    $k = 'Yes, I have the key';
                                }elseif($row['car_key']=='N'){
                                    $k = 'No, I do not have a key';
                                }else{
                                    $k = '';
                                }
                                
                                if($row['title']=='clean title'){
                                    $t = 'Yes, I have a clean title';
                                }elseif($row['title']=='Salvage Rebuilt'){
                                    $t = 'No, my title is branded (Salvage, rebuilt, lemon law, etc.)';
                                }elseif($row['title']=='Unknown'){
                                    $t = "No, I don’t have a title";
                                }else{
                                    $t = '';
                                }
                                
                                if($row['fire_damage']=='no'){
                                    $f = 'No, it has never had any fire or water damage ';
                                }elseif($row['fire_damage']=='W'){
                                    $f = 'Yes, it had fire or water damage ';
                                }else{
                                    $f = '';
                                }
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Key</strong>: ".$k."</td>"."\r\n";
                                    
                                    $message .= "<td><strong>Title:</strong> ".$t."</td>"."\r\n";
                                $message .= "</tr>"."\r\n";
                                if($row['fire_damage']=='no'){
                                    $f = 'No, it has never had any fire or water damage ';
                                }elseif($row['fire_damage']=='W'){
                                    $f = 'Yes, it had fire or water damage ';
                                }else{
                                    $f = '';
                                }
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Water or fire damage</strong>: ".$f."</td>"."\r\n";
                                    $message .= "<td></td>"."\r\n";
                                $message .= "</tr>"."\r\n";
                                
                                //
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<th style='text-align: start; padding: 20px 0px 5px 0px;' colspan='2'>User Location Details</th>"."\r\n";
                                $message .= "</tr>"."\r\n";
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Location name:</strong> ".$row['locationname']."</td>"."\r\n";
                                    $data = [
                                        ['id' => 'AL', 'name' => 'Alabama'],
                                        ['id' => 'AK', 'name' => 'Alaska'],
                                        ['id' => 'AZ', 'name' => 'Arizona'],
                                        ['id' => 'AR', 'name' => 'Arkansas'],
                                        ['id' => 'CA', 'name' => 'California'],
                                        ['id' => 'CO', 'name' => 'Colorado'],
                                        ['id' => 'CT', 'name' => 'Connecticut'],
                                        ['id' => 'DE', 'name' => 'Delaware'],
                                        ['id' => 'FL', 'name' => 'Florida'],
                                        ['id' => 'GA', 'name' => 'Georgia'],
                                        ['id' => 'HI', 'name' => 'Hawaii'],
                                        ['id' => 'ID', 'name' => 'Idaho'],
                                        ['id' => 'IL', 'name' => 'Illinois'],
                                        ['id' => 'IN', 'name' => 'Indiana'],
                                        ['id' => 'IA', 'name' => 'Iowa'],
                                        ['id' => 'KS', 'name' => 'Kansas'],
                                        ['id' => 'KY', 'name' => 'Kentucky'],
                                        ['id' => 'LA', 'name' => 'Louisiana'],
                                        ['id' => 'ME', 'name' => 'Maine'],
                                        ['id' => 'MD', 'name' => 'Maryland'],
                                        ['id' => 'MA', 'name' => 'Massachusetts'],
                                        ['id' => 'MI', 'name' => 'Michigan'],
                                        ['id' => 'MN', 'name' => 'Minnesota'],
                                        ['id' => 'MS', 'name' => 'Mississippi'],
                                        ['id' => 'MO', 'name' => 'Missouri'],
                                        ['id' => 'MT', 'name' => 'Montana'],
                                        ['id' => 'NE', 'name' => 'Nebraska'],
                                        ['id' => 'NV', 'name' => 'Nevada'],
                                        ['id' => 'NH', 'name' => 'New Hampshire'],
                                        ['id' => 'NJ', 'name' => 'New Jersey'],
                                        ['id' => 'NM', 'name' => 'New Mexico'],
                                        ['id' => 'NY', 'name' => 'New York'],
                                        ['id' => 'NC', 'name' => 'North Carolina'],
                                        ['id' => 'ND', 'name' => 'North Dakota'],
                                        ['id' => 'OH', 'name' => 'Ohio'],
                                        ['id' => 'OK', 'name' => 'Oklahoma'],
                                        ['id' => 'OR', 'name' => 'Oregon'],
                                        ['id' => 'PA', 'name' => 'Pennsylvania'],
                                        ['id' => 'RI', 'name' => 'Rhode Island'],
                                        ['id' => 'SC', 'name' => 'South Carolina'],
                                        ['id' => 'SD', 'name' => 'South Dakota'],
                                        ['id' => 'TN', 'name' => 'Tennessee'],
                                        ['id' => 'TX', 'name' => 'Texas'],
                                        ['id' => 'UT', 'name' => 'Utah'],
                                        ['id' => 'VT', 'name' => 'Vermont'],
                                        ['id' => 'VA', 'name' => 'Virginia'],
                                        ['id' => 'WA', 'name' => 'Washington'],
                                        ['id' => 'DC', 'name' => 'Washington D.C.'],
                                        ['id' => 'WV', 'name' => 'West Virginia'],
                                        ['id' => 'WI', 'name' => 'Wisconsin'],
                                        ['id' => 'WY', 'name' => 'Wyoming']
                                    ];
                                    $s123 = '';
                                    foreach ($data as $key => $value) {
                                        if($value['id']==$row['state']){
                                            $s123 = $value['name'];
                                        }
                                    }
                                    $message .= "<td><strong>City</strong>: ".$row['city']."</td>"."\r\n";
                                    
                                $message .= "</tr>"."\r\n";
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Street name</strong>: ".$row['address1']."</td>"."\r\n";
                                    $message .= "<td><strong>State</strong>: ".$s123." </td>"."\r\n";
                                $message .= "</tr>"."\r\n";
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td><strong>Address line 2:</strong> ".$row['address2']."</td>"."\r\n";
                                    $message .= "<td><strong>Zip</strong>:".$row['zip']."</td>"."\r\n";
                                $message .= "</tr>"."\r\n";
        
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td colspan='2' style='padding-top: 30px;'>Thank you for your continued support in managingour platform effectively.</td>"."\r\n";
                                $message .= "</tr>"."\r\n";
                                $message .= "<tr>"."\r\n";
                                    $message .= "<td style='padding-top: 20px;'><b>Best regards,<br>Your car into cash</b></td>"."\r\n";
                                $message .= "</tr>"."\r\n";
                                       
                            $message .= "</table>"."\r\n";
                        $message .= "</td>"."\r\n";
                    $message .= "</tr>"."\r\n";
        $message .= "</body>"."\r\n";
        $message .= "</html>"."\r\n";
    }

    //echo $message;exit;
    $to = ',';
    while ($row1 = $result1->fetch_assoc()) {
    
        $to .= $row1['email'].',';
    }
    
    $to1 = substr_replace($to ,"",-1);
    

    
    $subject = 'User Accepted Offer';
    $from = 'ben@yourcarintocash.com';
    
    $headers  = 'MIME-Version: 1.0' . "\r\n";
    $headers .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n";
    
    $headers .= 'From: '.$from."\r\n".'Reply-To: '.$from."\r\n" .
    'X-Mailer: PHP/' . phpversion();
    
    if($to1!=''){
        if(mail($to1, $subject, $message, $headers)){echo 1;}else{echo $to1;}exit();
    }
    
    
//}