// let form = document.getElementById('join-room-form')

// let handleSubmit= async(e) => {
//     e.preventDefault()
//     let room = e.target.room_name.value
//     let username = e.target.username.value             
//     let response = await fetch(`/get_token/?channel=${room}`)
//     let data = await response.json()
//     console.log(username)
//     let UID = data.uid
//     let token = data.token
//     sessionStorage.setItem('UID',UID)
//     sessionStorage.setItem('token',token)
//     sessionStorage.setItem('room',room)
//     sessionStorage.setItem('username',username)
//     let formData = new FormData();
//     formData.append('room_name', room);
//     formData.append('username', username);
//     fetch(`/join-room/`,{
//         method:'POST',
//         body:formData
//     })
// }

// form.addEventListener('submit',handleSubmit)