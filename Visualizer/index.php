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
    
    // Load the file for a given participant's dynamic or stable set
    function loadFile($experiment, $chain_code, $generation, $set, $word) {
        // Get the data from that file
        if ($set == "c") {
            $data = openFile("../Data/". $experiment ."/". $chain_code ."/". $generation . "d")."\n".openFile("../Data/". $experiment ."/". $chain_code ."/". $generation . "s");
        }
        else {
            $data = openFile("../Data/". $experiment ."/". $chain_code ."/". $generation . $set);
        }
        // Read the file line by line
        $lines = explode("\n", $data);
        // How many lines are there?
        $n = count($lines);
        // Set up an empty array for the data matrix
        $matrix = array();
        // For each line in the data file...
        for ($i=0; $i < $n; $i++) {
            // Separate out the columns delimited by tabs
            $row = explode("\t", $lines[$i]);
            if ($word=="ALL" OR $word==$row[0]) {
                $row[1] = explode(",", $row[1]);
                $row[2] = explode(",", $row[2]);
                $row[3] = explode(",", $row[3]);
                array_push($matrix, $row);
            }
        }
        // Return the data matrix
        return $matrix;
    }
    
/////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    if ($_REQUEST["page"] == "") { $page = "setup"; } else { $page = $_REQUEST["page"]; }
    if ($page == "display") {
        $js_onload = " onload='DrawTriangle()'";
        
        $type="file";
        if ($type=="file") {
            $matrix = loadFile($_REQUEST['experiment'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['set'], $_REQUEST['word']);
        }
    }
    
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

<?php
    if ($page == "display") {
        echo"<script type='text/javascript'>function DrawTriangle() { var canvas = document.getElementById('rectangle'); var c = canvas.getContext('2d');";
        
        $n = count($matrix);
        
        $colour_codes = array("#000000", "#C0C0C0", "#808080", "#FF0000", "#800000", "#FFFF00", "#808000", "#00FF00", "#008000", "#00FFFF", "#008080", "#0000FF", "#000080", "#FF00FF", "#800080");
        
        $colours = array();
        
        for ($i=0; $i<$n; $i++) {
            
            if ($colours[$matrix[$i][0]] != "") {
                $col = $colours[$matrix[$i][0]];
            }
            else {
                $colours[$matrix[$i][0]] = $colour_codes[0];
                $col = $colour_codes[0];
                unset($colour_codes[0]);
                $colour_codes = array_values($colour_codes);
            }
            
            echo "c.beginPath();\n";
            echo "c.moveTo('". $matrix[$i][1][0] ."', '". $matrix[$i][1][1] ."');\n";
            echo "c.lineTo('". $matrix[$i][2][0] ."', '". $matrix[$i][2][1] ."');\n";
            echo "c.lineTo('". $matrix[$i][3][0] ."', '". $matrix[$i][3][1] ."');\n";
            echo "c.closePath();\n";
            echo "c.lineWidth=2;\n";
            echo "c.strokeStyle='". $col ."';\n";
            echo "c.stroke();\n";
            echo "c.beginPath();\n";
            echo "c.arc(". $matrix[$i][1][0] .", ". $matrix[$i][1][1] .", 8, 0, 2 * Math.PI, false);\n";
            echo "c.fillStyle = '". $col ."';\n";
            echo "c.fill();\n";
            echo "c.lineWidth = 1;\n";
            echo "c.strokeStyle = '". $col ."';\n";
            echo "c.stroke();\n";
        }
        echo "}</script>";
    }
?>
        
</head>

<body<?php echo $js_onload; ?>>

<table style='width:100%;'>
    <tr>
        <td style='text-align:center;'>
<?php
    if ($page == "setup") {
        echo "
            <p class='page head'>Visualizer</p>
            <hr style='height:1; width:580px;' />
            <form id='parameters' name='f' method='post' action='index.php'>
                <input name='page' type='hidden' value='display' />
                <table style='width:400px; margin-left:auto; margin-right:auto;'>
                    <tr>
                        <td style='width:190px; text-align:right;'>
                            <span class='page body'>Experiment:</span>
                        </td>
                        <td style='width:20px;'></td>
                        <td style='width:190px;'>
                            <span class='page body'>
                                <input name='experiment' type='radio' value='1' checked /> Experiment 1<br />
                                <input name='experiment' type='radio' value='2' /> Experiment 2
                            </span>
                        </td>
                    </tr>
                    <tr>
                        <td style='width:190px; text-align:right;'>
                            <span class='page body'>Diffusion chain:</span>
                        </td>
                        <td style='width:20px;'></td>
                        <td style='width:190px;'>
                            <input name='chain' type='text' id='chain' style='font:Helvetica Neue; font-size:20px' size='8' />
                        </td>
                    </tr>
                    <tr>
                        <td style='width:190px; text-align:right;'>
                            <span class='page body'>Generation:</span>
                        </td>
                        <td style='width:20px;'></td>
                        <td style='width:190px;'>
                            <input name='gen' type='text' id='generation' style='font:Helvetica Neue; font-size:20px' size='8' />
                        </td>
                    </tr>
                    <tr>
                        <td style='width:190px; text-align:right;'>
                            <span class='page body'>Set:</span>
                        </td>
                        <td style='width:20px;'></td>
                        <td style='width:190px;'>
                            <input name='set' type='text' id='set_type' style='font:Helvetica Neue; font-size:20px' size='8' />
                        </td>
                    </tr>
        
        
        <tr>
        <td style='width:190px; text-align:right;'>
        <span class='page body'>Word:</span>
        </td>
        <td style='width:20px;'></td>
        <td style='width:190px;'>
        <input name='word' type='text' id='word' style='font:Helvetica Neue; font-size:20px' size='8' />
        </td>
        </tr>
        
        
                </table>
                <hr style='height:1; width:580px;' />
                <input type='submit' name='submit' value='Visualize' style='font-family:Helvetica Neue; font-size:30px;' />
            </form>
        ";
    }
        
    elseif ($page == "display") {
        echo "
        <table style='width:800px; margin-left:auto; margin-right:auto;'>
            <tr>
                <td>
                    <canvas id='rectangle' width='". $canvas_width ."' height='". $canvas_height ."' style='border:gray 1px dashed'></canvas>
                </td>
            </tr>
        </table>
        ";
    }
?>
        </td>
    </tr>
</table>
        
</body>
        
</html>