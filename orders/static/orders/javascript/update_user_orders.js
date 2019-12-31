const refreshOrderList = (function(){
  function refreshOrderList() {
    const csrfToken = getCookie('csrfToken');
    const currentMaxOrders = $("tr:last").prop("class");
    const message = $("#message");
    $.ajax({
      url: `/refresh_my_orders?max=${currentMaxOrders}`,
      method: "GET",
      headers: {
          "X-CSRFToken": csrfToken
      },
    }).done(function(data){
      message.empty();
      message.append("<p>Orders Updated</p>");
      if (data.new_orders){
        data.new_orders.forEach(item => {
          let status = 'Pending'
          if (item.completed) {
            status = 'Complete'
          }
          $("table tbody").append(`
            <tr class="${item.id}">
            <td>${item.order_number}</td>
            <td>
            ${item.item_name}
            ${item.item_type}
            </td>
            <td>${item.extras}</td>
            <td id="${item.id}">
                ${status}
            </td>
            <td>${item.date}</td>
            </tr>
            `);
        });
      };
      if (data.changed_orders) {
        data.changed_orders.forEach(item =>{
          $(`#${item.id}`).text("Completed");
        })
      };
      message.toggle();
      setTimeout(function(){
        message.toggle();
      }, 3000)
    });
  }
  return refreshOrderList;
}());

$(document).ready(function (){
  $("#refreshMyOrdersButton").click(function(){
    refreshOrderList();
  })
});