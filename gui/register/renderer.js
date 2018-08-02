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

/*注册新卡*/
let name = document.querySelector('#name')
var sex = document.getElementsByName("sex");
var ty = document.getElementsByName("ty");
let department = document.querySelector('#dep')
let ID = document.querySelector('#id')
let start_date = document.querySelector('#start_date')
let end_date = document.querySelector('#end_date')

let submit_button = document.querySelector('#create_button')

/*延长有效期*/
let end_date2 = document.querySelector('#end_date_2');
let extend_button = document.querySelector('#extend_button')


/*获得信息*/
let cardinfo = document.querySelector('#cardinfo');		//输入框
let cardinfo_button = document.querySelector('#cardinfo_button')

/*注销旧卡*/
var cb1 = document.getElementById("checkbox1");
var cb2 = document.getElementById("checkbox2");
let clear_button = document.querySelector('#clear_button')

/*添加门禁*/
let doorid = document.querySelector('#doorid');			//输入框
let door_button = document.querySelector('#door_button')

/*添加门禁*/
let doorid2 = document.querySelector('#doorid2');		//输入框
let door_button2 = document.querySelector('#door_button2')



submit_button.addEventListener('click', () => {
  var sex_val;
  for (i = 0; i < sex.length; i ++) {
    if (sex[i].checked) {
      sex_val = i.toString();
    }
  }
  var ty_val;
  for (i = 0; i < ty.length; i ++) {
    if (ty[i].checked) {
      ty_val = i.toString();
    }
  }
  client.invoke("create_card", name.value, sex_val, ty_val, department.value, ID.value, start_date.value, end_date.value, (error, res) => {
      if(error) {
    } else {
    }
  })
})

extend_button.addEventListener('click', () => {
  client.invoke("create_card", end_date2.value, (error, res) => {
      if(error) {
    } else {
    }
  })
})

clear_button.addEventListener('click', () => {
  var cb1_val, cb2_val;
  if (cb1.checked)
    cb1_val = "?";
  if (cb2.checked)
    cb2_val = "?";
  client.invoke("create_card", cb1_val, cb2_val, (error, res) => {
      if(error) {
    } else {
    }
  })
})
