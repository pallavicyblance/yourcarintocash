
<?php

//$to = 'cyblance.nigam@gmail.com';
/*$to = 'vipul.cyblance@gmail.com';
$subject = 'Marriage Proposal';
$from = 'ben@yourcarintocash.com';
 
// To send HTML mail, the Content-type header must be set
$headers  = 'MIME-Version: 1.0' . "\r\n";
$headers .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n";
 
// Create email headers
$headers .= 'From: '.$from."\r\n".
    'Reply-To: '.$from."\r\n" .
    'X-Mailer: PHP/' . phpversion();
 
// Compose a simple HTML email message
$message = '<html><body>';
//$message .= '<h1 style="color:#f40;">Hi vipul!</h1>';
//$message .= '<p style="color:#080;font-size:18px;">Will you marry me?</p>';


$message .= '<p style="color:#080;font-size:18px;">Hello Recipients Name </p>';
$message .= '<p style="color:#080;font-size:18px;">This is a sample email content. You can customize it to suit your needs.</p>';
$message .= '<p style="color:#080;font-size:18px;">Regards,<br>Your Name</p>';
$message .= '<p> 2023 Company Name. All rights reserved.</p>';

$message .= '</body></html>';
echo $message; 
// Sending email
if(mail($to, $subject, $message, $headers)){
    echo 'Your mail has been sent successfully.';
} else{
    echo 'Unable to send email. Please try again.';
}*/


?>

<?php

if(isset($_POST['button']) && isset($_FILES['attachment']))
{
    $from_email      = 'ben@yourcarintocash.com'; //from mail, sender email address
    $recipient_email = 'vipul.cyblance@gmail.com'; //recipient email address
    
    //Load POST data from HTML form
    $sender_name = $_POST["sender_name"]; //sender name
    $reply_to_email = $_POST["sender_email"]; //sender email, it will be used in "reply-to" header
    $subject     = $_POST["subject"]; //subject for the email
    //$message     = $_POST["message"]; //body of the email


    $message = '<html><body>';
    $message .= '<h1 style="color:#f40;">Hi vipul!</h1>';
    $message .= '<p style="color:#080;font-size:18px;">Will you marry me?</p>';

    $message .= '<p style="color:#080;font-size:18px;">Hello Recipients Name </p>';
    $message .= '<p style="color:#080;font-size:18px;">This is a sample email content. You can customize it to suit your needs.</p>';
    $message .= '<p style="color:#080;font-size:18px;">Regards,<br>Your Name</p>';
    $message .= '<p> 2023 Company Name. All rights reserved.</p>';

    $message .= '</body></html>';

    $message = html_entity_decode($message);

    /*Always remember to validate the form fields like this
    if(strlen($sender_name)<1)
    {
        die('Name is too short or empty!');
    }
    */
    //Get uploaded file data using $_FILES array
    $tmp_name = $_FILES['attachment']['tmp_name']; // get the temporary file name of the file on the server
    $name    = $_FILES['attachment']['name']; // get the name of the file
    $size    = $_FILES['attachment']['size']; // get size of the file for size validation
    $type    = $_FILES['attachment']['type']; // get type of the file
    $error   = $_FILES['attachment']['error']; // get the error (if any)

    //validate form field for attaching the file
    if($error > 0)
    {
        die('Upload error or No files uploaded');
    }

    //read from the uploaded file & base64_encode content
    $handle = fopen($tmp_name, "r"); // set the file handle only for reading the file
    $content = fread($handle, $size); // reading the file
    fclose($handle);                 // close upon completion

    $encoded_content = chunk_split(base64_encode($content));
    $boundary = md5("random"); // define boundary with a md5 hashed value

    //header
    $headers = "MIME-Version: 1.0\r\n"; // Defining the MIME version
    $headers .= "From:".$from_email."\r\n"; // Sender Email
    $headers .= "Reply-To: ".$reply_to_email."\r\n"; // Email address to reach back
    $headers .= "Content-Type: multipart/mixed;"; // Defining Content-Type
    $headers .= "boundary = $boundary\r\n"; //Defining the Boundary
        
    //plain text
    $body = "--$boundary\r\n";
    $body .= "Content-Type: text/plain; charset=ISO-8859-1\r\n";
    $body .= "Content-Transfer-Encoding: base64\r\n\r\n";
    $body .= chunk_split(base64_encode($message));
        
    //attachment
    $body .= "--$boundary\r\n";
    $body .="Content-Type: $type; name=".$name."\r\n";
    $body .="Content-Disposition: attachment; filename=".$name."\r\n";
    $body .="Content-Transfer-Encoding: base64\r\n";
    $body .="X-Attachment-Id: ".rand(1000, 99999)."\r\n\r\n";
    $body .= $encoded_content; // Attaching the encoded file with email
    
    $sentMailResult = mail($recipient_email, $subject, $body, $headers);

    if($sentMailResult ){
        echo "<h3>File Sent Successfully.<h3>";
        // unlink($name); // delete the file after attachment sent.
    }
    else{
        die("Sorry but the email could not be sent.
                    Please go back and try again!");
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
    <title>Send Attachment With Email</title>
</head>
<body>
    <div style="display:flex; justify-content: center; margin-top:10%;">
        <form enctype="multipart/form-data" method="POST" action="" style="width: 500px;">
            <div class="form-group">
                <input class="form-control" type="text" name="sender_name" placeholder="Your Name" required/>
            </div>
            <div class="form-group">
                <input class="form-control" type="email" name="sender_email" placeholder="Recipient's Email Address" required/>
            </div>
            <div class="form-group">
                <input class="form-control" type="text" name="subject" placeholder="Subject"/>
            </div>
            <div class="form-group">
                <textarea class="form-control" name="message" placeholder="Message"></textarea>
            </div>
            <div class="form-group">
                <input class="form-control" type="file" name="attachment" placeholder="Attachment" required/>
            </div>
            <div class="form-group">
                <input class="btn btn-primary" type="submit" name="button" value="Submit" />
            </div>       
        </form>
    </div>
</body>
</html>

