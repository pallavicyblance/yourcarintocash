<?PHP
$sender = 'anil.cyblance@gmail.com';
$recipient = 'ben@yourcarintocash.com';

$subject = "php mail test new";
$message = "php test message email";
$headers = 'From:' . $recipient;

if (mail($sender, $subject, $message, $headers))
{
    echo "Message accepted";
}
else
{
    echo "Error: Message not accepted";
}
?>