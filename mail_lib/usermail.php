<?php

if(isset($_POST['email'])){
    $email = $_POST['email'];
    $fname = $_POST['fname'];
    $year = $_POST['year'];
    $make = $_POST['make'];
    $model = $_POST['model'];
    $mileage = $_POST['mileage'];
    $drive = $_POST['drive'];
    $revised_price = $_POST['revised_price'];

    $recipient = 'ben@yourcarintocash.com';
    $subject = "php mail test new";

    $message = "year".$year;
    $message .= "make".$make;
    $message .= "model".$model;
    $message .= "mileage".$mileage;
    $message .= "drive".$drive;
    $message .= "revised_price".$revised_price;


    $headers = 'From:' . $recipient;

    if (mail($email, $subject, $message, $headers))
    {
        echo "Message accepted";
    }
    else
    {   
        echo "Error: Message not accepted";
    }

    
}
    /*$sender = 'pallavi.cyblance@gmail.com';
    $year = '2019';
    $make = 'Toyota';
    $model = 'Corolla';
    $mileage = '10000';
    $drive = 'D';
    $revised_price = '10000';

    $recipient = 'ben@yourcarintocash.com';

    $subject = "php mail test new";


    $message = "year".$year;
    $message .= "make".$make;
    $message .= "model".$model;
    $message .= "mileage".$mileage;
    $message .= "drive".$drive;
    $message .= "revised_price".$revised_price;


    $headers = 'From:' . $recipient;

    if (mail($sender, $subject, $message, $headers))
    {
        echo "Message accepted";
    }
    else
    {   
        echo "Error: Message not accepted";
    }*/
?>