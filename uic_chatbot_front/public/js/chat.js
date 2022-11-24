//client
const socket = io()  //call io to connect the server
// server(emit) -> client(receive) --acknowledgement --> server
// client(emit) -> server(receive) --acknowledgement --> client

//Elements
const $messageForm=document.querySelector('#message-form')
//for input and button
const $messageFormInput=$messageForm.querySelector('input')
const $messageFormButton=$messageForm.querySelector('button')
//socket.on to listen to the 'message'
//have client listen for "message" event and print the message to console
const $messages = document.querySelector('#messages')
const sidebarTemplate = document.querySelector('#sidebar-template').innerHTML
// Templates
const messageTemplate = document.querySelector('#message-template').innerHTML
const messageTemplateRight = document.querySelector('#message-template-right').innerHTML

//options
const{ username }= Qs.parse(location.search,{ ignoreQueryPrefix:true})

const autoscroll = () => {
    // New message element
    const $newMessage = $messages.lastElementChild

    // Height of the new message
    const newMessageStyles = getComputedStyle($newMessage)
    const newMessageMargin = parseInt(newMessageStyles.marginBottom)
    const newMessageHeight = $newMessage.offsetHeight + newMessageMargin
    //visible height
    const visibleHeight = $messages.offsetHeight
    
    //height of message container
    const containerHeight = $messages.scrollHeight

    //How far have i scrolled
    const scrollOffset = $messages.scrollTop + visibleHeight

    if (containerHeight - newMessageHeight <= scrollOffset + 50){
        $messages.scrollTop = $messages.scrollHeight
    }
}


socket.on('message',(message)=>{
    console.log(message)//dump message
    let currMessageTemplate
    if (message.username.toLowerCase() === username.toLowerCase()) {
        currMessageTemplate = messageTemplateRight
    } else {
        currMessageTemplate = messageTemplate
    }
    const html = Mustache.render(currMessageTemplate, {
        username:message.username,
        message:message.text,
        createdAt:moment(message.createdAt).format('kk:mm:ss A')
    })
    
    $messages.insertAdjacentHTML('beforeend', html)
    autoscroll()
})

socket.on('roomData',({ room, users}) =>{
    const html = Mustache.render(sidebarTemplate,{
        room,
        users
    })
    document.querySelector('#sidebar').innerHTML = html
    
})

 //setup listener for form submissions, emit "sendMessage" with input string as message data
$messageForm.addEventListener('submit',(e)=>{
    e.preventDefault()
    
    $messageFormButton.setAttribute('disabled','disabled')


    //message:<input name="message" placeholder="Message">
    const message = e.target.elements.message.value

    socket.emit('sendMessage', message, (error)=>{
        $messageFormButton.removeAttribute('disabled')
        $messageFormInput.value = ''  //发消息后清空框 
        $messageFormInput.focus()
        //enable

        if(error){
            return console.log(error)
        }
        console.log('Message delivered!')
    })
})
 
// error: maybe someone's name is repeat
socket.emit('join', {username}, (error) =>{
    if(error){
        alert(error)
        location.href='/'
    }
})