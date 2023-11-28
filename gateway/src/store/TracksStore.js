import { makeAutoObservable } from 'mobx';

export default class TracksStore {
    constructor() {
        const tracks = localStorage.getItem('last-query');
        this.tracks = tracks ? JSON.parse(tracks) : [];
        this.tracksLength = this.tracks.length
        this.tracksPrepared = [];
        this.isPagStop = false;
        this.lastTracksType = ''
        this.tracksType = ''
        makeAutoObservable(this)
    }

    setTracks(tracks) {
        this.tracks = tracks
        this.tracksLength = this.tracks.length
    }
}