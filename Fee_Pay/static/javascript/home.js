
function goBack() {
  window.history.back();
}
function myFunction() {
   myVar = setTimeout(showPage, 500);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("container").style.display = "block";
}
function myFunction1() {
  var popup = document.getElementById("myPopup");
  popup.classList.toggle("show");
}
function pay(){
  document.getElementById('pay').style.display="block";
}