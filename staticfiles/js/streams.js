const CHANNEL = appConfig.CHANNEL
const TOKEN = appConfig.TOKEN
const Name= appConfig.NAME
let UID = appConfig.UID
let APP_ID= appConfig.APP_ID

const client = AgoraRTC.createClient({mode:'rtc',codec:'vp8'})

let localTracks = []
let remoteUsers={}


let joinAndDisplayLocalStream =  async() => {

    document.getElementById('room-name').innerText = CHANNEL
    client.on('user-published',handleUserJoined)
    client.on('user-left',handleUserLeft)

    try{
        // let response = await fetch(`/get_key/`)
        // let key=await response.json()
        await client.join(APP_ID,CHANNEL,TOKEN,UID)    
    }
    catch(error){
        console.error(error)


        
        window.open('/','_self')
    }

    localTracks  = await AgoraRTC.createMicrophoneAndCameraTracks()
    // let member = await createMember()
    // console.log('member',member)
    let player = `<div class="video-container" id="user-container-${UID}">
                <div class="username-wrapper">
                    <span class="user-name">${Name}</span>
                </div>
                <div class="video-player" id="user-${UID}"></div>
            </div>
            `
    document.getElementById('video-streams').insertAdjacentHTML('beforeend',player)

    localTracks[1].play(`user-${UID}`)

    await client.publish([localTracks[0],localTracks[1]])
}


let handleUserJoined = async (user,mediaType) => {

    remoteUsers[user.uid]=user
    await client.subscribe(user,mediaType)
    if(mediaType === 'video'){
        let player = document.getElementById(`user-container-${user.uid}`)
        if(player != null){
            player.remove()
        }
        let member=await getMember(user)
            player = `<div class="video-container" id="user-container-${user.uid}">
                        <div class="username-wrapper">
                            <span class="user-name">${member.name}</span>
                        </div>
                        <div class="video-player" id="user-${user.uid}"></div>
                    </div>`
        
        document.getElementById('video-streams').insertAdjacentHTML('beforeend',player)

        user.videoTrack.play(`user-${user.uid}`)
        
    }
    if(mediaType === 'audio'){
        user.audioTrack.play()
    }
}

let handleUserLeft = async(user) => {
    let name=user.name
    delete remoteUsers[user.uid]
    //let msg = await deleteMember(user)
    console.log(name+"left !!!")
    document.getElementById(`user-container-${user.uid}`).remove()
}

let leaveAndRemoveLocalStream= async () =>{
    for (let i=0;localTracks.length >i;i++){
        localTracks[i].stop()
        localTracks[i].close()
    }
    await client.leave()
    let self={
        'uid':UID,
        'room':CHANNEL
    }
    let msg = await deleteMember(self)
    console.log(msg)
    window.open('/','_self')
}

let toggleCamera = async (e) => {
    if(localTracks[1].muted){
        await localTracks[1].setMuted(false)
        e.target.style.backgroundColor ='#fff'
    }
    else{
        await localTracks[1].setMuted(true)
        e.target.style.backgroundColor ='rgb(255,80,80,1)'
    }
}

let toggleMic = async (e) =>{
    if(localTracks[0].muted){
        await localTracks[0].setMuted(false)
        e.target.style.backgroundColor ='#fff'
    }
    else{
        await localTracks[0].setMuted(true)
        e.target.style.backgroundColor ='rgb(255,80,80,1)'
    }
}


let createMember = async() =>{
    let response = await fetch(`/create_member/`,{method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'username': Name , 'room': CHANNEL , 'UID':UID  , 'token': TOKEN})
    })
    let member= await response.json()
    return member

}

let getMember = async(user) => {
    let response = await fetch(`/get_member/?UID=${user.uid}&room=${CHANNEL}`)
    let member=await response.json()
    return member

}  

let deleteMember = async(user) =>{
    let response = await fetch(`/leave_member/`,{ method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'room': CHANNEL , 'UID':user.uid})
    })
    let msg = await response.json()
    return msg.message

}

joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click',leaveAndRemoveLocalStream)
document.getElementById('camera-btn').addEventListener('click',toggleCamera)
document.getElementById('mic-btn').addEventListener('click',toggleMic)

//console.log('streams.js connected')
