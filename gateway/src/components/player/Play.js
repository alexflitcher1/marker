import { createElement, useContext, useEffect, useState } from "react"
import { Context } from "../..";
import ReactDOM from 'react-dom';
import MetaData from "./MetaData";
import PlayerControls from "./PlayerControls";


const Play = () => {
    const {play} = useContext(Context)
    const {tracks} = useContext(Context)
    const [isPlaying, setIsPlaying] = useState(false)
    const [currentTime, setCurrentTime] = useState(0)
    const [nextState, setNextState] = useState(false)
    const [volume, setVolume] = useState(play.volume)
    const [interval, setIntervalId] = useState(0);

    play.isPlaying = isPlaying
    play.setIsPlaying = setIsPlaying
    const node = document.getElementById('audio'); 
    const audio = ReactDOM.findDOMNode(node);
    
    if (audio) {
        play.duration = audio.duration
        audio.volume = volume/100
        if (play.isPlaying) {
            localStorage.setItem('track-url', play.currentUrl)
            audio.play().catch(() => {})
        } else {
            audio.pause()
        }

        if (currentTime >= audio.duration) {
            clearInterval(interval)
            play.currentIndex = (play.currentIndex + 0.5) % tracks.tracksLength
            if (play.currentIndex % 1 == 0) { 
                play.metaData = tracks.tracks[play.currentIndex]
                play.lastUrl = play.currentUrl
                play.currentUrl = process.env.REACT_APP_CND_API_HOST + '/audio/' + play.metaData.path
                localStorage.setItem('track-metadata', JSON.stringify(play.metaData))
            }
        } else {
            if (!interval) {
                setIntervalId(setInterval(() => {
                    if (ranger) {
                        setCurrentTime(audio.currentTime)
                    }
                }, 1000/24))
            }
        }
    }

    const nodeRanger = document.getElementById('ranger');
    const ranger = ReactDOM.findDOMNode(node);

    const changeTime = (e) => {
        const time = e.target.value
        audio.currentTime = e.target.value
    }

    const changeVolume = (e) => {
        localStorage.setItem('track-volume', e.target.value)
        setVolume(e.target.value)
    }

    return [createElement('div', {className: 'player'}, // root element
        [
            createElement('input', {type: 'range', id: 'ranger', onChange: changeTime, value: currentTime, min: 0, max: play.duration}), // track progress bar
            createElement('div', {className: 'player__controls'}, // controls panel
                [
                    createElement(PlayerControls, {isPlaying: isPlaying, setIsPlaying: setIsPlaying, audio: audio}),
                    createElement(MetaData, {}),
                    createElement('input', {type: 'range', id: 'volume', onChange: changeVolume, value: volume, min: 0, max: 100}) // change volume progress bar
                ])
        ]),
        createElement('audio', { id: 'audio', src: play.currentUrl }, // hidden audio element
    )]
    
}

export default Play;