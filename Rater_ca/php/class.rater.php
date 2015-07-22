<?php

class Rater {

  private $valid_rater = False;

  function __construct($id) {
    global $data_directory;
    $this->id = $id;
    $this->file = new File($data_directory . 'started/' . $this->id, True);
    $rater_parameters = $this->file->getLine(0);
    if ($rater_parameters !== False) {
      $this->valid_rater = True;
      $this->current = $rater_parameters[0];
      $this->orientation = $rater_parameters[1];
    }
  }

  public function getCurrentTriangles() {
    $rating_pair = $this->getCurrentPair();
    if ($rating_pair === False) {
      return False;
    }
    $coords1 = explode(';', $rating_pair[0]);
    $triangle1 = array(explode(',', $coords1[0]), explode(',', $coords1[1]), explode(',', $coords1[2]));
    $coords2 = explode(';', $rating_pair[1]);
    $triangle2 = array(explode(',', $coords2[0]), explode(',', $coords2[1]), explode(',', $coords2[2]));
    if (rand(0, 1) === 1) {
      return array($triangle1, $triangle2, $rating_pair[0], $rating_pair[1]);
    }
    return array($triangle2, $triangle1, $rating_pair[0], $rating_pair[1]);
  }

  public function getLeftRightLabels() {
    if ($this->orientation == 'L') {
      return array('very similar', 'very different');
    }
    return array('very different', 'very similar');
  }

  private function getCurrentPair() {
    $rating_pair = $this->file->getLine($this->current);
    if ($rating_pair === False or is_null($rating_pair) === True) {
      return False;
    }
    return array($rating_pair[0], $rating_pair[1]);
  }

  private function setRating($rating_num, $triangle1, $triangle2, $rating) {
    if ($this->orientation == 'R') {
      $rating = 1000 - $rating;
    }
    return $this->file->setLine($rating_num, array($triangle1, $triangle2, $rating, time()));
  }

  private function incrementCurrentRating() {
    $this->current += 1;
    $current_header = $this->file->getLine(0);
    return $this->file->setLine(0, array($this->current, $this->orientation, $current_header[2], $current_header[3]));
  }

  public function storeRating($rating_num, $triangle1, $triangle2, $rating) {
    if (is_numeric($rating)) {
      if ($rating_num == $this->current) {
        $current_pair = $this->getCurrentPair();
        if ($current_pair[0] == $triangle1 or $current_pair[0] == $triangle2) {
          $this->setRating($rating_num, $current_pair[0], $current_pair[1], $rating);
          $this->incrementCurrentRating();
          return True;
        }
      }
    }
    return False;
  }

  public function logStartTime() {
    $current_header = $this->file->getLine(0);
    $current_header[] = $_SERVER['REMOTE_ADDR'];
    $current_header[] = time();
    $this->file->setLine(0, $current_header);
    if ($this->file->overwrite()) {
      return True;
    }
    return False;
  }

  public function getTimeTaken() {
    $previous_datum = $this->file->getLine($this->current - 2);
    return time() - $previous_datum[3];
  }

  public function validate() {
    if ($this->valid_rater === True) {
      return True;
    }
    return False;
  }

  public function generateCompletionCode() {
    $letters1 = array('B', 'C', 'D', 'E', 'F', 'G', 'H');
    $letters2 = array('t', 'u', 'v', 'w', 'x', 'y', 'z');
    $letters3 = array('K', 'L', 'M', 'N', 'P', 'Q', 'R');
    $code = rand(1, 5) . $letters1[rand(0, 6)] . rand(3, 7) . $letters2[rand(0, 6)] . rand(5, 9) . $letters3[rand(0, 6)] . rand(100, 999);
    $this->file->addLine(array($code));
    return $code;
  }

  public function save() {
    return $this->file->overwrite();
  }

  public function blockRater() {
    global $data_directory;
    // Log IP address
    $ip_log = new File($data_directory . 'ip_log', True);
    $ip_log->addLine(array($_SERVER['REMOTE_ADDR']));
    $ip_log->overwrite();
    unset($ip_log);

    // Set cookie
    setcookie('tst', $this->id, time()+2419200);
  }

}

class File {

  private $filename = '';
  private $write_access = False;
  private $data_change = False;
  public $data = False;

  public function __construct($filename, $write_access=False) {
    $this->filename = $filename;
    $this->write_access = $write_access;
    $file_contents = $this->openFile();
    if (is_null($file_contents)) {
      $this->data = array();
    }
    elseif ($file_contents !== False) {
      $this->data = explode("\n", $file_contents);
    }
  }

  public function __destruct() {
    if ($this->write_access) {
      flock($this->file, LOCK_UN);
      fclose($this->file);
    }
  }

  public function getLine($line_number) {
    if ($this->data === False) {
      return False;
    }
    if ($line_number >= count($this->data)) {
      return False;
    }
    $line = $this->data[$line_number];
    if ($line == '') {
      return Null;
    }
    return explode("\t", $line);
  }

  public function setLine($line_number, $content_array) {
    if ($line_number >= count($this->data)) {
      return False;
    }
    $this->data[$line_number] = implode("\t", $content_array);
    return True;
  }

  public function addLine($content_array) {
    $this->data[] = implode("\t", $content_array);
    return True;
  }

  public function removeLine($line_number) {
    unset($this->data[$line_number]);
    return True;
  }

  private function openFile() {
    if ($this->write_access) {
      return $this->openFileWithWriteAccess();
    }
    else {
      return $this->openFileWithoutWriteAccess();
    }
  }

  private function openFileWithoutWriteAccess() {
    if (file_exists($this->filename)) {
      $this->file = fopen($this->filename, 'r');
      if ($this->file != False) {
        if (flock($this->file, LOCK_SH)) {
          $file_size = filesize($this->filename);
          if ($file_size == 0) {
            $data = Null;
          }
          else {
            $data = fread($this->file, $file_size);
          }
          flock($this->file, LOCK_UN);
          fclose($this->file);
          return $data;
        }
        fclose($this->file);
      }
    }
    return False;
  }

  private function openFileWithWriteAccess() {
    if (file_exists($this->filename)) {
      if (is_writable($this->filename)) {
        $this->file = fopen($this->filename, 'a+');
        for ($i=0; $i<10; $i++) {
          if (flock($this->file, LOCK_EX)) {
            $file_size = filesize($this->filename);
            if ($file_size == 0) {
              return Null;
            }
            return fread($this->file, $file_size);
          }
          sleep(1);
        }
        fclose($this->file);
      }
      $this->write_access = False;
      return $this->openFileWithoutWriteAccess();
    }
    return False;
  }

  public function overwrite() {
    if ($this->write_access) {
      if (ftruncate($this->file, 0)) {
        if (fwrite($this->file, implode("\n", $this->data))) {
          flock($this->file, LOCK_UN);
          fclose($this->file);
          $this->write_access = False;
          return True;
        }
      }
      flock($this->file, LOCK_UN);
      fclose($this->file);
    }
    $this->write_access = False;
    return False;
  }

}

?>
