<!DOCTYPE html>
<html>
	<head>
		
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
		<link rel="stylesheet" type="text/css" href="result.css">
		<?php include 'navbar.php'; ?>
	</head>
<?php
	$place="./data/";
	
	$hit = file_get_contents($place.'HIT_cilin_utf8CT_zhconv.json');
	$hitindex = file_get_contents($place.'hit_index.json');
	
	$subindex = file_get_contents($place.'random_sub_index.json');
	$signindex=file_get_contents($place.'random_sign_index.json');
	$videoinfo = file_get_contents($place.'after_alignment5.json');
	$videoinfo = str_replace("{}", "null", $videoinfo);
	
	$C=file_get_contents($place.'compound_clear.json');//複合詞
	$NC=file_get_contents($place.'NOTcompound_clear.json');//非複合詞//暫無用到
	$C_expand=file_get_contents($place.'BK_same_C_expand.json');//複合詞-擴增     //同義
	$NC_expand=file_get_contents($place.'BK_same_NC_expand.json');//非複合詞-擴增	//同義
	
	
	
	$S2Name=$_POST["S2"];
	$GLOBALS['searchword']=$S2Name;
	
	$GLOBALS['ans']=array();//已出現過的sentense  1-1'1-2
	$GLOBALS["done"]=array();    //已出現過的word
	$GLOBALS['out']=array();//final
	$GLOBALS['keep']=array();//暫存手語同義(可能重複)
	
	$GLOBALS['matchingVideos']=array();
	$GLOBALS['allsub']=array(); //中文
	$GLOBALS['allsub_h']=array(); //手語
	$GLOBALS['ishand'] = true;
	
	$GLOBALS['iscompound'] = false;
	$GLOBALS['isvague'] = false;
	
	//////////特殊字///
	$GLOBALS['specialtext_compound'] = array();
	

	
	/////////function////////////////////////////////////////////
	function find_compound($wantCompound){
		$videos = json_decode($GLOBALS['videoinfo'], true); // 用來比對字幕裡是否出現複合詞

		foreach ($videos as $video) {
			$video_sign = $video["sign"];
			if(is_null($video_sign)){}
			else foreach ($video_sign as $video_signId => $video_signId_bk) {
				$breaktext = $video_signId_bk["breaktext"];
				$allFound = true; // 假設 "breaktext" 中包含了 $wantCompound 中的所有元素

				// 檢查 $wantCompound 中的所有元素是否都至少出現在 "breaktext" 中
				foreach ($wantCompound as $want) {
					$found = false; // 假設 $wantCompound 中的某個元素未在 "breaktext" 中找到
					foreach ($breaktext as $text) {
						if (strpos($text, $want) !== false) {
							$found = true; // 如果 "breaktext" 中包含 $wantCompound 中的元素，則將 found 設為 true
							break;
						
						}
					}
					if (!$found) {
						$allFound = false; // 如果 "breaktext" 中未包含 $wantCompound 中的某個元素，則將 allFound 設為 false
						break;
					}
				}
				// 如果 "breaktext" 中包含了 $wantCompound 中的所有元素
				if ($allFound) {
					preg_match('/^(.*?)_[zs]_(.*?)$/', $video_signId, $matches);
					list(,$videoid, $subnum) = $matches;//subnum_第幾個
					//print("123123=".$subnum."<br>");
					if(isset($GLOBALS['ans'][$videoid])){
						array_push($GLOBALS['ans'][$videoid],$video_signId);
					} 
					else {
						$GLOBALS['ans'][$videoid] = [$video_signId];
					}
					//print( "在 'breaktext' 中找到了包含 \$wantCompound 中的所有元素：" . implode(", ", $wantCompound) . "<br>");
					//print ("相應的 sign ID 為：" . $video_signId . "<br>");
					//print( "<br>");
				}
			}
		}
	}
	
	function find_sub($want) {
		$sub_index=json_decode($GLOBALS['subindex']);
		$videos=json_decode($GLOBALS['videoinfo']);
		foreach ($sub_index as $key => $value){//key:word,value:videoid
			if($key==strtoupper($want)){	
				foreach($value as $index=>$subid){//index:videoid,
					if(isset($GLOBALS['ans'][$index])){
						foreach($subid as $id){
							if(!in_array($id, $GLOBALS['ans'][$index])){
								array_push($GLOBALS['ans'][$index],$id);
							}
						}
					}
					else{
						$GLOBALS['ans'][$index]=$subid;
					}
				}			
				break;
			}
		}		
	}
	function find_sign($want) {
		$sign_index=json_decode($GLOBALS['signindex']);
		$videos=json_decode($GLOBALS['videoinfo']);
		foreach ($sign_index as $key => $value){//key:word,value:videoid
			if($key==strtoupper($want)){	
				foreach($value as $index=>$subid){//index:videoid,
					if(isset($GLOBALS['ans'][$index])){
						foreach($subid as $id){
							if(!in_array($id, $GLOBALS['ans'][$index])){	
								array_push($GLOBALS['ans'][$index],$id);
							}
						}
					}
					else{
						$GLOBALS['ans'][$index]=$subid;
					}
				}			
				break;
			}
		}		
	}
	function across_array(){
		$i=0;
		do{
			$yes=0;
			foreach($GLOBALS['ans'] as $key=>$value){
				if(isset($GLOBALS['ans'][$key][$i])){
					//print($GLOBALS['ans'][$key][$i]);
					array_push($GLOBALS['out'],$GLOBALS['ans'][$key][$i]);
					$yes=1;
				}
			}
			$i++;
		}while($yes==1);
		//echo nl2br(print_r($GLOBALS["out"], true));
	}
	function sub($handorchinese){
		$videos=json_decode($GLOBALS['videoinfo']);
		//echo nl2br(print_r($GLOBALS["ans"], true));
		if ($GLOBALS['ishand']) {//手語為主
			foreach($GLOBALS['out'] as $subid ){//#讓關鍵字變色
				//list($channel,$videoid, $ZorS,$subnum) = explode("_", $subid);
				preg_match('/^(.*?)_[zs]_(.*?)$/', $subid, $matches);
				list(,$videoid, $subnum) = $matches;//subnum_第幾個
				//print("@@= ".$subnum."</br>");
				$video = $videos->$videoid;
				$videoUrl = $video->url;
				$ytvid = substr($videoUrl, strpos($videoUrl, 'v=') + 2);

				/////////找關鍵字/////
				$searchss = '';  // 初始化為空字符串
				$searchzz = '';  // 初始化為空字符串
				try {
					foreach ($video->alignment as $alignmentItem) {
						if ($alignmentItem->s === $subid) {
							// 檢查是否要匹配所有搜尋內容或特定內容
							if ($GLOBALS['isvague']) {
								foreach ($GLOBALS["done"] as $ok) {
									// 檢查 "s_words[0]" 是否與任何搜尋內容匹配
									if ($alignmentItem->s_words[0] == $ok) {
										// 印出匹配的 "s_words" 和對應的 "z_words"
										$searchss = implode("/", $alignmentItem->s_words);  // 手語
										$searchzz = implode("/", $alignmentItem->z_words);  // 中文
										// 印出匹配後的結果
										//echo 'Matched s_words22: ' . $searchss . '<br>';
										//echo 'Corresponding z_words22: ' . $searchzz . '<br>';
									}
									
								}
							} 
							else {
								// 檢查 "s_words[0]" 是否與指定值 ($GLOBALS['searchword']) 匹配
								if ($alignmentItem->s_words[0] == $GLOBALS['searchword']) {
									// 印出匹配的 "s_words" 和對應的 "z_words"
									//echo '實際: ' . $alignmentItem->s_words. '<br>';
									//echo '實際2: ' . $alignmentItem->z_words . '<br>';
									$searchss = implode("/", $alignmentItem->s_words);  // 手語
									$searchzz = implode("/", $alignmentItem->z_words);  // 中文

									// 印出匹配後的結果
									
									//echo 'Matched s_words: ' . $searchss . '<br>';
									//echo 'CMatched  z_words: ' . $searchzz . '<br>';
								}
								
							}

							
						}
					}
					///////////////////////////
					if (!isset($GLOBALS['allsub'][$videoid])){
						foreach ($video->subtitles as $manywords) {//該影片，所有字幕
							//$allsub[]
							$GLOBALS['allsub'][$videoid][] = [
								't' => $manywords->text, //
								'start' => $manywords->start_time,
								'end' => $manywords->end_time
							];
							
						}
						if(is_null($video->sign)){
							$tempStartTime = reset($video->subtitles)->start_time;
								$tempEndTime = end($video->subtitles)->end_time;
								//print("5555=".$tempStartTime."</br>"."666=".$tempEndTime."</br>");
								$GLOBALS['allsub_h'][$videoid][] = [
									't_h' => '',
									'start_h' => $tempStartTime,
									'end_h' => $tempEndTime
								];
						}
						else foreach ($video->sign as $manywords_hand){
							if (empty($video->sign)){
								$tempStartTime = reset($video->subtitles)->start_time;
								$tempEndTime = end($video->subtitles)->end_time;
								//print("5555=".$tempStartTime."</br>"."666=".$tempEndTime."</br>");
								$GLOBALS['allsub_h'][$videoid][] = [
									't_h' => '',
									'start_h' => $tempStartTime,
									'end_h' => $tempEndTime
								];
							}
							else{
								try{
									$GLOBALS['allsub_h'][$videoid][] = [
										't_h' => implode('/', $manywords_hand->breaktext),
										'start_h' => $manywords_hand->start_time,
										'end_h' => $manywords_hand->end_time
									];
								}
								catch(Exception $e){
									$tempStartTime = reset($video->subtitles)->start_time;
									$tempEndTime = end($video->subtitles)->end_time;
									//print("5555=".$tempStartTime."</br>"."666=".$tempEndTime."</br>");
									$GLOBALS['allsub_h'][$videoid][] = [
										't_h' => '',
										'start_h' => $tempStartTime,
										'end_h' => $tempEndTime
									];
								}
							}	
						}
					}
					//$matchingVideos[]
					$GLOBALS['matchingVideos'][]= [
						'subid'=>$subid,
						'videoid'=>$videoid,
						'url'=> $ytvid,
						'startTime' => $video->sign->$subid->start_time,
						'endTime' => $video->sign->$subid->end_time,
						'text' => $video->sign->$subid->text,
						'search_s'=>$searchss,
						'search_z'=>$searchzz
						
					];
					//print($video->subtitles->$subid->text."<br/>");
					//print("videos url:".$ytvid."<br/>");	
						
				}
				catch (Exception $e) {
					echo 'Error: ' . $e->getMessage();
				}
				if (empty($searchss) || empty($searchzz)) {
					$searchss = '**';
					$searchzz = '**';
					//print("5555=".$subid."</br>");
					//echo 'Matched s_words3: ' . $searchss . '<br>';
					//echo 'Corresponding z_words3: ' . $searchzz . '<br>';
				}
			}
		}
		else{//中文為主
			foreach($GLOBALS['out'] as $subid ){//#讓關鍵字變色
				//list($channel,$videoid, $ZorS,$subnum) = explode("_", $subid);
				preg_match('/^(.*?)_[zs]_(.*?)$/', $subid, $matches);
				list(,$videoid, $subnum) = $matches;//subnum_第幾個
				//print("@@= ".$subnum."</br>");
				$video = $videos->$videoid;
				$videoUrl = $video->url;
				$ytvid = substr($videoUrl, strpos($videoUrl, 'v=') + 2);
				
				/////////找關鍵字/////
				$searchss = '';  // 初始化為空字符串
				$searchzz = '';  // 初始化為空字符串
				try {
					foreach ($video->alignment as $alignmentItem) {
						//print("5555=".$subid."\n");
						if ($alignmentItem->z == $subid) {
							// 檢查是否要匹配所有搜尋內容或特定內容 模糊
							if ($GLOBALS['isvague']) {
								foreach ($GLOBALS["done"] as $ok) {
									// 檢查 "s_words[0]" 是否與任何搜尋內容匹配
									if ($alignmentItem->z_words[0] == $ok) {
										// 印出匹配的 "s_words" 和對應的 "z_words"
										$searchss = implode("/", $alignmentItem->s_words);  // 手語
										$searchzz = implode("/", $alignmentItem->z_words);  // 中文
										// 印出匹配後的結果
										//echo 'Matched s_words22: ' . $searchss . '<br>';
										//echo 'Corresponding z_words22: ' . $searchzz . '<br>';
									}
								}
							} 
							else {
								// 檢查 "s_words[0]" 是否與指定值 ($GLOBALS['searchword']) 匹配
								if ($alignmentItem->z_words[0] == $GLOBALS['searchword']) {
									// 印出匹配的 "s_words" 和對應的 "z_words"
									//echo '實際: ' . $alignmentItem->s_words. '<br>';
									//echo '實際2: ' . $alignmentItem->z_words . '<br>';
									$searchss = implode("/", $alignmentItem->s_words);  // 手語
									$searchzz = implode("/", $alignmentItem->z_words);  // 中文
									// 印出匹配後的結果
									//echo 'z_words='.$alignmentItem->z.'<br>';
									//echo 'Matched s_words: ' . $searchss . '<br>';
									//echo 'Corresponding z_words: ' . $searchzz . '<br>';
								}
							}   
						}
					}
				} 
				catch (Exception $e) {
					echo 'Error: ' . $e->getMessage();
				}
				if (empty($searchss) || empty($searchzz)) {
					$searchss = '**';
					$searchzz = '**';
					//print("5555=".$subid."\n");
					//echo 'Matched s_words3: ' . $searchss . '<br>';
					//echo 'Corresponding z_words3: ' . $searchzz . '<br>';
				}

				//////////////////////////////////
				
				if (!isset($GLOBALS['allsub'][$videoid])){
					
				
					foreach ($video->subtitles as $manywords) {//該影片，所有字幕
						//$allsub[]
						$GLOBALS['allsub'][$videoid][] = [
							't' => $manywords->text, //
							'start' => $manywords->start_time,
							'end' => $manywords->end_time
						];
						
					}
					if(is_null($video->sign)){
						$tempStartTime = reset($video->subtitles)->start_time;
						$tempEndTime = end($video->subtitles)->end_time;
						$GLOBALS['allsub_h'][$videoid][] = [
							't_h' => '',
							'start_h' => $tempStartTime,
							'end_h' => $tempEndTime
						];
					}
					
					else foreach ($video->sign as $manywords_hand){
						if (empty($video->sign)){
								$tempStartTime = reset($video->subtitles)->start_time;
								$tempEndTime = end($video->subtitles)->end_time;
								$GLOBALS['allsub_h'][$videoid][] = [
									't_h' => '',
									'start_h' => $tempStartTime,
									'end_h' => $tempEndTime
								];
						}
						else{
								$GLOBALS['allsub_h'][$videoid][] = [
									't_h' => implode('/', $manywords_hand->breaktext),
									'start_h' => $manywords_hand->start_time,
									'end_h' => $manywords_hand->end_time
								];
							//print("start_h".$manywords_hand->start_time."<br/>");
							//print("end_h".$manywords_hand->end_time."<br/>");
							//print("text:".implode('/', $manywords_hand->breaktext)."<br/>");
						}
					}
				}
				////////////////////////////
				//$matchingVideos[]
				$GLOBALS['matchingVideos'][]= [
					'subid'=>$subid,
					'videoid'=>$videoid,
					'url'=> $ytvid,
					'startTime' => $video->subtitles->$subid->start_time,
					'endTime' => $video->subtitles->$subid->end_time,
					'text' => $video->subtitles->$subid->text,
					'search_s'=>$searchss,
					'search_z'=>$searchzz
					
				];
				//print($video->subtitles->$subid->text."<br/>");
				//print("videos url:".$ytvid."<br/>");	
					
			}
		}	
	}
	//////////////////////////////////////////////////////////////
	
	
	
	if(!empty($_POST['signlanguage'])){
		$sl=$_POST["signlanguage"];
		//print_r($sl);
	}
	
	if (isset($_POST["signlanguage"])) {
		//print_r($_POST["signlanguage"]);
        if ($_POST['signlanguage'][0] =='chinese_acc') { //中文精準
            $GLOBALS['ishand'] = false;
			array_push($GLOBALS["done"],$S2Name);
			find_sub($S2Name);
			#echo nl2br(print_r($GLOBALS['ans'], true));
        } 
		elseif ($_POST['signlanguage'][0] == 'chinese_vague') { //中文同義 //模糊
			$GLOBALS['ishand'] = false;
			$GLOBALS['isvague'] = true;
			$hitword_index=json_decode($hitindex);
			$hitid_index=json_decode($hit);
			$ids=$hitword_index->$S2Name;
			foreach($ids as $id){
				foreach($hitid_index->$id as $word){
					if(!in_array($word,$GLOBALS["done"])){
						find_sub($word);
						array_push($GLOBALS['keep'],$word);
					}
				}
			}
			$uniqueValues = array_unique($GLOBALS['keep']);
			// 存儲沒有重複的值到 $GLOBALS["done"]
			$GLOBALS["done"] = $uniqueValues;
        }
		elseif ($_POST['signlanguage'][0] == 'hand_acc') {	//手語精準
            $C_data = json_decode($C, true);       //複合詞
			//$NC_data = json_decode($NC, true);     //非複合詞
			
			find_sign($S2Name);
			array_push($GLOBALS["done"],$S2Name);
			
			foreach ($C_data as $key => $value) {
				if (in_array($S2Name, $value['word'])) {
					//print($S2Name . "  為複合詞" . "</br>");
					$GLOBALS['iscompound'] = true;
					//print("Word: ". implode(", ", $value['word']) ."</br>");
					foreach ($value['compounds'][0] as $compound) {
						//print( $compound . ",");
						$wantCompound[] = $compound;
					}
					array_push($GLOBALS['specialtext_compound'],implode("/", $value['compounds'][0]));
					
					//print("Compound: ". implode("/", $value['compounds'][0]) ."</br>");
					find_compound($wantCompound);
				}
			}
        }
		elseif ($_POST['signlanguage'][0] == 'hand_vague') {//手語模糊
			$GLOBALS['isvague'] = true;
			$C_expand_index = json_decode($C_expand); 
			$NC_expand_index = json_decode($NC_expand);
			$C_data = json_decode($C, true); //複合詞
			
			find_sign($S2Name);
			array_push($GLOBALS["done"],$S2Name);
			
			// C_expand_index
			foreach ($C_expand_index as $word) {
				// Check if any "original" value contains $S2Name
				if (isset($word->original) && in_array($S2Name, $word->original)) {
					//find_sign($word);
					//printOriginalValues($word);
					foreach ($word->original as $need) {
						foreach ($C_data as $key => $value) {
							if (in_array($need, $value['word'])) {
								$GLOBALS['iscompound'] = true;
								//print("Word: ". implode(", ", $value['word']) ."</br>");
								foreach ($value['compounds'][0] as $compound) {
									//print( $compound . ",");
									$wantCompound[] = $compound;
								}
								array_push($GLOBALS['specialtext_compound'],implode("/", $value['compounds'][0]));
								//print("Compound: ". implode("/", $value['compounds'][0]) ."</br>");
								find_compound($wantCompound);
							}
						}
						
						//find_sign($need);
						//array_push($GLOBALS["done"],$need);
					}
				}
			}

			// Loop through NC_expand_index
			foreach ($NC_expand_index as $word) {
				// Check if any "original" value contains $S2Name
				if (isset($word->original) && in_array($S2Name, $word->original)) {

					foreach ($word->original as $need) {
						find_sign($need);
						array_push($GLOBALS['keep'],$need);
					}
				}
			}
			
			$uniqueValues = array_unique($GLOBALS['keep']);
			// 存儲沒有重複的值到 $GLOBALS["done"]
			$GLOBALS["done"] = $uniqueValues;
			
		}


 
    } 
	else {//未選擇
		//echo '<script>alert("請選擇搜尋類型");</script>';
		//echo '<script>window.location.href = "search.php";</script>';
		//exit; 
		$GLOBALS['ishand'] = false;
		array_push($GLOBALS["done"],$S2Name);
		find_sub($S2Name);
    }

	across_array();
	//echo nl2br(print_r($GLOBALS["done"], true));
	sub($GLOBALS['ishand']);	//存取影片資訊
	//echo nl2br(print_r($GLOBALS["ans"], true));
	//echo nl2br(print_r($GLOBALS["out"], true));
	if (empty($GLOBALS['out'])) {
		echo '<script>alert("找不到與您搜尋字詞相符的資料");</script>';
		echo '<script>window.location.href = "search.php";</script>';
		exit;
	}
	
	// 將 matchingVideos，all 傳到JavaScript
		echo '<script src="result.js"></script>';
		echo '<script>';
		echo 'var matchingVideos = ' . json_encode($matchingVideos) . ';';
		echo 'var allsub = ' . json_encode($allsub) . ';';
		echo 'var allsub_h = ' . json_encode($allsub_h) . ';';
		echo 'var S2Name = ' . json_encode($S2Name) . ';';
		echo 'var specialtext = ' . json_encode($done) . ';';
		echo 'var specialtext_compound = ' . json_encode($specialtext_compound) . ';';
		
		echo '</script>';
		//echo'<div style="display: flex; align-items: center;"><h2 class="outputtext">搜尋內容為 <label class="wanttext">'.$S2Name.'</label><span id="howmanytext" class="howmanytext"></span></h2></div>';
		echo'<div><h2 class="outputtext">搜尋內容為  <label class="wanttext">'.$S2Name.'</label><span id="howmanytext" class="howmanytext"></span></h2></div>';
		//echo '<span id="howmanytext" class="howmanytext"></span>';//幾筆結果
		
		
		if($GLOBALS['iscompound']){
			//echo'<h2 class="compoundtext"><label class="wanttext">'.$S2Name.'</label>為複合詞</h2>';
			//echo '<h3>手語由以下組成:' . implode('/', $wantCompound) . '</h3>';
			
		}
		
		
		echo '<div id="vv"></div></br>
				中文字幕: <span id="words" class="word"><p></p></span></br>
				手語字幕: <span id="hand_words" class="word"><p></p></span>';
				
		echo '<div class="btnbox">
				<input class="videobtn" type="button" value="上一部" onclick="control(\'up\');">
				<input class="videobtn" type="button" value="下一部" onclick="control(\'down\');">
			</div><br>';
		
		if($GLOBALS['isvague']){
			echo '<h7>查詢內容包含:' . implode('/',$GLOBALS["done"]) . '</h7>';
		}
	
	
?>
		
</html>