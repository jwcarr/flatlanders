<?php
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// GLOBAL PARAMETERS
    
    // List of valid chain codes (default = [A, B, C, D, E, F, G, H])
    $chain_codes = array("A", "B", "C", "D", "E", "F", "G", "H");
    
    // Maximum generation number (default = 10)
    $max_generation_number = 10;
    
    // Magnitude of the stimuli sets (default = 48)
    $set_size = 48;
    
    // Amount of time for each training item in milliseconds (default = 5000)
    $time_per_training_item = 5000;
    
    // Delay before showing the training word in milliseconds (default = 1000)
    $word_delay = 1000;
    
    // Length of time to show feedback in milliseconds (default = 1000)
    $feedback_time = 1000;
    
    // Amount of time for the break between training and testing in seconds (default = 30)
    $break_time = 30;
    
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
    
    // Number of times a word can be reused to label items in the dynamic set (experiment 2 only) (default = 3)
    $permitted_word_repetitions = 3;
    
    // Do a mini test every X items during the training phase (default = 3, must be a divisor of $set_size)
    // Note, this also determines the number of passes over the training data, ensuring that each item is mini-tested exactly once
    $mini_test_frequency = 3;
    
    // For colourblind participants, use blue for correct answers rather than green. This should make it distinct from red.
    $colourblind = False;

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
        $data = openFile("data/". $condition ."/". $chain_code ."/". $generation . $set);
        // Read the file line by line
        $lines = explode("\n", $data);
        // Return the lines in an array
        return $lines;
    }

    // Get the words from a data file
    function getWords($condition, $chain_code, $generation) {
        // Load in the file for a specific participant's dynamic set file
        $lines = loadFile($condition, $chain_code, $generation, "d");
        // How many lines are there?
        $n = count($lines);
        // Set up an empty array in which to dump the words
        $words = array();
        // For each line in the data file...
        for ($i=0; $i < $n; $i++) {
            // Separate out the columns delimited by tabs
            $columns = explode("\t", $lines[$i]);
            // Dump the first column (the word) into the $words array
            array_push($words, $columns[0]);
        }
        // Return the words as an array
        return $words;
    }
    
    // Get a specific word from a given participant's dynamic set file
    function getWord($condition, $chain_code, $generation, $word_number) {
        // Get all words in that participant's dynamic file
        $words = getWords($condition, $chain_code, $generation);
        // Return the requested word
        return $words[$word_number];
    }
    
    // Save log data to the log file
    function saveLogData($new_data) {
        // Open the log file as it stands
        $data = openFile("data/log");
        // Write out the new log file
        writeFile("data/log", $data ."\n". $new_data);
    }
    
    // Save a test answer to a participant's dynamic or stable set file
    function saveAnswer($condition, $chain_code, $generation, $position, $answer, $xy) {
        // Parse the map position into a set type ("d" or "s") and the stimulus number (0–49)
        $position = explode(".", $position);
        // If saving a dynamic file...
        if ($position[0] == "d") {
            // Concatenate the answer, XY coordinates, and timestamp (delimited by tabs)
            $answer = trim($answer) ."\t". $xy[0] .",". $xy[3] ."\t". $xy[1] .",". $xy[4] ."\t". $xy[2] .",". $xy[5] ."\t". date("H:i:s");
        }
        // If saving a stable file...
        else {
            // Concatenate the stimulus number, answer, XY coordinates, and timestamp (delimited by tabs)
            $answer = $position[1] ."|||". trim($answer) ."\t". $xy[0] .",". $xy[3] ."\t". $xy[1] .",". $xy[4] ."\t". $xy[2] .",". $xy[5] ."\t". date("H:i:s");
        }
        // Determine the filename you want to write to
        $filename = "data/". $condition ."/". $chain_code ."/". $generation . $position[0];
        // Read the content of that file as it currently stands
        $current_data = openFile($filename);
        // The new content of the file is the old data + the new answer
        $new_data = $current_data ."\n". $answer;
        // Write this new data to the file
       	writeFile($filename, trim($new_data));
    }
    
    // Save the final test item, and then sort the stable set into its unshuffled order
    function saveFinalAnswer($condition, $chain_code, $generation, $position, $answer, $xy) {
        // Import the global variable $set_size
        global $set_size;
        // Parse the map position into a set type ("d" or "s") and the stimulus number (0–49)
        $position = explode(".", $position);
        // Load in the lines from a specific stable set file
        $lines = loadFile($condition, $chain_code, $generation, "s");
        // Concatenate the stimulus number, answer, XY coordinates, and timestamp (delimited by tabs) for the final test item
        $answer = $position[1] ."|||". trim($answer) ."\t". $xy[0] .",". $xy[3] ."\t". $xy[1] .",". $xy[4] ."\t". $xy[2] .",". $xy[5] ."\t". date("H:i:s");
        // Add the final answer to the lines array
        array_push($lines, $answer);
        // Set up an empty array in which to dump the parsed lines
        $mappings = array();
        // For each line in the file...
        for ($i=0; $i < $set_size; $i++) {
            // Parse the line into its stimulus number and recorded data
            $parsed_line = explode("|||", $lines[$i]);
            // Put the recorded data into the $mappings array with a key equal to the stimulus number (also, append the order number (i) to the recorded data)
            $mappings[$parsed_line[0]] = $parsed_line[1] ."\t". ($i+1);
        }
        // Sorts the $mappings array by key
        ksort($mappings);
        // Implode the $mappings array, using a line break as the glue
        $new_data = implode("\n", $mappings);
        // Write the new data to the data file
        writeFile("data/". $condition ."/" . $chain_code ."/". $generation."s", $new_data);
    }
    
    // Clear the data files for a specific participant
    function clearFiles($condition, $chain_code, $generation) {
        // Overwrite the dynamic set file with "" (null)
        writeFile("data/". $condition ."/". $chain_code ."/". $generation."d", "");
        // Overwrite the stable set file with "" (null)
        writeFile("data/". $condition ."/". $chain_code ."/". $generation."s", "");
    }
    
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// MAP FUNCTIONS - FUNCTIONS FOR CREATING AND PARSING THE MAP
    
    function generateMap() {
        // Import required global variables
        global $set_size; global $mini_test_frequency;
        
        // First we want to present the welcome page
        $map = "BEGIN";

        $success = false;
        while ($success == False) {
            // Set up empty array for the training numbers
            $training_numbers = array();
            
            // Set up an empty array for the mini test numbers
            $mini_test_numbers = array();
            
            // For each training pass...
            for ($i=0; $i < $mini_test_frequency; $i++) {
                // Set up an array containing the numbers 0 to $set_size-1
                $pass_i_numbers = range(0, $set_size-1);
                // Now shuffle this array
                shuffle($pass_i_numbers);
                // Then, working through $pass_i_numbers in sets of N, where N = $mini_test_frequency...
                for ($j=0; $j < $set_size; $j=$j+$mini_test_frequency) {
                    // Get the set of N items we want to choose from
                    $this_set = array_slice($pass_i_numbers, $j, $mini_test_frequency);
                    // Shuffle this set
                    shuffle($this_set);
                    // and then try N times to choose an $mt_item that hasn't already been added to $mini_test_numbers
                    for ($k=0; $k < $mini_test_frequency; $k++) {
                        $mt_item = $this_set[$k];
                        if (in_array($mt_item, $mini_test_numbers) == False) {
                            // When you've found one of the N items that hasn't already been added, add it to $mini_test_numbers
                            $mini_test_numbers[] = $mt_item;
                            // Break the most recent loop
                            break;
                        }
                        // If that fails...
                        if ($k == $mini_test_frequency-1) {
                            // Go through remainder of $pass_i_numbers to find one that is not in $mini_test_numbers
                            for ($l=$j+$mini_test_frequency; $l < $set_size-1; $l++) {
                                if (in_array($pass_i_numbers[$l], $mini_test_numbers) == False) {
                                    // Choose one of the members of $this_set at random
                                    $m = rand($j, $j+$mini_test_frequency-1);
                                    // Define $swapA as the randomly chosen item from $this_set
                                    $swapA = $pass_i_numbers[$m];
                                    // Define $swapB as item $l that you've just identified as a good swap
                                    $swapB = $pass_i_numbers[$l];
                                    // Swap those two around
                                    $pass_i_numbers[$l] = $swapA;
                                    $pass_i_numbers[$m] = $swapB;
                                    // Set the next mini test number to $swapB
                                    $mini_test_numbers[] = $swapB;
                                    // Break the most recent loop
                                    break;
                                }
                            }
                        }
                    }
                }
                // Finally, append the array to the array of training numbers
                $training_numbers = array_merge($training_numbers, $pass_i_numbers);
            }
            
            // If, after all that, you have a full set of mini test numbers, then set $success to True.
            // Otherwise, go through the whole process again until you find a map that works.
            if (count($mini_test_numbers) == $set_size) { $success = True; }

        }
        
        // Since this algorithm seems to be slightly biased towards choosing the last of N items to mini-test,
        // let's reshuffle each set of N to be sure it's truly random.
        for ($i=0; $i < $set_size*$mini_test_frequency; $i=$i+$mini_test_frequency) {
            $this_set = array_slice($training_numbers, $i, $mini_test_frequency);
            shuffle($this_set);
            array_splice($training_numbers, $i, $mini_test_frequency, $this_set);
        }
    
        // Add the training pages to the map in this shuffled order with a mini test every x items
        for ($i=0, $c=0; $i < $set_size*$mini_test_frequency; $i++) {
            if ($c == $mini_test_frequency) {
                $map = $map ."||MT-". $mini_test_numbers[($i/$mini_test_frequency)-1];
                $c=0;
            }
            $map = $map ."||TR-". $training_numbers[$i];
            $c=$c+1;
        }
        
        // Add on one final mini test and the break page
        $map = $map ."||MT-". $mini_test_numbers[$set_size-1] ."||BREAK";
        
        // Shuffle the order in which the test items in both the dynamic and stable sets will be presented
        $dynamic_set = range(0, $set_size-1); shuffle($dynamic_set);
        $stable_set = range(0, $set_size-1); shuffle($stable_set);
        
        // Add the test pages to the map, interleaving the dynamic flow and stable flow
        for ($i=0; $i < $set_size; $i++) {
            $map = $map ."||TS-d.". $dynamic_set[$i] ."||TS-s.". $stable_set[$i];
        }
        
        // Finally we want to add on the experiment completed page
        return $map ."||END";
    }
    
    function parseMap($map) {
        // Parse the map into its constituent parts
        $map = explode("||", $map);
        
        // Parse the first map item for information about the page and stimulus number
        $map_position = explode("-", $map[0]);
        
        // Remove the first item from the map
        unset($map[0]);
        
        // Implode the map array back to a string using double pipe as the glue
        $new_map = implode("||", $map);
        
        // Return the new map, and info about the page and stimulus number
        return array($new_map, $map_position[0], $map_position[1]);
    }
    
    
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// TRIANGLE STIMULI FUNCTIONS - FUNCTIONS FOR LOADING AND GENERATING TRIANGLES
    
    // Generate a random triangle stimulus
    function generateTriangle() {
        // Import global parameters
        global $canvas_width; global $canvas_height; global $canvas_border;
        
        // Choose coordinates for point A
        $x1 = rand($canvas_border+1, $canvas_width-$canvas_border);
        $y1 = rand($canvas_border+1, $canvas_height-$canvas_border);
        
        // Choose coordinates for point B
        $x2 = rand($canvas_border+1, $canvas_width-$canvas_border);
        $y2 = rand($canvas_border+1, $canvas_height-$canvas_border);

        // Choose coordinates for point C
        $x3 = rand($canvas_border+1, $canvas_width-$canvas_border);
        $y3 = rand($canvas_border+1, $canvas_height-$canvas_border);
        
        // Return an array containing the chosen X and Y coordinates
        return array($x1, $x2, $x3, $y1, $y2, $y3);
    }
    
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
// VALIDATION FUNCTIONS - FUNCTIONS FOR VALIDATING THE SETUP PARAMETERS

    // Check that the chain code belongs to the global set of valid chain codes
    function checkChain($chain_code) {
        global $chain_codes;
        if (in_array($chain_code, $chain_codes) == True) { return True; } else { return False; }
    }

    // Check that the generation number does not exceed the global maximum generation number (and is greater than 0)
    function checkGen($generation_number) {
        global $max_generation_number;
        if ($generation_number > 0 AND $generation_number <= $max_generation_number) { return True; } else { return False; }
    }

    // Check that the output data files exist and are writeable
    function checkOutputFiles($condition, $chain_code, $generation) {
        $dynamic_file = is_writable("data/". $condition ."/" . $chain_code ."/" . $generation ."d");
        $stable_file = is_writable("data/". $condition ."/" . $chain_code ."/" . $generation ."s");
        if ($dynamic_file == True AND $stable_file == True) { return True; } else { return False; }
    }
    
    // Check that the input data files contain the correct number of lines (i.e. $set_size number of lines)
    function checkInputSet($condition, $chain_code, $generation) {
        global $set_size;
        $lines = loadFile($condition, $chain_code, ($generation-1), "d");
        if (count($lines) == $set_size) { return True; } else { return False; }
    }
    
    // Check that the required sound files are present and accounted for
    function checkSoundFiles($words) {
        // Set up an array to dump a list of missing sound files
        $missing_words = array();
        // For each word that needs a vocalization...
        for ($i = 0; $i < count($words); $i++) {
            // ... check that a sounds file exists
            if (file_exists("vocalizations/". $words[$i] .".m4a") == False) {
                // If not, add it to the missing words array
                $missing_words[] = $words[$i] . ".m4a";
            }
        }
        // Return the array of missing words
        return $missing_words;
    }
    
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// MAIN PHP SCRIPT - THIS GETS EVERYTHING SORTED BEFORE WE START SENDING HTML

    // If a specific page has been specified, set that as the current page; otherwise, goto the parameters page
    if ($_REQUEST["page"] != "") { $page = $_REQUEST["page"]; } else { $page = "parameters"; }
    
    // Load in any variables sent from the previous page
    $cond = $_REQUEST["cond"]; $chain = $_REQUEST["chain"]; $gen = $_REQUEST["gen"]; $map = $_REQUEST["map"];
    
    // If we are currently in the experiment...
    if ($page == "experiment") {
        
        // Generate MAP if one hasn't been set up yet
        if ($map == "") {
            $map = generateMap();
        }
        
        // Parse the map
        $parsed_map = parseMap($map);
        $new_map = $parsed_map[0];
        $experiment_page = $parsed_map[1];
        $item_info = $parsed_map[2];
        
        // Set window location for next page for use in JavaScript below
        $window_location = "index.php?page=experiment&cond=". $cond ."&chain=". $chain ."&gen=". $gen ."&map=". $new_map;
        
        // If this is a TRAINING PAGE
        if ($experiment_page == "TR") {
            // Get the relvant training word from previous participant's dynamic set file
            $training_word = getWord($cond, $chain, ($gen-1), $item_info);
            
            // Get the XY coordinates for the relevant triangle from the previous participant's dynamic set file
            $xy = loadTriangle($cond, $chain, ($gen-1), "d", $item_info);
            
            // If is the first training item...
            if ($_REQUEST["first_training_item"] == "yes") {
                // Write log to the "training" file
                saveLogData("Cond.\tChain\tGen.\tTimestamp\n". $cond. "\t". $chain ."\t". $gen ."\t". date("d/m/Y H:i:s") ."\n\n". $map ."\n");
            }
            
            // If a mini test answer has been provided...
            if ($_REQUEST["a"] != "") {
                // Write it to the log along with the correct answer
                saveLogData($_REQUEST["correct_answer"] ."\t". $_REQUEST["a"]);
            }
            
            // Set JavaScript onload to TrainingLoad()
            $js_onload = " onload='TrainingLoad()'";
        }
        
        // If this is a MINI TEST PAGE
        elseif ($experiment_page == "MT") {
            // Get the XY coordinates for for the random chosen stimulus from the previous participant's dynamic set file
            $xy = loadTriangle($cond, $chain, ($gen-1), "d", $item_info);
            // Get the correct word for the randomly chosen stimulus
            $correct_answer = getWord($cond, $chain, $gen-1, $item_info);
            // Set JavaScript onload to TestingLoad()
            $js_onload = " onload='TestingLoad()'";
        }
        
        // If this is a TEST PAGE
        elseif ($experiment_page == "TS") {
            // Parse the test item information into its set (either "d" or "s") and the stimulus number from that set (number between 0 and 47)
            $stimulus_info = explode(".", $item_info);
            $stimulus_set = $stimulus_info[0];
            $stimulus_number = $stimulus_info[1];
            
            // Set JavaScript onload to TestingLoad()
            $js_onload = " onload='TestingLoad()'";
            
            // If the current test item belongs to the dynamic flow...
            if ($stimulus_set == "d") {
                // Generate random XY coordinates
                $xy = generateTriangle();
            }
            // Otherwise, if the current test item belongs to the stable flow...
            else {
                // Load the XY coordinates for the relevant triangle from the stable set file
                $xy = loadTriangle($cond, $chain, ($gen-1), "s", $stimulus_number);
            }
            
            // If the participant is in condition 2 and the current test item belongs to the dynamic set...
            if ($cond == 2 AND $stimulus_set == "d") {
                // Get the words that the participant has used so far
                $words = getWords($cond, $chain, $gen);
                
                // Count the total number of words that have been used so far
                $n = count($words);
                
                // Set up an empty array into which to put overused words
                $overused_words = array();
                
                // Add each word that has been overused to the $overused_words array
                for ($i=0; $i<$n; $i++) {
                    $c=1;
                    for ($j=$i+1; $j<$n; $j++) {
                        if ($words[$i] == $words[$j]) {
                            $words[$j] = $i." ".$j;
                            $c = $c+1;
                        }
                    }
                    if ($c == $permitted_word_repetitions) { $overused_words[] = $words[$i]; }
                }
                
                // Implode the array of words into a string
                $overused_words = "\"". implode("\", \"", $overused_words) ."\"";
            }
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

<?php if ($page == "experiment" AND $experiment_page == "BREAK") { echo "<script src='countdown.js' type='text/javascript'></script>"; }?>

<script type="text/javascript">

    // Location of the next page
    var next_page_location = '<?php echo $window_location; ?>';
        
    var answer = '';

    // Send to next page
    function NextPage() {
        window.location = next_page_location;
    }

    // Show the training item and play the vocalization
    function ShowWord() {
        document.getElementById('alex').play();
        document.f.a.value = '<?php echo $training_word; ?>';
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
        DrawTriangle();
        setTimeout("ShowWord()", <?php echo $word_delay; ?>);
        setTimeout("NextPage()", <?php echo $time_per_training_item; ?>);
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
        
    // Give feedback on whether the participant got the mini test right or wrong
    function GiveFeedback() {
        if (document.f.a.value == '') {
            return false;
        }
        else {
            document.f.a.blur();
            if (document.f.a.value == '<?php echo $correct_answer; ?>') {
                document.getElementById('tink').play();
                document.getElementById('feedback').src = 'images/check<?php if($colourblind==True){echo "_blue";} ?>.png';
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
    function DrawTriangle() {
        var canvas = document.getElementById('rectangle');
        var c = canvas.getContext('2d');
        c.beginPath();
        c.moveTo("<?php echo $xy[0]; ?>", "<?php echo $xy[3]; ?>");
        c.lineTo("<?php echo $xy[1]; ?>", "<?php echo $xy[4]; ?>");
        c.lineTo("<?php echo $xy[2]; ?>", "<?php echo $xy[5]; ?>");
        c.closePath();
        c.lineWidth="<?php echo $triangle_line_thickness; ?>";
        c.stroke();
        c.beginPath();
        c.arc("<?php echo $xy[0]; ?>", "<?php echo $xy[3]; ?>", "<?php echo $orienting_spot_radius; ?>", 0, 2 * Math.PI, false);
        c.fill();
        c.lineWidth = 1;
        c.strokeStyle = 'black';
        c.stroke();
    }

    // Check for duplicates in a participant's answers
    function CheckDuplicates() {
        if (document.f.a.value == '') {
            return false;
        }
        var used_words = [<?php echo $overused_words; ?>];
        if (used_words.indexOf(document.f.a.value) != -1) {
            document.getElementById('message').innerHTML = 'Ooops! You\'ve used this word too often. Please use another word.';
            document.getElementById('message').style.color = '#FF2F00';
            document.f.a.value = '';
            document.f.overuse.value = <?php echo $_REQUEST["overuse"]+1; ?>;
            return false;
        }
        document.f.a.blur();
        return true;
    }

</script>
        
</head>

<body<?php echo $js_onload; ?>>

<table style='width:100%; height:750px;'>
    <tr>
        <td style='text-align:center;'>
<?php
        
    if ($set_size % $mini_test_frequency != 0) { echo "WARNING: Global parameter mini_test_frequency must be a divisor of set_size"; }
        
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// Parameters page

    if ($page == "parameters") {
        echo "
            <p class='page head'>Settings</p>
            <hr style='height:1; width:580px;' />
            <form id='parameters' name='f' method='post' action='index.php'>
                <input name='page' type='hidden' value='validation' />
                <table style='width:400px; margin-left:auto; margin-right:auto;'>
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
                            <span class='page body'>Experiment:</span>
                        </td>
                        <td style='width:20px;'></td>
                        <td style='width:190px;'>
                            <span class='page body'>
                                <input name='condition' type='radio' value='1' /> Experiment 1<br />
                                <input name='condition' type='radio' value='2' checked /> Experiment 2
                            </span>
                        </td>
                    </tr>
                </table>
                <hr style='height:1; width:580px;' />
                <input type='submit' name='submit' value='Okay' style='font-family:Helvetica Neue; font-size:30px;' />
            </form>
        ";
    }

/////////////////////////////////////////////////////////////////////////////////////////////////////////
// Validation page
        
    elseif ($page == "validation") {
        
        // Function to output a row on the validation page
        function validationTableRow($colour, $message) {
            return "
                <tr>
                    <td style='width:30px;'>
                        <img src='images/". $colour .".png' width='16' height='16' alt='light' />
                    </td>
                    <td style='width:550px; text-align:left;'>
                        <p class='regular'>". $message ."</p>
                    </td>
                </tr>";
        }
        
        echo "
            <p class='page head'>Validation</p>
            <table style='margin-left:auto; margin-right:auto;'>
                <tr>
                    <td colspan='2'>
                        <hr style='height:1; width:580px;' />
                    </td>
                </tr>
        ";

        // Check that the chain code is valid
        if (checkChain($_REQUEST["chain"]) == True) { echo validationTableRow("green", "Chain " . $_REQUEST["chain"]); }
        else { echo validationTableRow("red", "Chain \"". $_REQUEST["chain"] ."\" is invalid"); $error_count ++; }

        // Check that the generation number is valid
        if (checkGen($_REQUEST["gen"]) == True) { echo validationTableRow("green", "Generation " . $_REQUEST["gen"]); }
        else { echo validationTableRow("red", "Generation \"". $_REQUEST["gen"] ."\" is invalid"); $error_count ++; }

        // Check the condition number is valid
        if ($_REQUEST["condition"] == 1 OR $_REQUEST["condition"] == 2) { echo validationTableRow("green", "Experimental condition " . $_REQUEST["condition"]); }
        else { echo validationTableRow("red", "Condition \"". $_REQUEST["condition"] ."\" is invalid"); $error_count ++; }

        // Check that there are $set_size words in the input set
        if (checkInputSet($_REQUEST["condition"], $_REQUEST["chain"], $_REQUEST["gen"]) == True) { echo validationTableRow("green", "Words in the input set are valid"); }
        else { echo validationTableRow("red", "Input file does not contain $set_size words"); $error_count ++; }
        
        // Check that the data files exist for writing
        if (checkOutputFiles($_REQUEST["condition"], $_REQUEST["chain"], $_REQUEST["gen"]) == True) { echo validationTableRow("green", "Output data files are ready for writing"); }
        else { echo validationTableRow("red", "Output data files at <i>/data/" . $_REQUEST["condition"] . "/" . $_REQUEST["chain"] . "/</i> are not writeable. Check Permissions"); $error_count ++; }

        // Check that sound files exist for the words in the input set
        $words = getWords($_REQUEST["condition"], $_REQUEST["chain"], ($_REQUEST["gen"]-1));
        $missing_words = checkSoundFiles($words);
        if (count($missing_words) == 0) { echo validationTableRow("green", "Required sound files are available"); }
        else {
            // If there are missing words, output a list of them
            for ($i=0; $i < count($missing_words); $i++) {
                $missing_words_list = $missing_words_list . $missing_words[$i] . ", ";
            }
            echo validationTableRow("red", "The following sound files are missing: " . substr($missing_words_list, 0, -2));
            $error_count ++;
        }
        
        // If the above validation functions produce no errors, display messages to check the volume level and keyboard layout
        if ($error_count == 0) {
            // Sound warning
            echo validationTableRow("orange", "Is the volume level okay? <a href=\"javascript:document.getElementById('alex').play()\">test</a>");
        
            // Keyboard layout warning
            echo validationTableRow("orange", "Are you using the Alpha-only keyboard layout?");
        }
        
        echo "
                <tr>
                    <td colspan='2'>
                        <hr style='height:1; width:580px;' />
                    </td>
                </tr>
            </table>";
        
        // If the above validation functions produce no errors, display the "Begin experiment" button and embed the sound check file
        if ($error_count == 0) {
            echo "
            <form id='parameters' name='f' method='post' action='index.php'>
                <input name='page' type='hidden' value='experiment' />
                <input name='chain' type='hidden' value='". $_REQUEST["chain"] ."' />
                <input name='cond' type='hidden' value='". $_REQUEST["condition"] ."' />
                <input name='gen' type='hidden' value='". $_REQUEST["gen"] ."' />
                <input type='submit' name='submit' value='Begin experiment' style='font-family:Helvetica Neue; font-size:30px;' />
            </form>
            <audio id='alex' src='sound_check.m4a' preload='auto'></audio>";
        }
    }
        
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// Experiment pages
        
    elseif ($page == "experiment") {
        
        // Welcome page           -------------------------------------------------------------------------
        if ($experiment_page == "BEGIN") {
            
            // Clear the data files in case they already contain content
            clearFiles($cond, $chain, $gen);
            
            // Write the condition, chain, and generation number to the detect file for use by the status tracker
            writeFile("detect", $cond . "||" . $chain . "||" . $gen);
            
            // Output HTML for the welcome page
            echo "
            <p class='large'>Stage 1: Training</p>
            <p>&nbsp;</p>
            <p class='regular'>You will see a series of triangles along with the words used to describe them.<br />
            After every third triangle, you will see one of those three triangles again, and you<br />
            must type in the word you just learned for it. You will be told whether or not you got it right.</p>
            <p class='regular'>Try to learn the words for the triangles as best as you can, as you will be tested on them later.</p>
            <p>&nbsp;</p>
            <p class='medium'>Press the enter key when you’re ready to begin training</p>
            <script type='text/Javascript'>document.onkeypress = KeyCheck;</script>
            ";
        }
        
        // Training page          -------------------------------------------------------------------------
        elseif ($experiment_page == "TR") {
            
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
            <audio id='alex' src='vocalizations/". $training_word .".m4a' preload='auto'></audio>
            ";
        }
        
        
        // Mini test page         -------------------------------------------------------------------------
        elseif ($experiment_page == "MT") {
            
            // Output HTML for the "mini test" page
            echo "
            <table style='width:800px; margin-left:auto; margin-right:auto;'>
                <tr>
                <td>
                    <canvas id='rectangle' width='". $canvas_width ."' height='". $canvas_height ."' style='border:gray 1px dashed'></canvas>
                    </td>
                </tr>
                <tr>
                    <td>
                        <form id='testing' name='f' method='post' action='index.php' onsubmit='return GiveFeedback()'>
                            <p>
                                <img id='space' src='images/spacer.gif' width='40' height='40' alt='feedback' />
                                <input name='a' type='text' value='' id='testtext' autocomplete='off' style='border:none; font-family:Helvetica Neue; font-size:40px; font-weight:lighter; text-align:center; outline:none' size='27' />
                                <img id='feedback' src='images/spacer.gif' width='40' height='40' alt='feedback' />
                            </p>
                            <p class='small'>Type in the word for this triangle and press enter.</p>
                        </form>
                    </td>
                </tr>
            </table>
            <audio id='tink' src='tink.m4a' preload='auto'></audio>
            <audio id='funk' src='funk.m4a' preload='auto'></audio>";
        }
        
        // Testing page           -------------------------------------------------------------------------
        elseif ($experiment_page == "TS") {
            
            // If this is not the first test item (indicated by the fact that $current is set to nothing), do the following...
            if ($_REQUEST["current"] != "") {
                // Create an XY array from the previous XY coordinates
                $last_xy = array($_REQUEST["last_x1"], $_REQUEST["last_x2"], $_REQUEST["last_x3"], $_REQUEST["last_y1"], $_REQUEST["last_y2"], $_REQUEST["last_y3"]);
                
                // Save the previous answer to the relevant file
                saveAnswer($cond, $chain, $gen, $_REQUEST["current"], $_REQUEST["a"], $last_xy);
            }
            
            // If the participant is in condition 1
            if ($cond == 1) {
                // Set the check javascript to CheckAnswer()
                $check_script = "CheckAnswer()";
            }
            // If the participant is in condition 2
            else {
                // Set the check javascript to CheckDuplicates()
                $check_script = "CheckDuplicates()";
            }
            
            // Output HTML for the test page
            echo "
            <table style='width:800px; margin-left:auto; margin-right:auto;'>
                <tr>
                    <td>
                        <canvas id='rectangle' width='". $canvas_width ."' height='". $canvas_height ."' style='border:gray 1px dashed'></canvas>
                    </td>
                </tr>
                <tr>
                    <td>
                        <form id='testing' name='f' method='post' action='index.php' onsubmit='return ". $check_script ."'>
                            <input name='page' type='hidden' value='experiment' />
                            <input name='map' type='hidden' value='". $new_map ."' />
                            <input name='chain' type='hidden' value='". $chain ."' />
                            <input name='cond' type='hidden' value='". $cond ."' />
                            <input name='gen' type='hidden' value='". $gen ."' />
                            <input name='current' type='hidden' value='". $item_info ."' />
                            <input name='last_x1' type='hidden' value='". $xy[0] ."' />
                            <input name='last_x2' type='hidden' value='". $xy[1] ."' />
                            <input name='last_x3' type='hidden' value='". $xy[2] ."' />
                            <input name='last_y1' type='hidden' value='". $xy[3] ."' />
                            <input name='last_y2' type='hidden' value='". $xy[4] ."' />
                            <input name='last_y3' type='hidden' value='". $xy[5] ."' />
                            <input name='overuse' type='hidden' value='". $_REQUEST["overuse"] ."' />
                            <p>
                                <img id='space' src='images/spacer.gif' width='40' height='40' alt='feedback' />
                                <input name='a' type='text' value='' id='testtext' autocomplete='off' style='border:none; font-family:Helvetica Neue; font-size:40px; font-weight:lighter; text-align:center; outline:none' size='27' />
                                <img id='feedback' src='images/spacer.gif' width='40' height='40' alt='feedback' />
                            </p>
                            <p class='small' id='message'>Type in the word for this triangle and press enter.</p>
                        </form>
                    </td>
                </tr>
            </table>";
        }
        
        // Break page         -------------------------------------------------------------------------
        elseif ($experiment_page == "BREAK") {
            
            // If an answer to a mini test has been provided...
            if ($_REQUEST["a"] != "") {
                // Write the answer to the log
                saveLogData($_REQUEST["correct_answer"] ."\t". $_REQUEST["a"]);
            }
            
            // Output HTML for the break page
            echo "
            <p class='large'>Stage 2: Test</p>
            <p class='medium'>The test will automatically begin in ". $break_time ." seconds</p>
            <p>&nbsp;</p>
            <table style='margin-left:auto; margin-right:auto;'>
                <tr>
                    <td>
                        <script type='application/javascript'>var myCountdown2 = new Countdown({style: 'flip', time: ". $break_time .", width:100, height:80, rangeHi:'second', onComplete: NextPage, labels: {color: '#FFFFFF'}});</script>
                    </td>
                </tr>
            </table>
            <p>&nbsp;</p>
            <p class='regular'>You will shortly see a series of triangles. For each one, type in what you<br />
            think it&apos;s called based on the training you&apos;ve just completed.</p>
            <p class='regular'>You may find it very difficult to remember the words for the different triangles.<br />
                Go with your instinct and type in a word that feels right. You will still<br />
                get points for getting a word partially correct.</p>";
            
            // If the participant is in the second condition...
            if ($_REQUEST["cond"] == 2) {
                // Add a reminder to say that they can't use the same word more than once
                echo "
            <p class='regular'>Remember: if you use a particular word too often, you will see a message asking you to use a different word.</p>";
            }
        }
        
        // End page         -------------------------------------------------------------------------
        elseif ($experiment_page == "END") {
            
            // Create an XY array from the previous XY coordinates
            $last_xy = array($_REQUEST["last_x1"], $_REQUEST["last_x2"], $_REQUEST["last_x3"], $_REQUEST["last_y1"], $_REQUEST["last_y2"], $_REQUEST["last_y3"]);
            
            // Save the final answer (and sort the stable data file back to its unshuffled order)
            saveFinalAnswer($cond, $chain, $gen, $_REQUEST["current"], $_REQUEST["a"], $last_xy);
            
            // Write time at whcih the experiment ended to log
            if ($cond == 1) {
                saveLogData("\nEND AT " . date("d/m/Y H:i:s") . "\n-------------------------------------------------------\n\n");
            }
            else {
                saveLogData("\nOveruse count = ". $_REQUEST["overuse"] ."\n\nEND AT " . date("d/m/Y H:i:s") . "\n-------------------------------------------------------\n\n");
            }
            
            // Output HTML for the completion page
            echo "
            <p class='large'>Experiment complete</p>
            <p class='medium'>Thanks for your participation</p>
            <p>&nbsp;</p>
            <a href='prize.html'>
            <img src='images/smile.png' width='145' alt='flatlander smile' />
            </a>";
        }
        
        // Return error, if the requested experiment page is invalid
        else {
            echo "<h1>Map error</h1><p>Please inform the experiment supervisor.</p>";
        }
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