console.log('Hello world')

const ws = new WebSocket('ws://localhost:8080')

ws.onopen = () => {
  console.log('Connected')
}

formChat.addEventListener('submit', (event) => {
  event.preventDefault()
  const message = textField.value
  ws.send(message)
  textField.value = null
})

ws.onmessage = (event) => {
  const message = event.data
  const div = document.createElement('div')
  div.innerText = message
  subscribe.appendChild(div)
}
