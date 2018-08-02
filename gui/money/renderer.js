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

/*综合信息*/
//无输入, 只有输出:
let name = document.querySelector('#name')
let dep = document.querySelector('#dep')			//院系
let ID = document.querySelector('#ID')
let ty = document.querySelector('#ty')				//类别
let start_date = document.querySelector('#start_date')
let end_date = document.querySelector('#end_date')
let balance = document.querySelector('#balance')		//余额


/*圈存*/
//输入:
let recharge = document.querySelector('#recharge')		//充值金额
let recharge_button = document.querySelector('#recharge_button')
//输出:
//let balance = document.querySelector('#balance')		//与"综合信息"重合


/*挂失获取金额*/
//输入:
let return_button = document.querySelector('#return_button')
//输出:
let lose_date = document.querySelector('#lose_date')		//挂失日期
let lose_money = document.querySelector('#lose_money')		//挂失金额


/*消费记录*/
//无输入, 只有输出:
let date1 = document.querySelector('#date1')   //第一个消费日期
let price1 = document.querySelector('#price1')   //第一个消费金额
let date2 = document.querySelector('#date2')   //第二个消费日期
let price2 = document.querySelector('#price2')   //第二个消费金额
let date3 = document.querySelector('#date3')
let price3 = document.querySelector('#price3')
let date4 = document.querySelector('#date4')
let price4 = document.querySelector('#price4')
let date5 = document.querySelector('#date5')
let price5 = document.querySelector('#price5')



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