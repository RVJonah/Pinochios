const sendOrder = (function() {
  function sendOrder(event) {
    if($(".empty").length === 1) {
      return;
    }
    const orderItems = $('form');
    const topping = $('select');
    const message = $('#message');
    let allToppingsAreChosen = true;
    topping.each(function() {
      if ($(this).children("option:selected").val() === 'unselected') {
        allToppingsAreChosen = false;
      };
    })
    if (!allToppingsAreChosen){
      message.empty();
      message.text("Please select all toppings");
      message.show()
      setTimeout(() => {
        message.hide();
      }, 3000)
      return
    }
    let order = [];
    orderItems.each(function(){
      order.push({
        itemType: $(this).attr('class'),
        itemId: $(this).attr('name'),
        extras: $(this).serialize()
      });
    });
    if(confirm("Are you sure your order is complete?")) {
      document.cookie = "ordered=" + JSON.stringify(order) + ";" + "SameSite=Strict";
      $(".itemForm")[0].submit()
    };
  };
  return sendOrder;
}());

$(document).ready(function() {
  $('#orderButton').click(function (event){
    sendOrder(event);
  })
})