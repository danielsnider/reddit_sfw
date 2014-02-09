window.onload = function () {
	index = 0;
	// document.getElementById("image"+index).style.display = '';	
	var images = JSON.parse(images_str);
	console.log(images[0]);
	console.log(images[0].url);
	document.getElementById("image").src = images[0].url;
	document.getElementById("title").href = "https://www.google.com/search?q=" + images[0].title;
	document.getElementById("title").innerHTML = images[0].title;
	document.getElementById("comments").href = "http://reddit.com" + images[0].permalink;
	document.getElementById("comments").innerHTML = images[0].ups + " Upvotes, " + images[0].num_comments + " Comments";
	document.getElementById("subreddit").href = "/r/" + images[0].subreddit;
	document.getElementById("subreddit").innerHTML = images[0].subreddit;
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
	// if (index < length-1) {
	// 	document.getElementById("image"+index).style.display = 'None'
	// 	index++;
	// 	document.getElementById("image"+index).style.display = ''
	// };
}

function previous_img () {
	// $('.fade').fadeIn();
	// if (index > 0) {
	// 	document.getElementById("image"+index).style.display = 'None'
	// 	index--;
	// 	document.getElementById("image"+index).style.display = ''
	// };
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