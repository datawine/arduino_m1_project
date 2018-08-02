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
let name = document.querySelector('#input')
let sex = document.querySelector('#radio') //输入格式为"男", "女", 而不是数字
let ty = document.querySelector('#radio1') //输入格式为"本科", "硕士", "博士"等, 而不是数字
let department = document.querySelector('#select') //输入的院系名会比较长, 需要处理
let ID = document.querySelector('#input1')  //是字符串, 而不是数字
let start_date = document.querySelector('#date') //ex 2018-07-13
let end_date = document.querySelector('#date1')

let create_button = document.querySelector('#create_button')

//let result = document.querySelector('#result')


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

