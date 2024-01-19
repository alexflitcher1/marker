import axios from 'axios';

export const $host = axios.create({
    baseURL: process.env.REACT_APP_ACCOUNT_API_HOST
})

export const $authHost = axios.create({
    baseURL: process.env.REACT_APP_ACCOUNT_API_HOST
})

export const $tracksHost = axios.create({
    baseURL: process.env.REACT_APP_TRACKS_API_HOST
})

export const $refreshHost = axios.create({
    baseURL: process.env.REACT_APP_ACCOUNT_API_HOST
})

export const $artistsHost = axios.create({
    baseURL: process.env.REACT_APP_ARTISTS_API_HOST
})

export const $albumsHost = axios.create({
    baseURL: process.env.REACT_APP_ALBUMS_API_HOST
})

export const $searchHost = axios.create({
    baseURL: process.env.REACT_APP_SEARCH_API_HOST
})

export const $playlistsHost = axios.create({
    baseURL: process.env.REACT_APP_PLAYLISTS_API_HOST
})

export const $cdnHost = axios.create({
    baseURL: process.env.REACT_APP_CND_API_HOST
})

const authInterceptorRefresh = config => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('refresh_token')}`
    return config
}

const authInterceptor = config => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`
    return config
}

$authHost.interceptors.request.use(authInterceptor)

$albumsHost.interceptors.request.use(authInterceptor)

$artistsHost.interceptors.request.use(authInterceptor)

$tracksHost.interceptors.request.use(authInterceptor)
    
$playlistsHost.interceptors.request.use(authInterceptor)

$refreshHost.interceptors.request.use(authInterceptorRefresh)