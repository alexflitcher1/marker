import { useContext, useEffect, useState } from "react";
import { Context } from "../..";
import "../../styles/albums.css";
import { albumWithTracks } from "../../http/tracks";
import Track from "../tracks/Track";
import { albumLike } from "../../http/albums";
import Likes from "./Likes";

const Album = (data) => {
    data = data.data;
    const [loaded, setLoaded] = useState(false);
    const [albumTracks, setTracks] = useState();
    const [changePreparedTracks, setPreparedTracks] = useState(false);
    const [isShow, setShowAlbumTracks] = useState(false);
    const [likeShow, setLikeShow] = useState(false);
    const {tracks} = useContext(Context);
    const {likes} = useContext(Context);
    const avatarUrl = process.env.REACT_APP_CND_API_HOST + '/img/' + data.avatar;

    useEffect(() => {
        if (loaded) {
            albumWithTracks(data.id).then(data => {
                tracks.tracksPrepared = JSON.parse(data.request.response).tracks;
                setTracks(JSON.parse(data.request.response));
            });
        }
    }, [loaded]);

    useEffect(() => {
        if (changePreparedTracks) {
            tracks.tracksPrepared = albumTracks.tracks;
            setPreparedTracks(false);
        }
    }, [changePreparedTracks])

    const showAlbumTracks = (e) => {
        if (!loaded) {
            setLoaded(true)
        }
    }

    const albumTracksPlay = (e) => {
        setPreparedTracks(true);
        tracks.tracksPrepared = albumTracks.tracks;
    }

    const setShow = () => {
        setShowAlbumTracks(!isShow)
    }

    const closeWindow = () => {
        setShowAlbumTracks(false)
    }

    return (
        <>
        <div className="album" onClick={showAlbumTracks} onMouseEnter={() => setLikeShow(true)} onMouseLeave={() => setLikeShow(false)}>
            <Likes liked={likes.albumLikes.indexOf(data.id) !== -1} id={data.id} show={likeShow} />
            <div onClick={setShow}><img src={avatarUrl} /></div>
            <div>{data.title}</div>
        </div>
        <div onMouseDown={albumTracksPlay} onMouseUp={albumTracksPlay} className={isShow ? "album-sidebar album-tracks" : "album-sidebar-hidden album-tracks"}>
            <div className="close" onClick={closeWindow}>X</div>
            {albumTracks ?
            albumTracks.tracks.map((value) => {
                if (likes.likes.length > 0) {
                    if (likes.likes.indexOf(value.id) !== -1 )
                        return <Track info={value} page={'album'} index={albumTracks.tracks.indexOf(value)} liked={true} />
                }
                return <Track info={value} page={'album'} index={albumTracks.tracks.indexOf(value)} liked={false} />
            })
            : ''}
        </div>
        </>
        )
}

export default Album;