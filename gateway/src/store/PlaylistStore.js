import { makeAutoObservable } from 'mobx';

export default class PlaylistStore {
    constructor() {
        this.playlists = []
        makeAutoObservable(this)
    }
    
}