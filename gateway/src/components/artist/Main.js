import { useContext, useEffect, useState } from "react";
import { Context } from "../..";
import { artistTracksPagination, likesIdsGet } from "../../http/tracks";
import { albumLikesIdsGet, artistAlbums } from "../../http/albums";
import "../../styles/albums.css";
import Track from "../tracks/Track";
import Album from "../albums/Album";

const Main = () => {
    const {tracks} = useContext(Context);
    const {likes} = useContext(Context);
    const {artist} = useContext(Context);
    const [prepTracks, setPrepTracks] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        likesIdsGet().then(data => {
            likes.likes = JSON.parse(data.request.response);
        });
        albumLikesIdsGet().then(data => {
            likes.albumLikes = JSON.parse(data.request.response);
        });
        artistAlbums(artist.artist.id).then(data => {
            artist.albums = JSON.parse(data.request.response);
        });
        if (loading) {
            artistTracksPagination(artist.artist.id, 0, 5).then(data => {
                tracks.tracksPrepared = JSON.parse(data.request.response);
                setPrepTracks(JSON.parse(data.request.response))
            }).finally(() => setLoading(false));
        }
    });

    const setPrepared = (e) => {
        tracks.tracksPrepared = prepTracks
    }

    if (loading) {
        return 'waiting..';
    }

    return (
        <>
        <div className='tabs-link'>
            <div className='dep__title'>Популярные треки</div>
        </div>
        <hr />
        {// это короче просто пиздец
        }
        <div onMouseDown={setPrepared} onMouseUp={setPrepared}>
            {prepTracks.map((value) => {
                if (likes.likes.length > 0) {
                    if (likes.likes.indexOf(value.id) !== -1 )
                        return <Track info={value} page={'main-artist'} liked={true} index={prepTracks.indexOf(value)} /> 
                }
                return <Track info={value} page={'main-artist'} liked={false} index={prepTracks.indexOf(value)} /> 
            })}
        </div>
        <hr />
        <div className='tabs-link'>
            <div className='dep__title'>Альбомы</div>
        </div>
        <hr />
        <div className="albums">
            {artist.albums.map((value) => {
                return <Album data={value} />
            })}
        </div>
        </>
    )
}

export default Main;