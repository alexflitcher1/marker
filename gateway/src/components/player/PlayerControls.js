import { useContext, useEffect, useState } from "react"
import { Context } from "../.."

const PlayerControls = ({ isPlaying, setIsPlaying, audio }) => {
    const {play} = useContext(Context)
    const {tracks} = useContext(Context)
    const [currentClass, setCurrentClass] = useState('button_play')
    

    const changeState = (e) => {
        play.lastUrl = play.currentUrl

        if (currentClass == 'button_pause') {
            setCurrentClass('button_play')
        } else if (currentClass == 'button_play') {
            setCurrentClass('button_pause')
        }

        play.currentUrl = play.lastUrl
        play.isPlaying = !play.isPlaying
        setIsPlaying(play.isPlaying)
    }

    const prevTrack = (e) => {
        if (audio.currentTime <= 5) {
            setCurrentClass('button_pause')
            play.currentIndex = play.currentIndex > 0 ? (play.currentIndex - 1) % tracks.tracksLength: tracks.tracksLength-1
            play.metaData = tracks.tracks[play.currentIndex]
            play.lastUrl = play.currentUrl
            play.currentUrl = process.env.REACT_APP_CND_API_HOST + '/audio/' + play.metaData.path
            localStorage.setItem('track-url', JSON.stringify(play.currentUrl))
            localStorage.setItem('track-metadata', JSON.stringify(play.metaData))
        } else {
            audio.currentTime = 0
        }
    }

    const nextTrack = (e) => {
        setCurrentClass('button_pause')
        play.currentIndex = (play.currentIndex + 1) % tracks.tracksLength
        play.metaData = tracks.tracks[play.currentIndex]
        play.lastUrl = play.currentUrl
        play.currentUrl = process.env.REACT_APP_CND_API_HOST + '/audio/' + play.metaData.path
        localStorage.setItem('track-url', JSON.stringify(play.currentUrl))
        localStorage.setItem('track-metadata', JSON.stringify(play.metaData))
    }

    return (
        <>
            <button className="button__circle prev_icon" onClick={prevTrack}></button>
            <button className={`button__circle ${currentClass}`} id="state__control" onClick={changeState}></button>
            <button className="button__circle next_icon" onClick={nextTrack}></button>
        </>
    )
}

export default PlayerControls;