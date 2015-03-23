$(function(){

	$('#user').blur(function(){
		$.ajax({
			type: 'POST',
			url: '/social/checkuser/',
			data : {
				'user' : $('#user').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: checkuseranswer,
			dataType: 'html'
		});
	});

});

function checkuseranswer(data, textStatus, jqHXR)
{
	$('#info').html(data);
}

function getMessages(view) {
  if (view != 'None') {
    url = "/social/messages.json/?view=" + view 
  }
  else {
    url = "/social/messages.json/"
  }
  $.ajax({
    type: 'GET',
    url: url,
    success: displayMessages,
    dataType: 'json'
  });
}
function displayMessages(data) {
  json = JSON.parse(data);
  json.map(function(message) {
    console.log(message);
    /*$('body').append("<p>" + message.fields.text + "</p>");*/
  });
}

