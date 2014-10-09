<script type="text/javascript">

// Location of the next_page_location page
var next_page_location = '<?php echo $window_location; ?>';
var answer = '';
var server_ip = '<?php echo $server_ip; ?>';
var node_port = '<?php echo $node_port; ?>';

// Send to next page
function NextPage() {
    window.location = next_page_location;
}

// Show the training item and play the vocalization
function ShowWord() {
    document.getElementById('alex').play();
    document.getElementById('message').html = '<?php echo $training_word; ?>';
}

// Applies to welcome page only. On pressing the 'enter key', move to the next page
function KeyCheck() {
    var keyID = event.keyCode;
    if (keyID == 13) {
        window.location = next_page_location + '&first_training_item=yes';
    }
}

// When the training page loads, draw the triangle, set delay for showing the training item, and set delay for moving to next page
function TrainingLoad() {
    DrawTriangle('rectangle', <?php echo $xy[0] .", ". $xy[1] .", ". $xy[2] .", ". $xy[3] .", ". $xy[4] .", ". $xy[5]; ?>);
    setTimeout("ShowWord()", <?php echo $word_delay; ?>);
    setTimeout("NextPage()", <?php echo $time_per_training_item; ?>);
}

//When the testing page loads, draw the triangle, and then give focus to the response textbox
function TestingLoad() {
    DrawTriangle('rectangle', <?php echo $xy[0] .", ". $xy[1] .", ". $xy[2] .", ". $xy[3] .", ". $xy[4] .", ". $xy[5]; ?>);
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

// Give feedback on whether the participant got the mini test right or wrong
function GiveFeedback() {
    if (document.f.a.value == '') {
        return false;
    }
    else {
        document.f.a.blur();
        if (document.f.a.value == '<?php echo $correct_answer; ?>') {
            document.getElementById('tink').play();
            document.getElementById('feedback').src = 'images/check.png';
            document.f.a.style.color = '<?php if($colourblind==True){echo "#008CED";} else {echo"#67C200";} ?>';
            answer = document.f.a.value;
            setTimeout("SaveMTResponse()", <?php echo $feedback_time; ?>);
        }
        else {
            document.getElementById('funk').play();
            document.getElementById('feedback').src = 'images/cross.png';
            document.f.a.style.color = '#FF2F00';
            document.f.a.style.fontStyle = 'oblique';
            answer = document.f.a.value;
            setTimeout("SaveMTResponse()", <?php echo $feedback_time; ?>);
            document.f.a.value = '<?php echo $correct_answer; ?>';
        }
        return false;
    }
}

// Send to next page, saving the mini test answer
function SaveMTResponse() {
    window.location = next_page_location + '&a=' + answer + '&correct_answer=<?php echo $correct_answer; ?>';
}

// Draw a triangle on the canvas
function DrawTriangle(canvasID, x0, x1, x2, y0, y1, y2) {

    document.f.last_x1.value = x0;
    document.f.last_x2.value = x1;
    document.f.last_x3.value = x2;
    document.f.last_y1.value = y0;
    document.f.last_y2.value = y1;
    document.f.last_y3.value = y2;

    var canvas = document.getElementById(canvasID);
    var c = canvas.getContext('2d');
    c.beginPath();
    c.moveTo(x0, y0);
    c.lineTo(x1, y1);
    c.lineTo(x2, y2);
    c.closePath();
    c.lineWidth = <?php echo $triangle_line_thickness; ?>;
    c.strokeStyle = 'black';
    c.stroke();
    c.beginPath();
    c.arc(x0, y0, "<?php echo $orienting_spot_radius; ?>", 0, 2 * Math.PI, false);
    c.fillStyle = 'black';
    c.fill();
    c.lineWidth = 1;
    c.strokeStyle = 'black';
    c.stroke();
}

function DrawTriangleArray(target_coordinates) {
    var target_triangle = target_coordinates.split(',');
    var distractor_triangles = [<?php echo $triangle_array_JS; ?>];
    var position = Math.floor(Math.random()*6);
    var triangles = distractor_triangles.slice( 0, position*6 ).concat( target_triangle ).concat( distractor_triangles.slice( position*6 ) );

    document.f.target.value= position;

    n = <?php echo $triangle_array_size[1]*$triangle_array_size[0]; ?>;

    for (i=0; i<(n*6); i+=6) {
        DrawTriangle('box'+(i/6), triangles[i], triangles[i+1], triangles[i+2], triangles[i+3], triangles[i+4], triangles[i+5]);
    }
}

// Check for duplicates in a participant's answers
function CheckDuplicates() {
    if (document.f.a.value == '') {
        return false;
    }
    var used_words = [<?php echo $overused_words; ?>];
    if (used_words.indexOf(document.f.a.value) != -1) {
        document.getElementById('instruction').innerHTML = 'Ooops! You’ve used this word too often. Please use another word.';
        document.getElementById('instruction').style.color = '#FF2F00';
        document.f.a.value = '';
        document.f.overuse.value = <?php echo $_REQUEST["overuse"]+1; ?>;
        return false;
    }
    document.f.a.blur();
    return true;
}

function PartnerFeedback(correct, coordinates) {
    if (correct == true) {
        $(instruction).html("Your partner answered correctly");
        $(message).html("<img src='images/check.png' width='33' height='33' />");
        $(stimulus).append("<canvas id='feedback_box' width='<?php echo $canvas_width; ?>' height='<?php echo $canvas_height; ?>'></canvas>");
        DrawTriangle(feedback_box, coordinates[0], coordinates[1], coordinates[2], coordinates[3], coordinates[4], coordinates[5]);
    }
    else {
        $(message).html("<img src='images/cross.png' width='33' height='33' />");
        $(instruction).html("Your partner answered incorrectly");
        $(stimulus).append("<canvas id='feedback_box' width='<?php echo $canvas_width; ?>' height='<?php echo $canvas_height; ?>'></canvas>");
        DrawTriangle(feedback_box, coordinates[0], coordinates[1], coordinates[2], coordinates[3], coordinates[4], coordinates[5]);
    }
    setTimeout('NextPage()' , <?php echo $feedback_time; ?>);
}

function SelectTriangle(triangle) {
    document.f.response.value = triangle;
    for (i=0; i<6; i++) {
        if (i != triangle) {
            document.getElementById("box"+i).style.border = "dashed gray 1px";
            document.getElementById("box"+i).style.background = "white";
        }
        else {
            document.getElementById("box"+triangle).style.border = "solid #B22B3B 1px";
            document.getElementById("box"+triangle).style.background = "#FEFAFA";
        }
    }
    document.getElementById('bottom-button').innerHTML = "<input type='submit' name='send_answer' id='button' value='Submit' />";
}

</script>
