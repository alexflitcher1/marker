import { useContext, useEffect, useState } from "react";
import { Context } from "../..";
import { likesGet } from "../../http/tracks";
import Track from "../tracks/Track";

const Likes = () => {
    const {tracks} = useContext(Context);
    const {play} = useContext(Context);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        likesGet().then(data => {
            tracks.tracksPrepared = JSON.parse(data.request.response)
        }).finally(() => setLoading(false))
    })


    if (loading) {
        return 'waiting...'
    }

    return (
        <div className='container'>
        <div className='leader__title'>Любимое</div>
        {tracks.tracksPrepared.map((value) => {
            return <Track info={value} page={'likes'} liked={true} index={tracks.tracksPrepared.indexOf(value)} /> 
        })}
        </div>
    )
}

export default Likes;