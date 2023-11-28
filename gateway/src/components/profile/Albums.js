import { useContext, useEffect, useState } from "react";
import { Context } from "../..";
import { albumLikesGet, albumLikesIdsGet } from "../../http/albums";
import Album from "../albums/Album";
import { likesIdsGet } from "../../http/tracks";

const Albums = () => {
    const {likes} = useContext(Context);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        likesIdsGet().then(data => {
            likes.likes = JSON.parse(data.request.response);
        })
        albumLikesIdsGet().then(data => {
            likes.albumLikes = JSON.parse(data.request.response);
        });
        albumLikesGet().then(data => {
            likes.albumsWithData = JSON.parse(data.request.response);
        }).finally(() => setLoading(false));
    }, []);

    if (loading) {
        return 'waiting..';
    }

    return (
        <div className="albums">
            {likes.albumsWithData.map((value) => {
                return <Album data={value.album} />
            })}
    </div>
    )
}

export default Albums;