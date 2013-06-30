<?php
    function openFile($filename) {
        if (file_exists($filename)) {
            if (filesize($filename) > 0) {
                $file = fopen($filename, "r");
                if (flock($file, LOCK_EX)) {
                    $data = fread($file, filesize($filename));
                    flock($file, LOCK_UN);
                }
                fclose($file);
                return $data;
            }
            return "";
        }
        return False;
    }
    function writeFile($filename, $data) {
        if (is_writable($filename)) {
            $file = fopen($filename, "w");
            if (flock($file, LOCK_EX)) {
                fwrite($file, $data);
                flock($file, LOCK_UN);
            }
            fclose($file);
            return True;
        }
        return False;
    }
    $data = openFile("data/prizedraw");
    $emails = explode("\n", $data);
    $emails[] = $_POST["email"];
    shuffle($emails);
    $data = implode("\n", $emails);
    writeFile("data/prizedraw", $data);
?>
<!DOCTYPE HTML>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Infinity</title>

<style type="text/css">
    .large {font-family: Helvetica Neue; font-weight:lighter; color: black; font-size: 40px}
    .medium {font-family: Helvetica Neue; font-weight:lighter; color: black; font-size: 30px}
</style>

</head>

<body onload='document.prize.email.focus()'>

<table style='width:100%; height:750px;'>
    <tr>
        <td style='text-align:center;'>
            <p class='large'>Email address saved</p>
            <p class='medium'>The winner will be notified by mid-August</p>
        </td>
    </tr>
</table>
        
</body>
        
</html>