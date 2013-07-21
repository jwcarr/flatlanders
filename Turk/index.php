<?php
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// GLOBAL PARAMETERS
    
    // Canvas width in pixels for the triangle stimuli (default = 500)
    $canvas_width = 500;
    
    // Canvas height in pixels for the triangle stimuli (default = 500)
    $canvas_height = 500;
    
    // Width of the unusable boarder area around the canvas in pixels (default = 10)
    $canvas_border = 10;
    
    // Thickness of the trianlge lines in pixels (default = 2)
    $triangle_line_thickness = 2;
    
    // Radius of the orienting spot in pixels (default = 8)
    $orienting_spot_radius = 8;

    // Set timezone for timestamps (default = UTC)
    date_default_timezone_set('UTC');
    
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// GENERAL FUNCTIONS - MAINLY INVOLVES LOADING AND SAVING DATA
    
    // Open a file
    function openFile($filename) {
        // If the file actually exists...
        if (file_exists($filename)) {
            // If the filesize > 0...
            if (filesize($filename) > 0) {
                // Open the file
                $file = fopen($filename, "r");
                // If you can secure a lock on the file...
                if (flock($file, LOCK_EX)) {
                    // Read the current data from the file...
                    $data = fread($file, filesize($filename));
                    // ... and then unlock it
                    flock($file, LOCK_UN);
                }
                // Close the file
                fclose($file);
                // Return the file's content
                return $data;
            }
            // If filesize is 0, return null
            return "";
        }
        // If the file does not exist, return False
        return False;
    }
    
    // Write data to a file
    function writeFile($filename, $data) {
        // If the file actually exists...
        if (is_writable($filename)) {
            // Open the file
            $file = fopen($filename, "w");
            // If you can secure a lock on the file...
            if (flock($file, LOCK_EX)) {
                // Write data to the file...
                fwrite($file, $data);
                // ... and then unlock it
                flock($file, LOCK_UN);
            }
            // Close the file
            fclose($file);
            // Return True to indicate success
            return True;
        }
        // If the file does not exist, return False        
        return False;
    }
    
    // Load the file for a given participant's dynamic or stable set
    function loadFile($condition, $chain_code, $generation, $set) {
        // Get the data from that file
        $data = openFile("../data/". $condition ."/". $chain_code ."/". $generation . $set);
        // Read the file line by line
        $lines = explode("\n", $data);
        // Return the lines in an array
        return $lines;
    }
    
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// TRIANGLE STIMULI FUNCTIONS - FUNCTIONS FOR LOADING AND GENERATING TRIANGLES
    
    // Load the coordinates for a particular triangle stimulus from a given data file
    function loadTriangle($condition, $chain_code, $generation, $stimulus_set, $stimulus_number) {
        // Load in the lines from a specific data file
        $lines = loadFile($condition, $chain_code, $generation, $stimulus_set);
        // Break the particular line we need into columns using the tab as a delimiter
        $columns = explode("\t", $lines[$stimulus_number]);
        // Extract the XY coordinates for point A
        $xy1 = explode(",", $columns[1]);
        // Extract the XY coordinates for point B
        $xy2 = explode(",", $columns[2]);
        // Extract the XY coordinates for point C
        $xy3 = explode(",", $columns[3]);
        // Return the loaded coordinates
        return array($xy1[0], $xy2[0], $xy3[0], $xy1[1], $xy2[1], $xy3[1]);
    }
    
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// MAIN PHP SCRIPT - THIS GETS EVERYTHING SORTED BEFORE WE START SENDING HTML

    // If a specific page has been specified, set that as the current page; otherwise, goto the parameters page
    if ($_REQUEST["page"] != "") { $page = $_REQUEST["page"]; } else { $page = "instructions"; }
    
    // Load in any variables sent from the previous page
    $cond = $_REQUEST["cond"]; $chain = $_REQUEST["chain"]; $gen = $_REQUEST["gen"]; $map = $_REQUEST["map"];
    
    // If we are currently in the experiment...
    if ($page == "experiment") {
        
        // Set window location for next page for use in JavaScript below
        $window_location = "index.php?page=experiment&cond=". $cond ."&chain=". $chain ."&gen=". $gen ."&map=". $new_map;
    }
    
    $left_triangle = loadTriangle(1,"A",1,"s",rand(0,47));
    $right_triangle = loadTriangle(1,"A",1,"s",rand(0,47));
    
    $js_onload = " onload='DrawTriangle()'";

/////////////////////////////////////////////////////////////////////////////////////////////////////////
?>
<!DOCTYPE HTML>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Infinity</title>

