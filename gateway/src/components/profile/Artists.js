import { useContext, useEffect, useState } from "react";
import { Context } from "../..";
import { artistLikes } from "../../http/artists";
import { Link } from "react-router-dom";
import { ARTIST_ROUTE } from "../../utils/consts";
import Artist from "../artists/Artist";


const Artists = () => {
    const {likes} = useContext(Context);
    const [loading, setLoading] = useState(true);
    const [likeShow, setLikeShow] = useState(false);
    const avatarUrl = process.env.REACT_APP_CND_API_HOST + '/artist-avatar/';

    useEffect(() => {
        artistLikes().then(data => {
            likes.artistsWithData = JSON.parse(data.request.response)
        }).finally(() => setLoading(false))
    }, [])

    if (loading) {
        return '...waiting'
    }

    return (
        <>
        <div className='leader__title'>Артисты</div>
        <div className="artist__likes">
            {likes.artistsWithData.map(value => {
                return <Artist data={value.artist} />
            })}
        </div>
        </>
    )
}

export default Artists;