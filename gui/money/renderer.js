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
//没有输入, 只有输出:
let balance = document.querySelector('#balance')   //余额

client.invoke("query_money", (error, res) => {
  if(error) {
    
  } else {
    balance.textContent = res
  }
})

/*圈存*/
//输入:
let recharge = document.querySelector('#recharge')
let recharge_button = document.querySelector('#recharge_button')
//输出:
//let balance = document.querySelector('#balance')   //余额, 和"查看余额"重复不用再声明

/*消费*/
//输入:
let consume = document.querySelector('#consume')
let consume_button = document.querySelector('#consume_button')
//输出:
//let balance = document.querySelector('#balance')   //余额

recharge_button.addEventListener('click', () => {
  client.invoke("charge_money", recharge.value, (error, res) => {
      if(error) {
    } else {
      alert(res);
    }
  })
})

consume_button.addEventListener('click', () => {
  client.invoke("consume_money", consume.value, (error, res) => {
      if(error) {
    } else {
      alert(res);
    }
  })
})

/*消费记录*/
//没有输入, 只有输出:
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

client.invoke("query_money_num", (error, res) => {
  if(error) {

  } else {
    num_list = res.split('|')
    if (num_list[0].length > 0)
    {
      price1.textContent = num_list[0]
    }  
  }
})

client.invoke("query_money_record", (error, res) => {
  if(error) {

  } else {
    num_list = res.split('|')
    if (num_list[0].length > 0)
    {
      date1.textContent = num_list[0]
    }  
  }
})
