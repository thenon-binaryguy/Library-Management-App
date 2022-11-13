


function validateForm() {
    let x = document.forms["login"]["username"].value;
    let y =document.forms["login"]["password"].value
    if(x =="" && y=="")
    {
        alert("Email and Psassword must be filled out");
        return false;
      }
    else if (x == "") {
      alert("Email must be filled out");
      return false;
    }
    else if (y == "") {
        alert("Password must be filled out");
        return false;
      }
  }

function validateForm1(){
    let w = document.forms["signup"]["email"].value;
    let x =document.forms["signup"]["name"].value
    let y = document.forms["signup"]["password"].value;
    let z =document.forms["signup"]["age"].value
    if(x==""||y==""||z==""||w=="")
    {
        alert("Field empty") ; 
        return false;
    }
}


function toggleSignup(){
    document.getElementById("login-toggle").style.backgroundColor="#fff";
     document.getElementById("login-toggle").style.color="#222";
     document.getElementById("signup-toggle").style.backgroundColor="#F7CA18";
     document.getElementById("signup-toggle").style.color="#fff";
     document.getElementById("login-form").style.display="none";
     document.getElementById("signup-form").style.display="block";
 }
 
 function toggleLogin(){
     document.getElementById("login-toggle").style.backgroundColor="#F7CA18";
     document.getElementById("login-toggle").style.color="#fff";
     document.getElementById("signup-toggle").style.backgroundColor="#fff";
     document.getElementById("signup-toggle").style.color="#222";
     document.getElementById("signup-form").style.display="none";
     document.getElementById("login-form").style.display="block";
 }
 function addbookform() {
    document.getElementById("publication").innerHTML = "";
 }
function msg(){
    alert("User Created")
} 

 