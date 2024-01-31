var tag = document.createElement('script')   ;
    tag.src = "https://www.youtube.com/iframe_api";

var firstScriptTag = document.getElementsByTagName('script')[0];
	firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
	
var videoIndex = 0; // 目前影片在清單中的索引
var player;

function onYouTubeIframeAPIReady() {
	player = new YT.Player('vv', {
		height: '390',
		width: '640', 
		events: {'onReady': onPlayerReady}});
}
function onPlayerReady() {
	updateVideo();
	updateDisplayInfo();
	var textt = document.getElementById('words');
	var hand_textt = document.getElementById('hand_words');
	
	
	var videoData = matchingVideos[videoIndex];//沒用到
	
	var subtitles_id = videoData.id;
		
    var currentSubtitle = null;
	var currentSubtitle_h = null;
	setInterval(
		function () {
			var currentTime = Math.round(player.getCurrentTime() * 10) / 10;
			//console.log(allsub[matchingVideos[videoIndex].videoid]);
			//中文
			for(index in allsub[matchingVideos[videoIndex].videoid]){
				var subinfo = allsub[matchingVideos[videoIndex].videoid][index];//該字幕的開始結束
				//console.log(subinfo);
				if (currentTime >= subinfo.start && currentTime <= subinfo.end) {
					currentSubtitle = subinfo.t;
					//////////////////////////////////
					textt.innerHTML = '<span class="subtext">' + currentSubtitle + '</span>';
					//console.log(currentTime);
						break;
				}
				

			}
			if (currentSubtitle !== null) {
				//console.log(currentSubtitle);
				//console.log(specialtext)
				////////////////////////////////////////////////////特殊關鍵字
				Object.values(specialtext).forEach(function(special) {
					var regex = new RegExp(special, 'g');
					if (currentSubtitle.includes(special) && special!=null && special!='') {
						currentSubtitle = currentSubtitle.replace(regex, '<span style="color: red;">' + special + '</span>');
					}
				});		
				//console.log(matchingVideos[videoIndex].search_z);
				if (currentSubtitle.includes(matchingVideos[videoIndex].search_z) && matchingVideos[videoIndex].search_z!=null && matchingVideos[videoIndex].search_z!='') {
					currentSubtitle = currentSubtitle.replace(new RegExp(matchingVideos[videoIndex].search_z, 'g'), '<span style="color: red;">' + matchingVideos[videoIndex].search_z + '</span>');
				}
				
				//////////////////////////////////
				
				
				textt.innerHTML = '<span class="subtext">' + currentSubtitle + '</span>';
				//console.log(currentTime);
			} 
			else {
				currentSubtitle_h = "";
				textt.innerHTML = "";
				//console.log("沒東西");
			}
			//手語
			for(index in allsub_h[matchingVideos[videoIndex].videoid]){
				var subinfo = allsub_h[matchingVideos[videoIndex].videoid][index];//該字幕的開始結束
				console.log(subinfo);
				console.log(currentTime);
				if (currentTime >= subinfo.start_h && currentTime <= subinfo.end_h) {
					console.log(specialtext);
					currentSubtitle_h = subinfo.t_h;
					/////////////////////////////////////////////////////////////
					console.log(currentSubtitle_h);
					hand_textt.innerHTML = '<span class="subtext">' + currentSubtitle_h + '</span>';
					//console.log(currentTime);
					break;
				}
			}
			if (currentSubtitle_h !== null) {
				//console.log(currentSubtitle_h);
				////////////////////////////////////////////////////特殊關鍵字
				Object.values(specialtext).forEach(function(special) {
				  var regex2 = new RegExp(special, 'g');
				  if (currentSubtitle_h.includes(special) && special!=null && special!='') {   
					currentSubtitle_h = currentSubtitle_h.replace(regex2,'<span style="color: red;">' + special + '</span>');
				  }
				});
				Object.values(specialtext_compound).forEach(function(specialtext_compound2) {
				  var regex2 = new RegExp(specialtext_compound2, 'g');
				  if (currentSubtitle_h.includes(specialtext_compound2) && specialtext_compound2!=null && specialtext_compound2!='') {   
					currentSubtitle_h = currentSubtitle_h.replace(regex2,'<span style="color: green;">' + specialtext_compound2 + '</span>');
				  }
				});
				if (currentSubtitle_h.includes(matchingVideos[videoIndex].search_s)&&matchingVideos[videoIndex].search_s!=null && matchingVideos[videoIndex].search_s!='') {//特殊關鍵字
					//console.log("matchingVideos="+matchingVideos[videoIndex].search_s);
					currentSubtitle_h = currentSubtitle_h.replace(new RegExp(matchingVideos[videoIndex].search_s, 'g'), '<span style="color: red;">' + matchingVideos[videoIndex].search_s + '</span>');
				}
				/////////////////////////////////////////////////////////////
				hand_textt.innerHTML = '<span class="subtext">' + currentSubtitle_h + '</span>';
				//console.log(currentTime);
			} else {
				hand_textt.innerHTML = "";
				console.log("沒東西456");
			}
		}, 500);
		
}

function control(action) {
    if (action === 'up') {
        videoIndex = (videoIndex - 1 + matchingVideos.length) % matchingVideos.length;
    } else if (action === 'down') {
        videoIndex = (videoIndex + 1) % matchingVideos.length;
    }
    updateVideo();
	updateDisplayInfo();
}

function updateVideo() {
	//console.log(videoIndex);
    var videoData = matchingVideos[videoIndex];
    var startTimeInSeconds = Math.floor(videoData.startTime);
    // 構建影片連結，加入起始時間
	player.loadVideoById({
        'videoId': videoData.url,
        'startSeconds': startTimeInSeconds
    });
    
}
       
function updateDisplayInfo() {
    console.log('Updating display information...');
    var howManyText = document.getElementById('howmanytext');
    console.log('howManyText:', howManyText);
    howManyText.innerHTML = '<h5>'+(videoIndex + 1) + ' / ' + matchingVideos.length + ' 筆</h5>';
}


