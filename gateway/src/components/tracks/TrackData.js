import { Link } from "react-router-dom";
import { ARTIST_ROUTE } from "../../utils/consts"


const TrackData = ({ info }) => {
    const src = process.env.REACT_APP_CND_API_HOST + '/img/' + info.avatar
    return (
        <>
        <div className='avatar'><img className='avatar__img' src={src} /></div>
        <div>
            <div key={info.id}>{info.title}</div>
            <div className='artists'>
                {info.artists.map((val) => 
                    <div key={val.id} className='artist'><Link to={ARTIST_ROUTE + '/' + val.id}>{val.name}</Link></div>
                )}
            </div>
        </div>
        </>
    )
}

export default TrackData;