window.onload = function () {
	once = true;
	index = 0;
	images = JSON.parse(images_str);
	length = images.length; 
	showImage(index);
		console.log(document.URL);
	// if (document.URL == "http://dsnider.no-ip.info/" || once == true) { 
	// 	once = false;
		document.getElementById("image").style.paddingTop = "0px"; 	
	// }

}

$('body').keydown(function (e) {
	if(e.keyCode == 39){ // right arrow key
		next_img();
	}
});

$('body').keydown(function (e) {
	if(e.keyCode == 37){ // left arrow key
		previous_img();	
	}
});

$(function () {
	// Fade out when mouse cursor is inactive
	// Source: http://stackoverflow.com/questions/15532423/fade-out-mouse-cursor-when-inactive-with-jquery
	var timer;
	var fadeInBuffer = false;
	$(document).mousemove(function () {
		if (!fadeInBuffer) {
			if (timer) {
				clearTimeout(timer);
				timer = 0;
			}
			$('.fade').fadeIn();
			$('html').css({
				cursor: ''
			});
		} else {
			fadeInBuffer = false;
		}


		timer = setTimeout(function () {
			$('.fade').fadeOut()
			$('html').css({
				cursor: 'none'
			});
			fadeInBuffer = true;
		}, 5000)
	});
});


function next_img () {
	// $('.fade').fadeIn();
	if (index < length-1) {
		index++;
		showImage(index);
	};
}

function previous_img () {
	// $('.fade').fadeIn();
	if (index > 0) {
		index--;
		showImage(index);
	};
}

function addFav (url) {
	$.ajax({
		url: "/favorite",
		type:'POST',
		data: url,
		success: function(msg)
		{
            // alert('Fav sent');
        }               
    });
}

function check_size () {
	//size of div
	var img = document.getElementById('imageid'); 
	var width = img.clientWidth;
	var height = img.clientHeight;

	//image size
	var img = new Image();
	img.onload = function() {
		alert(this.width + 'x' + this.height);
	}
	img.src = 'http://www.google.com/intl/en_ALL/images/logo.gif';

	//jquery
	var imgWidth = $("#imgIDWhatever").width();
}

function showImage (index) {
	document.getElementById("image").style.paddingTop = "0px";
	document.getElementById("image").src = images[index].url;
	// document.getElementById("title").href = "http://reddit.com" + images[index].permalink;
	document.getElementById("title").innerHTML = images[index].title;
	document.getElementById("comments").href = "http://reddit.com" + images[index].permalink;
	document.getElementById("comments").innerHTML = images[index].ups + " Upvotes, " + images[index].num_comments + " Comments";
	document.getElementById("subreddit").href = "/r/" + images[index].subreddit;
	document.getElementById("subreddit").innerHTML = images[index].subreddit;
	if (index != 0) { document.getElementById("buffer-1").src = images[index-1].url; }
	document.getElementById("buffer1").src = images[index+1].url;
	document.getElementById("buffer2").src = images[index+2].url;
	document.getElementById("buffer3").src = images[index+3].url;
	var ih = $("#image").innerHeight();
	var wh = $(window).height();
	var pad = 0;
	var pad = (wh-ih)/2;
	document.getElementById("image").style.paddingTop = pad + "px";		
}

