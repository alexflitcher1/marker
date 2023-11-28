import { makeAutoObservable } from 'mobx';

export default class ArtistStore {
    constructor() {
        this.artist = {}
        this.albums = {}
        makeAutoObservable(this)
    }
    
}