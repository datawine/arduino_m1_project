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

/*查询余额*/
//没有输入, 只有输出

/*圈存*/
let seller1 = document.querySelector('#seller1')
let recharge = document.querySelector('#recharge')
let recharge_button = document.querySelector('#recharge_button')

/*消费*/
let seller1 = document.querySelector('#seller2')
let recharge = document.querySelector('#consume')
let recharge_button = document.querySelector('#consume_button')

/*消费记录*/
//没有输入, 只有输出




/*
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
*/