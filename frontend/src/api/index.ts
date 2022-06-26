import axios from "axios";


// const API_URL = "http://localhost:8000";
const API_URL = process.env.VUE_APP_API_URL
axios.defaults.baseURL = API_URL

export interface Video{
    url: String,
    school_class: String,
    teacher: String,
    subject: String,
    lesson_start_time: Date
}

export function isAlive() {
    return axios.get(`/`)
}

export function addVideo(payload: Video){
    return axios.post('/add_video', payload)
}

export function getVideoList(){
    return axios.get('/get_video_list')
}

export function getVideoCard(_id: String){
    return axios.get('/get_video_card', { params: {_id}})
}
