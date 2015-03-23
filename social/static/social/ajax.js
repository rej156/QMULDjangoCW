$(function(){

	$('#user').blur(function(){
		$.ajax({
			type: 'POST', url: '/social/checkuser/',
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
  // Display messages in reverse chronological order
  JSON
    .parse(data)
    .reverse()
    .map(function(message) {
      var li = "<li>";
      var date = new Date(message.fields.time);
      var author = '<a href=/social/messages/?view=' + message.fields.auth + '>' + message.fields.auth + '</a>'; 
      var recipient = message.fields.recip;
      var text = '"' + message.fields.text + '"';
      var type = (message.fields.private) ? 'whispered' : 'wrote';

      // ADD ERASE!
      li = li + date.toUTCString() + ': ' + author + ' ' + type + ': ' + text + '</p></li>';
      $('#messages ul').append(li);
    });
}

