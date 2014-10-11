<?php

function generateMap($condition, $chain, $generation) {
  // Import required global variables
  global $set_size, $mini_test_frequency;

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

  if ($condition == 3) {
    $map = $map ."||MT-". $mini_test_numbers[$set_size-1] ."||WAIT";
  }
  else {
    // Add on one final mini test and the break page
    $map = $map ."||MT-". $mini_test_numbers[$set_size-1] ."||BREAK";
  }

  if ($_REQUEST["subject"] == "") {$_REQUEST["subject"] = "SubA";}

  // Shuffle the order in which the test items in both the dynamic and stable sets will be presented
  $dynamic_set = range(0, $set_size-1); shuffle($dynamic_set);
  $stable_set = range(0, $set_size-1); shuffle($stable_set);

  if ($condition == 3) {
    $mapA = $map; $mapB = $map;
    // Add the test pages to the map, interleaving the dynamic flow and stable flow
    for ($i=0; $i < $set_size; $i+=2) {
      $mapA = $mapA ."||TS-d.". $dynamic_set[$i] ."||TA-d.". $dynamic_set[$i+1] ."||TS-s.". $stable_set[$i] ."||TA-s.". $stable_set[$i+1];
      $mapB = $mapB ."||TA-d.". $dynamic_set[$i] ."||TS-d.". $dynamic_set[$i+1] ."||TA-s.". $stable_set[$i] ."||TS-s.". $stable_set[$i+1];
    }
    $map = $mapA;
    writeFile("data/client", "page=experiment&subject=SubB&cond={$condition}&chain={$chain}&gen={$generation}&map={$mapB}||END");
  }
  else {
    // Add the test pages to the map, interleaving the dynamic flow and stable flow
    for ($i=0; $i < $set_size; $i++) {
      $map = $map ."||TS-d.". $dynamic_set[$i] ."||TS-s.". $stable_set[$i];
    }
  }

  // Finally we want to add on the experiment completed page
  return $map ."||END";
}

?>
