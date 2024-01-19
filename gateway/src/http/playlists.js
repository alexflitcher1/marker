import {$playlistsHost} from './index'

export const playlistsByUid = async (query) => {
    const response = await $playlistsHost.get('/playlists')
    return response
}

export const playlistsCreate = async (title, avatar, description) => {
    const data = {
        title: title,
        avatar: avatar,
        description: description
    }
    const response = await $playlistsHost.post('/playlists/create', data)
}