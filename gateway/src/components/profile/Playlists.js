import { useContext, useEffect, useState } from "react";
import { playlistsByUid } from "../../http/playlists";
import { Context } from "../..";
import Playlist from "../playlists/Playlist";
import { Link } from "react-router-dom";
import '../../styles/playlists.css'

const Playlists = () => {
    const {playlists} = useContext(Context)
    const [loading, setLoading] = useState(true)


    useEffect(() => {
        playlistsByUid().then(data => {
            playlists.playlists = JSON.parse(data.request.response)
        }).finally(() => setLoading(false))
    }, [])

    if (loading) {
        return '...waiting'
    }

    return (
        <>
        <div className="playlists">
            {playlists.playlists.map((value) => {
                return <Playlist data={value} />
            })}
            <div className="playlist-new">
                <div><Link to="/playlists/new">+</Link></div>
            </div>
        </div>
        </>
    )
}

export default Playlists;