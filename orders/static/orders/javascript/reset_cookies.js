const resetCookies = (function(){
  document.cookie = "ordered=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  document.cookie = "basket=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}())