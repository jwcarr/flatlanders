<?php

class Rater {

  private $valid_rater = False;

  function __construct($id) {
    $this->id = $id;
    $this->file = new File('data/started/' . $this->id, True);
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
    if ($rating_pair[0] >= 0) {
      $triangle1 = $this->stable_set[$rating_pair[0]];
      $triangle2 = $this->stable_set[$rating_pair[1]];
    }
    else {
      $triangle1 = $this->practice_set[abs($rating_pair[0])-1];
      $triangle2 = $this->practice_set[abs($rating_pair[1])-1];
    }
    if (rand(0, 1) === 1) {
      return array($triangle1, $triangle2, $rating_pair[0], $rating_pair[1]);
    }
    return array($triangle2, $triangle1, $rating_pair[1], $rating_pair[0]);
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
    $this->submitted_rating = $rating;
    if ($this->orientation == 'R') {
      $this->submitted_rating = 1000 - $rating;
    }
    return $this->file->setLine($rating_num, array($triangle1, $triangle2, $this->submitted_rating, time()));
  }

  private function incrementCurrentRating() {
    $this->current += 1;
    $current_header = $this->file->getLine(0);
    return $this->file->setLine(0, array($this->current, $this->orientation, $current_header[2], $current_header[3]));
  }

  public function storeRating($rating_num, $triangle1, $triangle2, $rating) {
    if ($rating_num == $this->current) {
      $current_pair = $this->getCurrentPair();
      if ($current_pair[0] == $triangle1 or $current_pair[0] == $triangle2) {
        if ($current_pair[1] == $triangle1 or $current_pair[1] == $triangle2) {
          $this->setRating($rating_num, $triangle1, $triangle2, $rating);
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
    $letters2 = array('K', 'L', 'M', 'N', 'P', 'Q', 'R');
    $letters3 = array('t', 'u', 'v', 'w', 'x', 'y', 'z');
    $code = rand(1, 5) . $letters1[rand(0, 6)] . rand(3, 7) . $letters2[rand(0, 6)] . rand(5, 9) . $letters3[rand(0, 6)] . rand(100, 999);
    $this->file->addLine(array($code));
    return $code;
  }

  public function save() {
    return $this->file->overwrite();
  }

  public function blockRater() {
    // Log IP address
    $ip_log = new File('data/ip_log', True);
    $ip_log->addLine(array($_SERVER['REMOTE_ADDR']));
    $ip_log->overwrite();
    unset($ip_log);

    // Set cookie
    setcookie('tst', 'false', time()+2419200);
  }

  private $practice_set = array(array(array(86, 169), array(120, 216), array(436, 399)), array(array(144, 391), array(208, 137), array(457, 168)), array(array(86, 78), array(211, 107), array(147, 483)), array(array(300, 72), array(222, 477), array(113, 110)), array(array(42, 319), array(93, 132), array(46, 412)), array(array(429, 92), array(312, 197), array(119, 197)), array(array(321, 361), array(415, 193), array(224, 237)), array(array(213, 263), array(455, 213), array(370, 59)), array(array(177, 372), array(447, 44), array(475, 193)), array(array(280, 308), array(219, 21), array(355, 351)), array(array(311, 180), array(66, 426), array(446, 166)), array(array(398, 474), array(21, 332), array(153, 380)), array(array(50, 312), array(460, 337), array(35, 192)), array(array(218, 323), array(385, 355), array(257, 372)), array(array(259, 12), array(379, 60), array(30, 391)), array(array(229, 62), array(159, 116), array(451, 351)), array(array(51, 389), array(426, 63), array(401, 164)));

  private $stable_set = array(array(array(391, 41), array(216, 359), array(395, 193)), array(array(486, 420), array(466, 135), array(48, 26)), array(array(77, 378), array(218, 284), array(101, 337)), array(array(17, 46), array(151, 56), array(365, 187)), array(array(451, 398), array(119, 210), array(123, 346)), array(array(480, 200), array(18, 58), array(163, 93)), array(array(115, 72), array(67, 147), array(76, 253)), array(array(23, 28), array(369, 459), array(24, 30)), array(array(154, 238), array(467, 70), array(310, 310)), array(array(47, 391), array(148, 373), array(38, 126)), array(array(281, 293), array(134, 442), array(28, 68)), array(array(196, 412), array(444, 339), array(304, 208)), array(array(14, 381), array(248, 59), array(194, 65)), array(array(302, 153), array(253, 50), array(22, 320)), array(array(254, 421), array(291, 307), array(450, 150)), array(array(76, 358), array(489, 417), array(96, 438)), array(array(94, 322), array(203, 172), array(357, 266)), array(array(472, 215), array(100, 255), array(419, 377)), array(array(83, 486), array(84, 230), array(32, 399)), array(array(35, 425), array(89, 233), array(175, 236)), array(array(44, 216), array(18, 283), array(221, 415)), array(array(264, 426), array(482, 179), array(18, 329)), array(array(50, 230), array(454, 95), array(53, 165)), array(array(67, 215), array(473, 407), array(217, 122)), array(array(428, 58), array(228, 125), array(188, 159)), array(array(27, 166), array(224, 232), array(336, 184)), array(array(436, 397), array(257, 297), array(167, 38)), array(array(237, 152), array(242, 200), array(252, 74)), array(array(348, 115), array(438, 274), array(26, 142)), array(array(163, 62), array(52, 204), array(431, 228)), array(array(361, 351), array(363, 67), array(427, 305)), array(array(434, 46), array(256, 333), array(263, 59)), array(array(328, 478), array(105, 100), array(94, 196)), array(array(43, 236), array(379, 412), array(248, 230)), array(array(347, 119), array(193, 213), array(98, 56)), array(array(437, 319), array(434, 366), array(263, 222)), array(array(340, 30), array(42, 217), array(206, 132)), array(array(367, 14), array(142, 80), array(418, 272)), array(array(288, 255), array(363, 115), array(201, 424)), array(array(165, 353), array(21, 269), array(375, 230)), array(array(309, 341), array(144, 310), array(36, 277)), array(array(149, 207), array(426, 247), array(34, 439)), array(array(426, 423), array(260, 418), array(118, 450)), array(array(89, 154), array(125, 240), array(275, 406)), array(array(430, 321), array(167, 177), array(252, 84)), array(array(106, 64), array(466, 431), array(23, 193)), array(array(215, 192), array(480, 472), array(474, 272)), array(array(76, 347), array(113, 369), array(99, 460)));

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
