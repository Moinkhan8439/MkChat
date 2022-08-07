let form = document.getElementById('form')

let handleSubmit= async(e) => {
    e.preventDefault()
    let room = e.target.room.value.toUpperCase()
    let username = e.target.username.value             
    let response = await fetch(`/get_token/?channel=${room}`)
    let data = await response.json()
    console.log(username)
    let UID = data.uid
    let token = data.token
    sessionStorage.setItem('UID',UID)
    sessionStorage.setItem('token',token)
    sessionStorage.setItem('room',room)
    sessionStorage.setItem('username',username)

    window.open('/room/','_self')
}

form.addEventListener('submit',handleSubmit)