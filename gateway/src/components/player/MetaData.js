import { useContext } from "react"
import { Context } from "../.."

const MetaData = () => {
    const {play} = useContext(Context)
    const src = process.env.REACT_APP_CND_API_HOST + '/img/' + play.metaData.avatar
    if (play === null) {
        return 0
    }

    return (
        <>
        <div className="player__meta">
            <div className='avatar'><img className='avatar__img_player' src={src} /></div>
            <div className="metadata">
                <div>{play.metaData.title}</div>
                <div className='artists'>
                    {play.metaData.artists ? 
                    play.metaData.artists.map((val) => {
                        return <div key={val.id} className='artist'>{val.name}</div>
                    })
                    : ''}
                </div>
            </div>
        </div>
        </>
    )

}

export default MetaData;