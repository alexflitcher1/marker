import {$albumsHost} from './index'

export const artistAlbums = async (id) => {
    const response = await $albumsHost.get(`/albums/artist/${id}`)
    return response
}

export const albumLike = async (id) => {
    const response = await $albumsHost.post('/albums/likes', {album_id: id})
    return response
}

export const albumLikesGet = async () => {
    const response = await $albumsHost.get('/albums/likes')
    return response
}

export const albumLikesIdsGet = async () => {
    const response = await $albumsHost.get('/albums/likes-ids')
    return response
}