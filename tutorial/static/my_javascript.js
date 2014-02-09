window.onload = function () {
	index = 0;
	document.getElementById("image"+index).style.display = '';	
	console.log(images_str);
	var images = JSON.parse(images_str);
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
		document.getElementById("image"+index).style.display = 'None'
		index++;
		document.getElementById("image"+index).style.display = ''
	};
}

function previous_img () {
	// $('.fade').fadeIn();
	if (index > 0) {
		document.getElementById("image"+index).style.display = 'None'
		index--;
		document.getElementById("image"+index).style.display = ''
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