<style type="text/css">
    .page {font-family: Helvetica Neue;}
    .head {color: #B22B3B; font-size: 30px}
    .body {color: black; font-size: 15px}
    .small {font-family: Helvetica Neue; font-size: 14px; font-weight:lighter;}
    .regular {font-family: Helvetica Neue; color: black; font-size: 16px}
    .large {font-family: Helvetica Neue; font-weight:lighter; color: black; font-size: 40px}
    .medium {font-family: Helvetica Neue; font-weight:lighter; color: black; font-size: 30px}
    .textfield {border-top-width: 0px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px;}
</style>

<script type="text/javascript">

    // Location of the next page
    var next_page_location = '<?php echo $window_location; ?>';
        
    var answer = '';

    // Send to next page
    function NextPage() {
        window.location = next_page_location;
    }

    // When the testing page loads, draw the triangle, and then give focus to the response textbox
    function TestingLoad() {
        DrawTriangle();
        document.f.a.focus();
    }
        
    // Check that the participant has not given a blank answer
    function CheckAnswer() {
        if (document.f.a.value == '') {
            return false;
        }
        document.f.a.blur();
        return true;
    }
    
    // Draw a triangle on the canvas
    function DrawTriangle() {
        var canvas_left = document.getElementById('left');
        var c = canvas_left.getContext('2d');
        c.beginPath();
        c.moveTo("<?php echo $left_triangle[0]; ?>", "<?php echo $left_triangle[3]; ?>");
        c.lineTo("<?php echo $left_triangle[1]; ?>", "<?php echo $left_triangle[4]; ?>");
        c.lineTo("<?php echo $left_triangle[2]; ?>", "<?php echo $left_triangle[5]; ?>");
        c.closePath();
        c.lineWidth="<?php echo $triangle_line_thickness; ?>";
        c.stroke();
        c.beginPath();
        c.arc("<?php echo $left_triangle[0]; ?>", "<?php echo $left_triangle[3]; ?>", "<?php echo $orienting_spot_radius; ?>", 0, 2 * Math.PI, false);
        c.fill();
        c.lineWidth = 1;
        c.strokeStyle = 'black';
        c.stroke();
        
        
        var canvas_right = document.getElementById('right');
        var c = canvas_right.getContext('2d');
        c.beginPath();
        c.moveTo("<?php echo $right_triangle[0]; ?>", "<?php echo $right_triangle[3]; ?>");
        c.lineTo("<?php echo $right_triangle[1]; ?>", "<?php echo $right_triangle[4]; ?>");
        c.lineTo("<?php echo $right_triangle[2]; ?>", "<?php echo $right_triangle[5]; ?>");
        c.closePath();
        c.lineWidth="<?php echo $triangle_line_thickness; ?>";
        c.stroke();
        c.beginPath();
        c.arc("<?php echo $right_triangle[0]; ?>", "<?php echo $right_triangle[3]; ?>", "<?php echo $orienting_spot_radius; ?>", 0, 2 * Math.PI, false);
        c.fill();
        c.lineWidth = 1;
        c.strokeStyle = 'black';
        c.stroke();
    }

</script>
        
</head>

<body<?php echo $js_onload; ?>>

<table style='width:100%; height:600px;'>
    <tr>
        <td style='text-align:center;'>
<?php
        
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// Experiment pages
        
    if ($page == "instructions") {
            
            // Output HTML for the welcome page
            echo "
            <p class='large'>Shape matching task</p>
            <p>&nbsp;</p>
            <p class='regular'>You will see 20 pairs of triangles. For each pair of triangles, rate how similar you think they are.</p>
            ";
    }
        
        // Training page          -------------------------------------------------------------------------
    elseif ($page == "task") {
        
            // Output HTML for the training page
            echo "
            <table style='width:1200px; margin-left:auto; margin-right:auto;'>
                <tr>
                    <td>
                        <canvas id='left' width='". $canvas_width ."' height='". $canvas_height ."' style='border:gray 1px dashed'></canvas>
                    </td>
                    <td>
                        <canvas id='right' width='". $canvas_width ."' height='". $canvas_height ."' style='border:gray 1px dashed'></canvas>
                    </td>
                </tr>
                <tr>
                    <td colspan='2'>
                        <form id='testing' name='f'>
        <input type='hidden' name='page' value='task' />
        <input type='hidden' name='ratings' value='". $ratings ."' />
        <p class='regular'><br />Use the slider to rate the similarity of these triangles<br />&nbsp;</p>
        <p class='small'>Very different&nbsp;&nbsp;&nbsp;&nbsp;<input type='range' min='0' max='100' name='rating' value='50' style='width:500px;' />&nbsp;&nbsp;&nbsp;&nbsp;Very similar</p>
                            <p class='small'>&nbsp;</p>
        <p><input type='submit' value='Next >' /></p>
                        </form>
                    </td>
                </tr>
            </table>
            ";
    }
        
    elseif ($page == "end") {
        
        // Output HTML for the training page
        echo "
        <table style='width:800px; margin-left:auto; margin-right:auto;'>
        <tr>
        <td>
        <canvas id='rectangle' width='". $canvas_width ."' height='". $canvas_height ."' style='border:gray 1px dashed'></canvas>
        </td>
        </tr>
        <tr>
        <td>
        <form id='testing' name='f'>
        <p><input name='a' type='text' value='' id='testtext' autocomplete='off' style='border:hidden; font-family:Helvetica Neue; font-size:40px; font-weight:lighter; text-align:center; outline:none' size='60' /></p>
        <p class='small'>&nbsp;</p>
        </form>
        </td>
        </tr>
        </table>
        ";
    }

/////////////////////////////////////////////////////////////////////////////////////////////////////////
// Return error, if the requested page is invalid
        
    else {
        echo "<h1>Page error</h1><p>Please inform the experiment supervisor.</p>";
    }
        
/////////////////////////////////////////////////////////////////////////////////////////////////////////

?>

        </td>
    </tr>
</table>
        
</body>
        
</html>