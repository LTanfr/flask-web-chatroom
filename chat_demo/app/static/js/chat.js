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
        $("#messages").append(data.message_html);
        flask_moment_render_all();
        scrollToBottom();
    })

    socket.on('user count', function(data) {
        $('#user-count').html(data.count)
    })

    function new_message(e) {
        let $input = $("#my_message");
        let message = $input.val().trim()
        if(e.which === ENTER_KEY && !e.shiftKey && message)
        {
            e.preventDefault();
            socket.emit('new message', message);
            $input.val('');
        }
    }
    $("#my_message").on('keydown', new_message.bind(this));

    $('#send_button').on('click', function() {
        let $message = $("#my_message")
        if($message.val().trim() !== '')
        {
            socket.emit('new message', $message.val().trim());
            $message.val('');
        }
    })

});