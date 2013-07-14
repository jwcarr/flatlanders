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
    
    #$triangles = array(array(250,250,250,50,400,75), array(300,100,400,40,200,400));
    #$triangles = array(array(250,250,250,50,400,75), array(300,45,400,-15,200,345));
    $triangles = array(array(250,250,250,50,400,75), array(250,250,350,190,150,550));
    
    if ($_REQUEST["page"] == "") { $page = "setup"; } else { $page = $_REQUEST["page"]; }
    if ($page == "display") { $js_onload = " onload='DrawTriangle()'"; }
    
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
        
        $n = count($triangles);
        
        for ($i=0; $i<$n; $i++) {
            echo "c.beginPath();\n";
            echo "c.moveTo('". $triangles[$i][0] ."', '". $triangles[$i][1] ."');\n";
            echo "c.lineTo('". $triangles[$i][2] ."', '". $triangles[$i][3] ."');\n";
            echo "c.lineTo('". $triangles[$i][4] ."', '". $triangles[$i][5] ."');\n";
            echo "c.closePath();\n";
            echo "c.lineWidth=2;\n";
            echo "c.strokeStyle='red';\n";
            echo "c.stroke();\n";
            echo "c.beginPath();\n";
            echo "c.arc(". $triangles[$i][0] .", ". $triangles[$i][1] .", 8, 0, 2 * Math.PI, false);\n";
            echo "c.fill();\n";
            echo "c.lineWidth = 1;\n";
            echo "c.strokeStyle = 'black';\n";
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
                                <input name='condition' type='radio' value='1' checked /> Experiment 1<br />
                                <input name='condition' type='radio' value='2' /> Experiment 2
                            </span>
                        </td>
                    </tr>
                    <tr>
                        <td style='width:190px; text-align:right;'>
                            <span class='page body'>Diffusion chain:</span>
                        </td>
                        <td style='width:20px;'></td>
                        <td style='width:190px;'>
                            <input name='chain' type='text' id='chain' autocomplete='off' style='font:Helvetica Neue; font-size:20px' size='8' />
                        </td>
                    </tr>
                    <tr>
                        <td style='width:190px; text-align:right;'>
                            <span class='page body'>Generation:</span>
                        </td>
                        <td style='width:20px;'></td>
                        <td style='width:190px;'>
                            <input name='gen' type='text' id='generation' autocomplete='off' style='font:Helvetica Neue; font-size:20px' size='8' />
                        </td>
                    </tr>
                    <tr>
                        <td style='width:190px; text-align:right;'>
                            <span class='page body'>Word:</span>
                        </td>
                        <td style='width:20px;'></td>
                        <td style='width:190px;'>
                            <input name='gen' type='text' id='generation' autocomplete='off' style='font:Helvetica Neue; font-size:20px' size='8' />
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