import { $artistsHost } from "./index";

export const artistData = async (id) => {
    const response = await $artistsHost.get(`/artists/${id}`);
    return response;
}

export const artistLike = async (id) => {
    const response = await $artistsHost.post('/artists/likes', {artist_id: id})
    return response
}

export const artistLikes = async () => {
    const response = await $artistsHost.get(`/artists/likes`);
    return response;
}

export const artistLikeIds = async () => {
    const response = await $artistsHost.get(`/artists/likes-ids`);
    return response;
}