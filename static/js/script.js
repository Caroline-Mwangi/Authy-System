const passwordInput = document.querySelector("#pass")
const eye = document.querySelector("#eye")

eye.addEventListener("click", function(){
    this.classList.toggle("fa-eye-slash")
    const type = passwordInput.getAttribute("type") === "password" ? "text" : "password"
    passwordInput.setAttribute("type", type)
  })

const password = document.querySelector("#cpass")
const confirm_eye = document.querySelector("#cpeye")

confirm_eye.addEventListener("click", function(){
    this.classList.toggle("fa-eye-slash")
    const type = password.getAttribute("type") === "password" ? "text" : "password"
    password.setAttribute("type", type)
  })