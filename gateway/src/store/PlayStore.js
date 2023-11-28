import { makeAutoObservable } from 'mobx';

export default class PlayStore {
    constructor() {
        const trackUrl = localStorage.getItem('track-url')
        const volume = localStorage.getItem('track-volume')
        this.currentUrl = trackUrl ? trackUrl : 'http://localhost:8004/audio/namnedetka.mp3'
        this.currentTime = 0
        this.duration = 0
        this.currentIndex = 0
        this.volume = volume ? volume : 50
        this.metaData = localStorage.getItem('track-metadata') ? JSON.parse(localStorage.getItem('track-metadata')) : {}
        this.lastUrl = trackUrl ? trackUrl : 'http://localhost:8004/audio/namnedetka.mp3'
        this.isPlaying = false
        this.setIsPlaying = ''
        makeAutoObservable(this)
    }
    
}