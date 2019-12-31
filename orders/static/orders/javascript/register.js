const Registration = (function () {
  function alert(element, message) {
    element.empty();
    element.append(message);
    element.show();
    setTimeout(function(){
      element.hide();
    }, 3000)
  }
  function registration(event) {
    event.preventDefault();
    const csrfToken = getCookie("csrftoken");
    const fields = $("input");
    const comment = $("#comment");
    const regdata = $("#regform").serializeArray();
    const [csrfToken, username, pass, confpass, email, confemail, fname, sname, college] = fields;
    let msg = "";
    $.each(fields, function(index) {
      if (this.value === "") {
        if (this.name !== 'csrfmiddlewaretoken') {
          msg += "<p>" + this.title + " is required. </p>";
        }
      }
    });
    if (msg) {
      alert(comment, msg)
      return false;
    }
    if (pass.value !== confpass.value) {
      alert(comment, "Passwords need to match");
      return false;
    }
    if (email.value !== confemail.value) {
      alert(comment, "Email addresses must match");
      return false;
    }
    $.ajax({
      method: "POST",
      url:"/register",
      headers: {
        "X-CSRFToken": csrfToken
      },
      data: { 
        form: regdata,
        check: true 
      }
    }).done(function(data){
      if (data.user_is_unique === true){
        return $("#regform").submit();
      };
      if (data.error) {
        alert(comment, data.error);
        return;
      };
    });
  }
  return registration;
}());

$(document).ready(function () {
  $("#regbtn").click(function(event) {
    Registration(event);
  });
});