import axios from "axios";


const API_URL = "http://localhost:8000";

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