import { useContext, useState } from "react"
import ReactDOM from 'react-dom';
import { Context } from "../..";
import Likes from "./Likes";
import TrackData from "./TrackData";


const Track = ({ info, liked, page, index }) => {
    const {play} = useContext(Context);
    const {tracks} = useContext(Context);

    const audioSrc = process.env.REACT_APP_CND_API_HOST + '/audio/' + info.path
    var [show, setShow] = useState(false)

    const playTrack = (e) => {
        tracks.lastTracksType = tracks.tracksType;
        tracks.tracksType = page;
        tracks.setTracks(tracks.tracksPrepared);
        localStorage.setItem('last-query', JSON.stringify(tracks.tracks));
        const id = "audio_" + e.target.id.slice(7)
        const node = document.getElementById(id); 
        const audio = ReactDOM.findDOMNode(node);
        audio.volume = 0.1

        play.lastUrl = play.currentUrl
        play.currentUrl = audio.childNodes[0].getAttribute('data-src')

        if (!play.isPlaying) {
            play.setIsPlaying(!play.isPlaying)
            play.isPlaying = !play.isPlaying
        } else {
            play.setIsPlaying(!play.isPlaying)
            play.isPlaying = !play.isPlaying
        }

        if (play.lastUrl !== play.currentUrl) {
            play.setIsPlaying(true)
            play.currentIndex = index
            localStorage.setItem('track-metadata', JSON.stringify(info))
            play.metaData = info
        }
    }

    return (
        <div className='track'
            onMouseEnter={() => setShow(true)}
            onMouseLeave={() => setShow(false)}
        >
            <div className="track-index">{index+1}</div>
            {show ?
            <button onClick={playTrack} id={"button_" + info.id} className="play">⏵︎</button> 
            :
            ''}
            <TrackData info={info} />
            <Likes liked={liked} id={info.id} show={show} />
            <div>
                <div id={'audio_' + info.id}>
                    <div data-src={audioSrc}></div>
                </div>
            </div>
        </div>
    )
}

export default Track