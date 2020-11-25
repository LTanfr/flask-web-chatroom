$(document).ready(function() {

    var socket = io();

    const ENTER_KEY = 13;

    function scrollToBottom() {
        let $messages = $("#messages");
        $messages.scrollTop($messages[0].scrollHeight);
    }

    $('#messages').load(messages_url, function (){
        scrollToBottom();
    });


    var page = 1;
    function load_messages() {
        let $messages = $('#messages');
        let position = $messages.scrollTop();
        if (position === 0) {
            page++;
            $.ajax({
                url: messages_url,
                type: 'GET',
                data: {page: page},
                success: function (data) {
                    let pre_height = $messages[0].scrollHeight;
                    $(data).prependTo('#messages').hide().fadeIn(800);
                    let next_height = $messages[0].scrollHeight;
                    flask_moment_render_all();
                    $messages.scrollTop(next_height - pre_height);
                },
                error: function () {
                    alert('No more messages.')
                }
            })
        }
    }

    $('#messages').scroll(load_messages);

    socket.on('new message', function (data) {
        if (data.username)
        $("#messages").append(data.message_html);
        flask_moment_render_all();
        scrollToBottom();
    })

    socket.on('user count', function(data) {
        $('#user-count').html(data.count)
    })

    var username = $("#username")[0].innerText;
    function new_message(e) {
        let input = $("#my_message").val().trim();
        let message = {
          'username': username,
          'input': input
        };
        if(e.which === ENTER_KEY && !e.shiftKey && message)
        {
            e.preventDefault();
            socket.emit('new message', message);
            $("#my_message").val('');
        }
    }
    $("#my_message").on('keydown', new_message.bind(this));

    $('#send').on('click', function() {
        let input = $("#my_message").val().trim();
        if(input !== '')
        {
            let message = {
                'username': username,
                'input': input
            };
            socket.emit('new message', message);
            $("#my_message").val('');
        }
    })
});