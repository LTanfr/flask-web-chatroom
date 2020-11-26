$(document).ready(function() {

    var socket = io();

    const ENTER_KEY = 13;
    const username = $("#username")[0].innerText;

    $(window).bind('beforeunload', () => {
        socket.emit('user leave', username);
        socket.disconnect();
    })

    $('.user-list').load(users_list_url, () => {

    });

    function scrollToBottom() {
        let $messages = $("#messages");
        $messages.scrollTop($messages[0].scrollHeight);
    }

    $('#messages').load(messages_url, () => {
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
        if (data.username) {
            if(data.username !== username) {
                $("#messages").append(data.message_x);
            }else {
                $("#messages").append(data.message_y);
            }
        }
        flask_moment_render_all();
        scrollToBottom();
    })

    socket.on('online users', (data) => {
        const user_list = data.users_html
        $('.user-list').html(user_list)
    })

    socket.on('connect', () => {
        socket.emit('user in',username);
    })

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