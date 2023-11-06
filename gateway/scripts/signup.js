async function send(){
 
    // получаем введеное в поле имя и возраст
    var firstName = document.querySelector('#first_name').value
    var lastName = document.querySelector('#last_name').value
    var login = document.querySelector('#login').value
    var email = document.querySelector('#email').value
    var password = document.querySelector('#password').value
    var retPass = document.querySelector('#ret_pass').value
    // отправляем запрос
    const response = await fetch("http://localhost:8081/account/mail", {
            method: "POST",
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({ 
                firstName: firstName,
                lastName: lastName,
                login: login,
                email: email,
                password: password
            })
        });
        
    const data = await response.json();
    if (data.result) {
        document.querySelector('form').innerHTML = 
        "<table>" + 
        "<div class='input'>" +
        "<tr><td><label for='email' id='email'>" + email + "</label></td><td></td></tr>" +
        "<tr><td><label for='email' id='firstName'>" + firstName + "</label></td><td></td></tr>" +
        "<tr><td><label for='email' id='lastName'>" + lastName + "</label></td><td></td></tr>" +
        "<tr><td><label for='email' id='login'>" + login + "</label></td><td></td></tr>" +
        "<tr><td><label for='email' id='password'>" + password + "</label></td><td></td></tr>" +
        "</div>" +
        "<div class='input'>" +
        "<tr><td><label for='code'>Код с почты</label></td><td><input id='code'></td></tr>" +
        "</div>" +
        "<tr><td><button id='send'>Отправить</button></td></tr>" +
        "</table>"
        document.querySelector('form').removeEventListener('submit', send)
        document.querySelector('form').addEventListener('submit', createUser)
    } else {
        
    }

}

async function createUser(){

    // получаем введеное в поле имя и возраст
    var firstName = document.querySelector('#firstName').textContent
    var lastName = document.querySelector('#lastName').textContent
    var login = document.querySelector('#login').textContent
    var email = document.querySelector('#email').textContent
    var password = document.querySelector('#password').textContent
    var code = document.querySelector('#code').value
    // отправляем запрос
    const response = await fetch("http://localhost:8081/account/create", {
            method: "POST",
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({
                user: {
                    login: login,
                    firstName: firstName,
                    lastName: lastName,
                    email: email,
                    password: password
                },
                mail: {
                    email: email,
                    code: code
                }
            })
        });
        
    const data = await response.json();
    if (data.result) {
        alert(data.result)
    } else {
        alert(data.error)
    }
    

}

document.querySelector('form').addEventListener('submit', send)