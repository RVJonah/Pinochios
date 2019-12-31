const updateOrderList = (function(){
  function updateOrderList() {
    const csrfToken = getCookie('csrftoken');
    const checkedOrders = $(".complete");
    let completedOrders = [];
    checkedOrders.each(function() {
      if ($(this).is(':checked')) {
        completedOrders.push($(this).parent().prop('id'));
      };
    });
    if (completedOrders !== []) {
      $.ajax({
        url: "/update_order_list",
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken
        },
        data: { 
          completed_orders : JSON.stringify(completedOrders)
        }
      }).done(function(data){
        if (data.success === true) {
          completedOrders.forEach((order)=> {
            const item = $(`#${order}`);
            item.text("Complete");
            item.children().remove();
          });
        } else {
          $("#message").empty();
          $("#message").text(data.error);
        }
      });
    };
  }
  return updateOrderList;
}());

$(document).ready(function (){
  $("#updateButton").click(function(){
    updateOrderList();
  })
});