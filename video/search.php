<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Search</title>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
		<link rel="stylesheet" type="text/css" href="search.css">
		<?php include 'navbar.php'; ?>
    </head>
	<body>
		<div class="search-container">
			<h1 class="searchtext">查詢</h1>
			
		   <p> 
			<form method="post" action="result.php">
				<lable>
					<input name="S2" type="text" autofocus/>
					<input class="submit_btn" type="submit" value="查詢">
				</lable>
				<fieldset>
				  <legend>選擇搜尋種類("用"的手語>>手、錢)</legend>
				  <div>
					<input type="radio" id="chinese_acc" name="signlanguage[]" value="chinese_acc" />
					<label for="hand_acc">中文_精準比對</label>
				  </div>
				  <div>
					<input type="radio" id="chinese_vague" name="signlanguage[]" value="chinese_vague" />
					<label for="hand_vague">中文_模糊比對</label>
				  </div>
				  
				  <div>
					<input type="radio" id="hand_acc" name="signlanguage[]" value="hand_acc" />
					<label for="hand_acc">手語_精準比對</label>
				  </div>
				  <div>
					<input type="radio" id="hand_vague" name="signlanguage[]" value="hand_vague" />
					<label for="hand_vague">手語_模糊比對</label>
				  </div>
				    
				</fieldset>
			
		   </p>
		</div>
	</body>
	

</html>