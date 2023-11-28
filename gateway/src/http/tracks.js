import {$tracksHost} from './index'

export const pagination = async (start, stop) => {
    const response = await $tracksHost.get(`/tracks/pagination/${start}/${stop}`)
    return response
}

export const albumWithTracks = async (id) => {
    const response = await $tracksHost.get(`/tracks/album/${id}`);
    return response;
}

export const artistTracksPagination = async (id, start, stop) => {
    const response = await $tracksHost.get(`/tracks/artist/${id}/${start}/${stop}`);
    return response;
}

export const avatar = async(file) => {
    return process.env.REACT_APP_CND_API_HOST + `/img/${file}`
}

export const likeTrack = async (id) => {
    const response = await $tracksHost.post('/tracks/likes', {track_id: id})
    return response
}

export const likesGet = async () => {
    const response = await $tracksHost.get('/tracks/likes')
    return response
}

export const likesIdsGet = async () => {
    const response = await $tracksHost.get('/tracks/likes-ids')
    return response
}