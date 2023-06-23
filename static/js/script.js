$(() => {
    const socket = io();

    const messageForm = document.getElementById('message-form');
    const chatLog = document.getElementById('sayhi');
    const messageInput = document.getElementById('message');


    socket.emit('join', {}); 

    socket.on('assign_name', function(data) {
        document.querySelector('#username').innerHTML = 'Username: ' + data.username;
        });

    socket.on('chat', function (data) {
        document.querySelector('#messages').innerHTML += '<li>' + data.username + ': ' + data.message + '</li>';
        });



    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = messageInput.value;
        socket.emit('message', message);
        messageInput.value = '';
        });
          
        
        $('#send').click(() => {
            let msg = $('#message').val();
            socket.emit('send_message', { 'message': msg });
            /*$('#messages').append('<li>' + msg + '</li>');*/ // Add this line
            $('#message').val('');
            });

        /*socket.on('receive_message', data => {
        console.log('Message received:', data.message); // Add this line
        $('#messages').append('<li>' + data.message + '</li>');
        });*/

        socket.on('message', (msg) => {
        const chatMessage = document.createElement('p');
        chatMessage.textContent = msg;
        chatLog.appendChild(chatMessage);
        chatLog.scrollTop = chatLog.scrollHeight;
        });



  });

