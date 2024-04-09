<?php
header('Access-Control-Allow-Origin: *');

if(isset($_POST['email'])){
    $email = $_POST['email'];
    $fname = $_POST['fname'];
    $year = $_POST['year'];
    $make = $_POST['make'];
    $model = $_POST['model'];
    $mileage = $_POST['mileage'];
    $drive = $_POST['drive'];
    $revised_price = $_POST['revised_price'];

    if($drive == 'D'){
        $drive = 'yes';
    }else{
        $drive = 'no';
    }
    if($email !=''){
        $recipient = 'ben@yourcarintocash.com';
        $subject = 'User Registration';

        $message = '<html lang="en">';
        $message .= '<head>';
        $message .= '<meta charset="UTF-8">';
        $message .= '<meta name="viewport" content="width=device-width, initial-scale=1.0">' ; 
        $message .= '<title>Email Template</title>' ;
        $message .= '<style type="text/css">';

        $message .= 'body {
            Margin: 0;
            padding: 0;
            background-color: #f6f9fc;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        table {
          border-spacing: 0;
        }
        td {
          padding: 0;
        }
        img {
          border: 0;
        }
        .wrapper {
            width: 100%;
            table-layout: fixed;
            background-color: #f6f6f6;
            padding-bottom: 40px;
        }
        .webkit {
          max-width: 600px;
          background-color: #ffffff;
        }
        .outer {
          Margin: 0 auto;
          width: 100%;
          max-width: 600px;
          border-spacing: 0;
          font-family: Arial, sans-serif;
          color: #333333;
        }
        .three-columns {
          text-align: center;
          font-size: 0;
          padding-top: 40px;
          padding-bottom: 30px;
        }
        .three-columns .column {
          width: 100%;
          max-width: 200px;
          display: inline-block;
          vertical-align: top;
        }
        .padding {
          padding: 15px;
        }
        .content {
          font-size: 15px;
          line-height: 20px;
        }';
        $message .= '</style>';
        $message .= '</head>';

        $message .= '<body>';
        $message .= '<center class="wrapper">';
        $message .= '<div class="webkit">';
        $message .= ' <table class="outer" align="center" style="font-size: 14px;font-family: Arial, sans-serif; box-sizing: border-box; line-height: 1.4;">';
        $message .= '<tr>';
        $message .= '<td>';
        $message .= '<table width="100%" style="background:#f6f6f6;">';
        $message .= '<tr>';
        $message .= '<td style="text-align:center;padding:20px;">';
        $message .= '<img src="https://yourcarintocash.com/wp-content/uploads/2022/06/car-logo.png" width="143" alt="Logo">';
        $message .= '</td>';
        $message .= '</tr>';
        $message .= '</table>';
        $message .= '</td>';
        $message .= '</tr>';


        $message .=  '<tr>';
        $message .= '<td style="padding:20px;">';
        $message .= '<table width="100%">';

        $message .= '<tr>';
        $message .= '<td colspan="3" style="padding-bottom:10px;">';
        $message .= 'Dear '.$fname .',';
        $message .= '</td>';
        $message .= '</tr>';

        $message .= '<tr>';
        $message .= '<td colspan="3" style="padding-bottom:15px;">';
        $message .= "<strong>Congratulations!</strong> We're thrilled to inform you that your offer for the " . $year. " " . $make . " " .$model . " has been accepted.";
        $message .= '</td>';
        $message .= '</tr>';

        $message .= '<tr>';
        $message .= '<td width="270px" style="background-color:#22b573;color:#ffffff;padding:25px;text-align:center; border-radius: 5px;    box-sizing: border-box;">';
        $message .= '<h3 style="font-weight: 900; font-size: 22px; margin: 0px;padding: 0px;">Offer Amount</h3>';
        $message .= '<h2 style="font-weight: bold; font-size: 46px; margin: 0px;padding: 0px;">$'. $revised_price . '</h2>';
        $message .= '</td>';
        $message .= '<td style="width:20px;"></td>';
        $message .= '<td width="270px" style="background-color:#333333;color:#ffffff;padding:25px 10px;text-align:center; border-radius: 5px;    box-sizing: border-box;">';
        $message .= '<table width="100%" border="0">';
        $message .= '<tr>';
        $message .= '<td>';
        $message .= '<h3 style="font-weight: 900; color: #22b573; font-size: 18px; margin: 0px;padding: 0px;">'. $year. " " . $make . " " .$model .' </h3>';
        $message .= '<p style="font-size: 16px;line-height: 1.5; margin: 0px;padding: 0px;"><strong>Running and Driving:</strong> Yes<br>
        <strong>Mileage:</strong> '. $mileage . '</p>';
        $message .= '</td>';
        $message .= '</tr>';
        $message .= '</table>';
        $message .= '</td>';
        $message .= '</tr>';

        $message .= '<tr>';
        $message .= '<td colspan="3" style="padding-top:15px;">';
        $message .= '</tr>';

        $message .= '<tr>';
        $message .= '<td width="270px" style="padding:0px;text-align:center; border-radius: 5px; box-sizing: border-box; overflow: hidden;">';
        $message .= '<img width="100%" src="https://yourcarintocash.com/dev-carcash/static/images/dimg.jpg" width="270px" height="270px" alt="" style="float: left;">';
        $message .= '</td>';
        $message .= '<td style="width:20px;"></td>';
        $message .= '<td width="270px" style="background-color:#f6f6f6;color:#333333;padding:15px;text-align:left; border-radius: 5px;    box-sizing: border-box;font-size: 16px;line-height: 1.4; vertical-align: top;">';
        $message .= '<h3 style="font-weight: 900; font-size: 22px; margin: 0px;padding: 0px; margin-bottom: 10px;">Action Required:</h3>';
        $message .= '<p style="margin: 0px 0px 15px 0px;"><strong>Title signing instructions:</strong> For <strong style="color: #22b573;">Minnesota</strong> sellers, please refer <a href="#" style="text-decoration: underline;color: #000;">step-by-step: How to properly sign your title in MN</a></p>';
        $message .= '<p style="margin: 0px;">Once signed, please send the picture of the signed title to this email address.</p>';
        $message .= '</td>';
        $message .= '</tr>';

        $message .= '<tr>';
        $message .= '<td colspan="3" style="height: 20px;"></td>';
        $message .= '</tr>';

        $message .= '<tr>';
        $message .= '<td colspan="3"  style="padding:0px 0;">';
        $message .= 'Your pick-up partner is <strong>Twin Cities Auctions</strong>. A representative from them will contact you shortly to arrange the pick-up.';
        $message .= '</td>';
        $message .= '</tr>';

        $message .= '<tr>';
        $message .= '<td colspan="3" style="height: 10px;"></td>';
        $message .= '</tr>';

        $message .= '<tr>';
        $message .= '<td colspan="3"  style="padding:0px 0;">';
        $message .= 'Thank you for choosing us! <br>For any assistance, please reach out to <strong><a href="mailto:support@yourcarintocash.com" style="color:#22b573;">support@yourcarintocash.com</a></strong>';
        $message .= '</td>';
        $message .= '</tr>';

        $message .= '<tr>';
        $message .= '<td colspan="3" style="height: 10px;"></td>';
        $message .= '</tr>';

        $message .= '<tr>';
        $message .= '<td colspan="3"  style="padding:0px 0; line-height: 1.4;">';
        $message .= '<strong>Best Regards, <br> <span style="color: #22b573;">YourCarIntoCash</span></strong>';
        $message .= '</td>';
        $message .= '</tr>';

        $message .= '</table>';
        $message .= '</td>';
        $message .= '</tr>';


        $message .= '</table>';
        $message .= '</div>';
        $message .= '</center>';

        $headers  = 'MIME-Version: 1.0' . "<br/>";
        $headers .= 'From:' . $recipient;
        
        if(mail($email, $subject, $message, $headers)){echo 1;}else{echo 2;}exit();
    }

}
?>