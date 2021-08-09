$.ajaxSetup({
beforeSend: function (xhr, settings) {
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie != '') {
	var cookies = document.cookie.split(';');
	for (var i = 0; i < cookies.length; i++) {
	var cookie = jQuery.trim(cookies[i]);
	if (cookie.substring(0, name.length + 1) == (name + '=')) {
	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	break;
	}
	}
}
return cookieValue;
}
if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
}
}
});

$(document).on("click", ".post-like", function () {
	var id = $(this).data('id');
	$.ajax({
	  type: "post",
	  url: "/like/",
	  data: {
		id: id,
		csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
	  },
	  success: function (data) {
		$("#post-like-" + id).removeClass("post-like text-info").addClass("post-liked disabled text-secondary");
		var like_count = data["like_count"]
		$("#like-count-" + id).html(like_count);
		// alert(data["message"])
	  }
	});
});

$(document).on("click", ".post-notate", function () {
var id = $(this).data('id');
$.ajax({
	type: "post",
	url: "/accounts/notation/",
	data: {
		id: id,
		csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
	},
	success: function (data) {
		$("#post-notate-" + id).removeClass("btn-outline-secondary post-notate").addClass("btn-outline-success post-disnotate");
		$("#post-notate-" + id).html("<i class=\"fas fa-bell\"></i> 通知ON");
		alert(data["message"])
	}
});
});

$(document).on("click", ".post-disnotate", function () {
var id = $(this).data('id');
$.ajax({
	type: "post",
	url: "/accounts/notation/",
	data: {
		id: id,
		csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
	},
	success: function (data) {
		$("#post-notate-" + id).removeClass("btn-outline-success post-disnotate").addClass("btn-outline-secondary post-notate");
		$("#post-notate-" + id).html("<i class=\"fas fa-bell-slash\"></i> 通知OFF");
		alert(data["message"])
	}
});
});
