import { defineStore } from "pinia";

export type RootState = {
    page: String,
    popupOpened: boolean,
    video: any
}


export const useMainStore = defineStore({
    id: "mainStore",
    state: ()=>({
        page: 'home',
        popupOpened: false,
        video: {}
    } as RootState),
    actions: {
        changePage(page: String){
            this.page = page
        },
        openPopup(){
            this.popupOpened = true
        },
        closePopup(){
            this.popupOpened = false
        }
    }
})