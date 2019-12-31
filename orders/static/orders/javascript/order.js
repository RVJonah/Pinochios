const basketManager = (function(){
  let basket = getCookie("basket");
  function showHideMessage(text) {
    let messageBox = $(".addMessage");
    messageBox.text(text);
    messageBox.show();
    setTimeout(() => {
        messageBox.hide();
    }, 3000);
  }
  function addItem(button) {
    const foodType = event.target.parentElement.parentElement.parentElement.parentElement.id;
    const itemName = button.target.name;
    const itemIsLarge = $(`input:checked[name="${itemName} IsLarge"]`).val();
    const numberOfItems = $(`input[name="${itemName} Number"]`).val();
    let itemIsSmall;
    if (`input[name$="${itemName}IsSmall"]`) {
      itemIsSmall = $(`input:checked[name="${itemName} IsSmall"]`).val();
    };
    if (!itemIsSmall && !itemIsLarge) {
      showHideMessage("Please select an item");
      return
    };
    if (itemIsSmall === itemIsLarge) {
      return showHideMessage("Please select large or small");
    };
    if (!numberOfItems) {
      return showHideMessage("Please select a number of items");
    };
    const size = itemIsLarge ? 'large' : 'small';
    const itemDetails = JSON.stringify({
      itemType: foodType,
      itemSize: size,
      item: itemName,
      itemNumber: numberOfItems
    });
    if (basket === '') {
      basket = itemDetails
    } else {
      basket = basket + "-" + itemDetails
    };
    const now = new Date();
    const time = now.getTime();
    const expireTime = time + 24*60*60*1000;
    now.setTime(expireTime);
    document.cookie = 'basket=' + basket + "; expires=" + now.toGMTString() +"SameSite=Strict";
    showHideMessage("Item Added");
  }
  return addItem
}())

$(document).ready(function () {
  $(".addButton").click(function (event) {
    basketManager(event);
  });
});