const zerorpc = require("zerorpc")
let client = new zerorpc.Client()

client.connect("tcp://127.0.0.1:4242")

client.invoke("echo", "server ready", (error, res) => {
  if(error || res !== 'server ready') {
    console.error(error)
  } else {
    console.log("server is ready")
  }
})

let formula = document.querySelector('#formula')
let name = document.querySelector('#name')
let sex = document.querySelector('#sex')
let ty = document.querySelector('#ty')
let department = document.querySelector('#department')
let ID = document.querySelector('#ID')
let start_date = document.querySelector('#start_date')
let end_date = document.querySelector('#end_date')

let submit_button = document.querySelector('#submit_button')

let result = document.querySelector('#result')


submit_button.addEventListener('click', () => {
  client.invoke("create_card", name.value, sex.value, ty.value, department.value, ID.value, start_date.value, end_date.value, (error, res) => {
    if(error) {
      console.error(error)
    } else {
      result.textContent = res
    }
  })
})
submit_button.dispatchEvent(new Event('click'))
//formula.dispatchEvent(new Event('input'))

