const API = "http://127.0.0.1:8000/api/auth/"

async function register() {

    const username = document.getElementById("reg_username").value
    const email = document.getElementById("reg_email").value
    const password = document.getElementById("reg_password").value

    const res = await fetch(API + "register/", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({username,email,password})
    })

    const data = await res.json()

    document.getElementById("message").innerText = JSON.stringify(data)
}


async function login() {

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    const res = await fetch(API + "login/", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({username,password})
    })

    const data = await res.json()

    if(data.access){
        localStorage.setItem("access",data.access)
        localStorage.setItem("refresh",data.refresh)
        document.getElementById("message").innerText="Login success"
    }else{
        document.getElementById("message").innerText="Login failed"
    }
}


async function resetPassword(){

    const email = document.getElementById("reset_email").value

    const res = await fetch(API + "reset-password/", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({email})
    })

    const data = await res.json()

    document.getElementById("message").innerText = data.message
}

async function refreshMyToken() {
    const refreshToken = localStorage.getItem('refresh_token');

    const response = await fetch('/api/auth/token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            refresh: refreshToken
        }),
    });

    if (response.ok) {
        const data = await response.json();
        // The API returns a new 'access' token
        localStorage.setItem('access_token', data.access);
        console.log("Token refreshed successfully!");
    } else {
        console.log("Refresh token expired. Redirecting to login...");
        window.location.href = '/login.html/';
    }
}