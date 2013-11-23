
// Enable pusher logging - don't include this in production
Pusher.log = function(message) {
  if (window.console && window.console.log) {
    window.console.log(message);
  }
};

var pusher = new Pusher('4a1b121857529e74584b');
var channel = pusher.subscribe('message_channel');
channel.bind('new_message', function(data) {
  alert(data.message);
});