<?php
echo "<h1> zpracování formuláře </h1> \n";



$prijmeni = $_POST["prijmeni"];
$jmeno = $_POST["jmeno"];
$heslo = $_POST["heslo"];
$barva = $_POST["barva"];
$email = $_POST["email"];
$datum = $_POST["datum"];
$vek = $_POST["vek"];
$zajmy = $_POST["zajmy"];
$poznamka = $_POST["poznamka"];

$dekujeme = "Formulář odeslán, děkujeme";

/* testing formuláře
echo $prijmeni."<br>\n"; 
echo $jmeno."<br>\n";
echo $heslo."<br>\n";
echo $barva."<br>\n";
echo $email."<br>\n";
echo $datum."<br>\n";
echo $vek."<br>\n";
echo $zajmy."<br>\n";
echo $poznamka."<br>\n";
*/

echo $dekujeme."<br>\n";

$SQL = "INSERT INTO registrace (ID, jmeno, prijmeni, vek, heslo, barva, email, datum, zajmy, poznamka) VALUES (NULL, '$jmeno', '$prijmeni', '$vek', '$heslo', '$barva', '$email', '$datum', '$zajmy', '$poznamka');";

$spojeni = mysqli_connect("localhost", "root",  "");
mysqli_select_db($spojeni,"skoleni");
mysqli_query($spojeni,$SQL);
mysqli_close($spojeni);




?>
