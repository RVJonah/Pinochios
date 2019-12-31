const basketActions = (function(){
  basketCookie = getCookie("basket");
  const basketItems = {};
  if (basketCookie !== '') {
    const basketItemsCookie = basketCookie.split("-");
      for (let i=0; i < basketItemsCookie.length; i++) {
        basketItems[i] = JSON.parse(basketItemsCookie[i]);
      };
  };
  const basketActions = {
    emptyBasket: () => {
      if ($('.itemDiv').length === 0) 
        {return}
      $('.itemDiv').remove();
      $('#total').text("0.00");
      $('.comment').append("<p class='empty'>Your basket is emtpy</p>");
      document.cookie = "basket=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      },
    deleteItem(event) {
      let itemNumberToDelete = event.target.parentElement.parentElement.id;
      let cost = $(`#${itemNumberToDelete} .price`).text();
      let newTotal = parseFloat($("#total").text()) - parseFloat(cost);
      $("#total").text(newTotal.toFixed(2));
      delete basketItems[itemNumberToDelete];
      $(`#${itemNumberToDelete}`).remove();
      let newBasketCookie = ''
      let numberOfItemsRemaining = (Object.keys(basketItems).length);
      let itemKeysRemaining = Object.keys(basketItems);
      for (let i=0; i < numberOfItemsRemaining; i++) {
        if (i === numberOfItemsRemaining - 1) {
          newBasketCookie = newBasketCookie + JSON.stringify(basketItems[itemKeysRemaining[i]])
        } else {
          newBasketCookie = newBasketCookie + JSON.stringify(basketItems[itemKeysRemaining[i]]) + "-";
        }
      }
      if (numberOfItemsRemaining > 0) {
        const now = new Date();
        const time = now.getTime();
        const expireTime = time + 24*60*60*1000;
        now.setTime(expireTime);
        document.cookie = 'basket=' + newBasketCookie + "; expires=" + now.toGMTString() +"SameSite=Strict";
      } else {
        document.cookie = "basket=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"; 
      }          
    },
    checkUncheck(event) {
      let newCost, newTotal;
      let itemDivNumber = event.target.parentElement.parentElement.parentElement.id;
      let cost = parseFloat($(`#${itemDivNumber} .price`).text());
      let currentTotal = parseFloat($("#total").text());
      if (event.target.checked){
        newTotal =  currentTotal + parseFloat(0.50);
        newCost = cost + 0.50;
      } else {
        newTotal = currentTotal - parseFloat(0.50);
        newCost = cost - 0.50;
      }
      $(`#${itemDivNumber} .price`).text(newCost.toFixed(2));
      $("#total").text(newTotal.toFixed(2));
    }
  }
  return basketActions
}())
$(document).ready(function () {
  $("#emptyButton").click(function () {
    basketActions.emptyBasket();
  });
  $(".deleteButton").click(function (event) {
    basketActions.deleteItem(event);
  });
  $(".checkbox").change(function(event) {
    basketActions.checkUncheck(event);
  });
});