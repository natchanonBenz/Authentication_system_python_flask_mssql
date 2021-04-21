// ---------------------------------------- Function 1 : Authenication ------------------------------------------------
function loginbtn() {
  var name = document.getElementById("username");
  var pass = document.getElementById("password");

  if ((String(name.value).localeCompare("admin")) !== 0 && (String(pass.value).localeCompare("admin")) !== 0) {
    document.getElementById("loginfail").innerHTML = "Login Fail, Please try again";
  }
  console.log(name + "name");
  var entry = {
    name: name.value,
    pass: pass.value
  };

  fetch(`/login`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
    .then(function (response) {
      if (response.status !== 200) {
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(function (data) {
        //console.log("recievefromfalsk:"+data)
        // console.log(data.message);
        // document.getElementById("testtext").innerHTML = data.message;
      });
    })
    .catch(function (error) {
      console.log("Fetch error: " + error);
    });
}