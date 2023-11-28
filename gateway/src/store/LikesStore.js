import { makeAutoObservable } from 'mobx';

export default class LikesStore {
    constructor() {
        this.likes = {}
        this.albumLikes = {}
        this.artistLikes = {}
        this.likesWithData = {}
        this.albumsWithData = {}
        this.artistsWithData = {}
        makeAutoObservable(this)
    }
    
}