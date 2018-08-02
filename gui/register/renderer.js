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

/*
let name = document.querySelector('#name')
var sex = document.getElementsByName("sex");

// let ty = document.querySelector('#ty')
let department = document.querySelector('#dep')
let ID = document.querySelector('#id')
let start_date = document.querySelector('#start_date')
let end_date = document.querySelector('#end_date')
*/
let submit_button = document.querySelector('#create_button')

submit_button.addEventListener('click', () => {
  /*
  var sex_val = "0";
  for (i = 0; i < sex.length; i ++) {
    if (sex[i].checked) {
      sex_val = i.toString();
    }
  }
  alert(sex.length);
  */
  client.invoke("create_card", "1", "?", "3", "2", "3", "4", "5", (error, res) => {
//  client.invoke("create_card", name.value, "?", "3", department.value, ID.value, start_date.value, end_date.value, (error, res) => {
      if(error) {
//      console.error(error)
    } else {
    }
  })
})
//formula.dispatchEvent(new Event('input'))
