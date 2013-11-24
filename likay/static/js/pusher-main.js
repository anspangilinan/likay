var pusher = new Pusher('4a1b121857529e74584b');
var channel = pusher.subscribe('message_channel');
channel.bind('new_post', function(data) {
  var $el = $('<li class="list-group-item"><span class="badge">now</span>' + data.message + '</li>');

  $el.insertBefore(($('.list-group').children('li')[0]))
});