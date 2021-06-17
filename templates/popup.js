document.addEventListener('DOMContentLoaded', () => {
  var lowercaseCheckbox = document.getElementById("lowercase");
  var uppercaseCheckbox = document.getElementById("uppercase");
  var numbersCheckbox = document.getElementById("numbers");
  var specialcharCheckbox = document.getElementById("specialchar");
  var length = document.getElementById("length");
  var button = document.getElementById("generateButton");
  var form = document.getElementById("form");
  var copyBtn = document.getElementById("copyBtn");

  var str = '';
  var lowercase = 'abcdefghijklmnopqrstuvwxyz';
  var uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var numbers = '0123456789';
  var specialchar = '!?@#$%^&*()_+~|}{[]=-;';
  var pass = '';


  function generateP() {
    pass = "";
    for (i = 1; i <= length.value; i++) {
        var char = Math.floor(Math.random()
                    * str.length);

        pass += str.charAt(char);
    }

    return pass;
  }

  button.addEventListener('click', function(e) {
    var gen = "";
    str = "";
    if (lowercaseCheckbox.checked) {
      str = str.concat(lowercase);
    }
    if (uppercaseCheckbox.checked) {
      str = str.concat(uppercase);
    }
    if (numbersCheckbox.checked) {
      str = str.concat(numbers);
    }
    if (specialcharCheckbox.checked) {
      str = str.concat(specialchar);
    }
    gen = generateP();
    document.getElementById("generatedpass").value = gen;

    console.log("hi");
    console.log(str);
    console.log(gen);
  }, false)
})

copyBtn.addEventListener('click', function(e) {
  var copyText = document.getElementById("generatedpass");
  copyText.select();

  document.execCommand("copy");
  // alert("Copied the text: " + copyText.value);

})

// var button = document.getElementById("generateButton");

// button.addEventListener("click", function(){
//     const req = new XMLHttpRequest();
//     const baseUrl = 'http://127.0.0.1:8000/authentication';
//     // const urlParams = `email=${email}&password=${pwd}`;
//     const idk = alert("hi")


//     req.open("POST", baseUrl, true);
//     req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//     req.send(idk);

//     req.onreadystatechange = function() { // Call a function when the state changes.
//         if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
//             console.log("Got response 200!");
//         }
//     }
// });