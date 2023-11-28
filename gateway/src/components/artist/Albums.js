import { useContext, useEffect, useState } from "react";
import { Context } from "../..";
import { albumLikesIdsGet, artistAlbums } from "../../http/albums";
import Album from "../albums/Album";

const Albums = () => {
    const {artist} = useContext(Context);
    const {likes} = useContext(Context);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        albumLikesIdsGet().then(data => {
            likes.albumLikes = JSON.parse(data.request.response);
        });
        artistAlbums(artist.artist.id, 0, 10).then(data => {
            artist.albums = JSON.parse(data.request.response);
        }).finally(() => setLoading(false));
    }, []);

    if (loading) {
        return 'waiting..';
    }

    return (
        <div className="albums">
            {artist.albums.map((value) => {
                return <Album data={value} />
            })}
    </div>
    )
}

export default Albums;