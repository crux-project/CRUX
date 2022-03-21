<?php
  
    header("Access-Control-Allow-Origin: *");
    header("Access-Control-Allow-Methods: PUT, GET, POST");
    header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
        
    $folderPath = "C:/Users/Abhishek/CRUX_Website/upload/";
   
    $file_tmp = $_FILES['file']['tmp_name'];
    $tmp = explode('.',$_FILES['file']['name']);
    $file_ext = strtolower(end($tmp));
    $file = $folderPath . uniqid() . '.'.$file_ext;
    move_uploaded_file($file_tmp, $file);
    
?>