import { makeAutoObservable, set } from 'mobx';

export default class UserStore {
    constructor() {
        const settings = localStorage.getItem('user-settings');
        this._isAuth = false
        this._user = {}
        this._settings = settings ? JSON.parse(settings) : {}
        makeAutoObservable(this)
    }

    setIsAuth(bool) {
        this._isAuth = bool
    }

    setUser(user) {
        this._user = user
    }

    setSettings(settings) {
        this._settings = settings
    }

    get isAuth() {
        return this._isAuth
    }

    get user() {
        return this._user
    }

    get settings() {
        return this._settings
    }
}