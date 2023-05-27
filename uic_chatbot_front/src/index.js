const path = require('path')
const http = require('http')
const express = require('express')
const socketio = require('socket.io')
const request = require('request')
const Filter = require('bad-words')
const { generateMessage } = require('./utils/messages')
const { addUser, removeUser, getUser, getUsersInRoom } = require('./utils/users')


const app = express()
const server = http.createServer(app)// create webserver can pass express
const io = socketio(server)//calling socketio as a function

const port = process.env.PORT || 3000
const publicDirectoryPath = path.join(__dirname, '../public')

app.use(express.static(publicDirectoryPath))

const botName = 'Bot'

// server (emit) -> client(receive) - countUpdated
//client (emit) -> server(receive) - increment
io.on('connection', (socket) => {
    console.log('New WebSocket connection')
        //socket.emit: emit to particular connection
        //broadcast: emit to everybody, but the that particular connection
        //io.emit: emit to everyone
    socket.on('join',(options, callback) => {
        const {error,user} = addUser({ id: socket.id, ...options })

        if (error) {
            return callback(error)
        }

        socket.join()

        socket.emit('message',generateMessage('Admin','欢迎来到UIC招生问答聊天室，这里你可以和同在讨论室的其他成员进行聊天，也可以在聊天前输入@Bot向机器人就UIC招生问题的进行咨询，祝您体验愉快。\nWelcome to the UIC Admissions Q&A chat room, where you can chat with other members in the same room or type @Bot before chatting to ask the bot questions about UIC admissions. ')) //server emit "message" when new client connects, send"Welcome!" as the event data
        socket.broadcast.emit('message',generateMessage('Admin', `${user.username} 加入了聊天室。\n${user.username} has joined.`))
        io.emit('roomData',{
            room:user.room,
            users:getUsersInRoom()
        })
        callback()
        //    //socket.emit: sends an even t to a specific client
    //    //io.emit: send event to every connected client
    //    //socket.broadcast.emit:send an event to every connected client except socket one
    //    // io.to.emit: send a message to everyone in a room without sending it to people in other rooms
    })
    
    //have server listen for "sendMessage", send message to all connected clients
    
    
    
    socket.on('sendMessage', (message, callback) => {
        const user = getUser(socket.id)
        const filter = new Filter()
        if (filter.isProfane(message)){ //isProfane用来检查是否有脏话存在
            //return callback('profanity is not allowed!') 
            //if error, delete the next 2 line and use the up one line code
            socket.emit('message', generateMessage(botName, '抱歉，脏话是不被允许的!\nThis message has not delivered, profanity not allowed!'))
            return callback()
        }
        
        io.emit('message', generateMessage(user.username, message))
        // Additional processing for messages start with @Bot
        if (message.toLowerCase().startsWith('@bot')) {
            let question = message.substring(4).trim()
            if (question.length === 0) {
                io.emit('message', generateMessage(botName, '请输入内容。\nEmpty request is not allowed.'))
                return callback()
            }
            request('http://127.0.0.1:5000/query-vsbert', {
                method: 'POST',
                json: {
                    "query": question
                }
            }, (err, res, body) => {
                console.log(res)
                let answer
                if (err) { 
                    answer = '抱歉，我们目前连接不上Q&A的服务器。\nSorry, we are unable to reach the Q&A server at the moment.'
                } else if (res.body) {
                    answer = body.answer
                } else {
                    answer = 'The server did not understand you request.'
                }
                io.emit('message', generateMessage(botName, answer))
            })
            return callback()
        }

        return callback('Delivered!')
    })

    socket.on('disconnect',()=>{
        const user = removeUser(socket.id)

        if(user){
            io.emit('message',generateMessage('Admin',`${user.username} has left! `))
            io.emit().emit('roomData',{
                users:getUsersInRoom()
            })
        }

    })
})

server.listen(port, () => {
    console.log(`Server is up on port ${port}!`)
})