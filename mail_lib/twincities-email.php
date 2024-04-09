<?php
header('Access-Control-Allow-Origin: *');


if(isset($_POST['email_ragister'])){
    $email = $_POST['email_ragister'];
    $firstname = $_POST['first_name_ragister'];
    $lastname = $_POST['last_name_ragister'];
    if($email !=''){
        $recipient = 'ben@yourcarintocash.com';
        $subject = 'User Registration';
        $message = 'Hello '.$firstname.' '.$lastname.','. "<br/><br/>";
        $message .= 'Thank you for joining Twin city!'. "<br/><br/>";
        $message .= 'This is the confirmation mail you are getting after successful registration'. "<br/>";
        $message .= 'Best regards,'. "<br/>";
        $message .= 'Twin cities auctions'. "<br/>";
        $headers  = 'MIME-Version: 1.0' . "<br/>";
        $headers .= 'From:' . $recipient;
        echo $message; exit();
        if(mail($email, $subject, $message, $headers)){echo 1;}else{echo 2;}exit();
    }
}

?>
