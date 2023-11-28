import { useContext, useEffect, useState } from "react";
import { Context } from "../..";
import { artistTracksPagination, likesIdsGet } from "../../http/tracks"
import Track from "../tracks/Track";


const Tracks = () => {
    const {likes} = useContext(Context);
    const {tracks} = useContext(Context);
    const {artist} = useContext(Context);
    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1)
    const [fetching, setFetching] = useState(false)

    useEffect(() => {
        document.addEventListener('scroll', scrollHandler)
        return function () {
            document.removeEventListener('scroll', scrollHandler)
        }
    }, []);

    useEffect(() => {
        likesIdsGet().then(data => {
            likes.likes = JSON.parse(data.request.response);
        });
        artistTracksPagination(artist.artist.id, 0, 10).then(data => {
            tracks.tracksPrepared = JSON.parse(data.request.response)
            tracks.isPagStop = false
        }).finally(() => setLoading(false));
    }, []);

    useEffect(() => {
        if (fetching) {
            artistTracksPagination(artist.artist.id, currentPage*10, 10).then(data => {
                setCurrentPage(currentPage + 1)
                tracks.tracksPrepared = [...tracks.tracksPrepared, ...JSON.parse(data.request.response)]
                if (!JSON.parse(data.request.response).length)
                    tracks.isPagStop = true
            }).finally(() => {
                setFetching(false)
            });
        }
    }, [fetching]);

    const scrollHandler = (e) => {
        if (!tracks.isPagStop) {
            if (e.target.documentElement.scrollHeight - (e.target.documentElement.scrollTop + window.innerHeight) < 100) {
                setFetching(true)
            }
        }
    }

    if (loading) {
        return 'waiting..';
    }

    return (
        <>
        {tracks.tracksPrepared.map((value) => {
            if (likes.likes.length > 0) {
                if (likes.likes.indexOf(value.id) !== -1 )
                    return <Track info={value} page={'track-artist'} liked={true} index={tracks.tracksPrepared.indexOf(value)} /> 
            }
            return <Track info={value} page={'track-artist'} liked={false} index={tracks.tracksPrepared.indexOf(value)} /> 
        })}
        </>
    )
}

export default Tracks;