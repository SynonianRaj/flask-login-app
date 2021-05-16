function showLogin() {
  let x = document.getElementById("signup").style;
  let y = document.getElementById("login").style;
  if (x.display == "block") {
    x.display = "none";
    y.display = "block";
  } else {
    x.display = "block";
    y.display = "none";
  }
}

function signupFunction() {
  var a = document.getElementById("password").value;
  var b = document.getElementById("confirm").value;
  var str = document.getElementById("email").value;
  if (a != "" && b != "") {
    if (
      str.includes("@gmail.com") == true ||
      str.includes("@hotmail.com") == true ||
      str.includes("@outlook.com") == true ||
      str.includes("@yahoo.com") == true
    ) {
      if (a == b) {
        var a = (document.getElementById("myForm").action = "/verify-email");
      } else {
        alert("Password Does not matched");
        document.getElementById("password").value = "";
        document.getElementById("confirm").value = "";
      }
    } else {
      alert("Please Enter a valid Email");
	  document.getElementById("email").value = "";
    }
  }
}

