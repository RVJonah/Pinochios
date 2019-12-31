const refreshOrderList = (function(){
  function refreshOrderList() {
    const csrfToken = getCookie('csrfToken');
    const currentMaxOrders = $("tr:last").prop("class");
    const message = $("#message");
    console.log(currentMaxOrders)
    $.ajax({
      url: `/refresh_order_list?max=${currentMaxOrders}`,
      method: "GET",
      headers: {
          "X-CSRFToken": csrfToken
      },
    }).done(function(data){
      message.empty();
      message.append("<p>Orders Updated</p>");
      if (data.new_orders.length > 0){
        data.new_orders.forEach(item => {
          $("table tbody").append(`
            <tr class="${item.id}">
            <td>${item.order_number}</td>
            <td class="itemedBy">${item.username}</td>
            <td>
            ${item.item_name}
            ${item.item_type}
            </td>
            <td>${item.extras}</td>
            <td id="${item.id}">
                <input type="checkbox" class="complete">
            </td>
            <td>${item.date}</td>
            </tr>
            `);
        });
      } else {
        if (data.error) {
          message.append(`<p>No new orders</p>`);
        };
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
  $("#refreshOrderListButton").click(function(){
    refreshOrderList();
  })
});