var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/',function(req, res){
  res.sendFile(__dirname + 'client.html');
});

var count=1;
var client_list = [];

io.on('connection', (socket) => {
  console.log('user connected: ', socket.id);
  var name = "user" + count++;
  io.to(socket.id).emit('change name',name);
  client_list.push(socket.id);
  
  socket.on('disconnect', () => {
    console.log('user disconnected: ', socket.id);
  });
  
  console.log('clients: ', client_list);
  io.emit('receive client list', client_list);
  
  socket.on('send message', (name,text) => {
    var msg = name + ' : ' + text;
    console.log(msg);
    io.emit('receive message', msg);
  });
});

http.listen(3000, () => {
  console.log('server on!');
});

