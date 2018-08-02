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


let name = document.querySelector('#name')
var sex = document.getElementsByName("sex");
var ty = document.getElementsByName("ty");
let department = document.querySelector('#dep')
let ID = document.querySelector('#id')
let start_date = document.querySelector('#start_date')
let end_date = document.querySelector('#end_date')

let submit_button = document.querySelector('#create_button')

let end_date2 = document.querySelector('#end_date_2');
let extend_button = document.querySelector('#extend_button')

var cb1 = document.getElementById("checkbox1");
var cb2 = document.getElementById("checkbox2");
let clear_button = document.querySelector('#clear_button')

submit_button.addEventListener('click', () => {
  var sex_val;
  for (i = 0; i < sex.length; i ++) {
    if (sex[i].checked) {
      sex_val = (i+1).toString();
    }
  }
  var ty_val;
  for (i = 0; i < ty.length; i ++) {
    if (ty[i].checked) {
      ty_val = (i+1).toString();
    }
  }
  client.invoke("create_new", name.value, sex_val, ty_val, department.value, ID.value, start_date.value, end_date.value, (error, res) => {
      if(error) {
    } else {
      alert(res);
    }
  })
})

extend_button.addEventListener('click', () => {
  client.invoke("refresh_card", end_date2.value, (error, res) => {
      if(error) {
    } else {
      alert(res);
    }
  })
})

clear_button.addEventListener('click', () => {
  var cb1_val, cb2_val;
  if (cb1.checked)
    cb1_val = "1";
  else
    cb1_val = "2";
  if (cb2.checked)
    cb2_val = "1";
  else
    cb2_val = "2";
  client.invoke("clear_cards", cb1_val, cb2_val, (error, res) => {
      if(error) {
    } else {
      alert(res);
    }
  })
})
