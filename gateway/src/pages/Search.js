import { Link, useParams } from "react-router-dom"
import Footer from "../components/global/Footer"
import Header from "../components/global/Header"
import { useContext, useEffect, useState } from "react"
import { search } from "../http/search"
import Track from "../components/tracks/Track"
import Album from "../components/albums/Album"
import { Context } from ".."
import { albumLikesIdsGet } from "../http/albums"
import { ARTIST_ROUTE } from "../utils/consts"
import Artist from "../components/artists/Artist"
import { likesIdsGet } from "../http/tracks"

const Search = () => {
    const params = useParams()
    const [searchResults, setResults] = useState({tracks: [], albums: [], artists: []})
    const {likes} = useContext(Context)
    const {tracks} = useContext(Context)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        likesIdsGet().then(data => {
            likes.likes = JSON.parse(data.request.response);
            console.log(likes.likes)
        });
        albumLikesIdsGet().then(data => {
            likes.albumLikes = JSON.parse(data.request.response);
        });
    }, [])

    useEffect(() => {
        setLoading(true)
        search(params.query).then((data) => {
            setResults(JSON.parse(data.request.response))
            tracks.tracksPrepared = JSON.parse(data.request.response).tracks
        }).finally(() => setLoading(false))
    }, [params.query])

    if (loading) {
        return "...waiting"
    }

    return (
        <>
        <Header />
        <div className='container'>
            <div className="leader__title">Результаты поиска</div>
            <hr />
            <div className="tracks-search">
                <div className="dep__title">Треки</div>
                <div className="track-search">
                    {searchResults.tracks.map((value, i) => {
                        if (likes.likes.length > 0) {
                            if (likes.likes.indexOf(value.id) !== -1 )
                                return <Track info={value} page={'track-search'} liked={true} index={i} /> 
                        }
                        return <Track info={value} page={'track-search'} liked={false} index={i} /> 
                    })}
                </div>
            </div>
            <hr />
            <div className="tracks-albums">
                <div className="dep__title">Альбомы</div>
                <div className="albums">
                    {searchResults.albums.map((value) => {
                        return <Album data={value}/> 
                    })}
                </div>
            </div>
            <hr/>
            <div className="tracks-artists">
                <div className="dep__title">Артисты</div>
                <div className="artists">
                    {searchResults.artists.map((value) => {
                        return <Artist data={value} />
                    })}
                </div>
            </div>
        </div>
        <Footer />
        </>
    )
}

export default Search