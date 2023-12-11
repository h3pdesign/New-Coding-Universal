<?php
// Enter your Host, username, password, database below.
// I left password empty because i do not set password on localhost.
$con = mysqli_connect("localhost", "root", "", "allphptricks");
// Check connection
if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

?>

<form name="form" method="get" action="">
    <label><strong>Plattform</strong></label><br />
    <table border="0" width="60%">
        <tr>
            <?php
            $count = 0;
            $sql = mysqli_query($con, "SELECT todo FROM checks");
            foreach ($sql as $row) {
                $count++;
            ?>
                <td width="3%">
                    <input type="checkbox" name="plattform[]" value="<?php echo $row["os_type"]; ?>">
                </td>
                <td width="30%">
                    <?php echo $row["plattform"]; ?>
                </td>
            <?php
                if ($count == 3) { // three items in a row
                    echo '</tr><tr>';
                    $count = 0;
                }
            } ?>
        </tr>
    </table>
    <input type="submit" name="submit" value="Submit">
</form>

<br />



<label>Platform<?= $row['platform'] ?></label></br>
<input type="radio" name="platform" <?= $row['platform'] == "IOS" ? "checked" : "" ?> value="IOS">A
<input type="radio" name="platform" <?= $row['platform'] == "IOS-XE" ? "checked" : "" ?> value="IOS-XE">B

echo<<<js

<script>

    document.querySelector('input[name="rate"]:checked').value;

    </script>


    ?>