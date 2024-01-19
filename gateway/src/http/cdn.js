import {$cdnHost} from './index'

export const uploadPlaylistAvatar = async (file) => {
    const response = await $cdnHost.post('/playlist/avatar-upload', file, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    return response
}