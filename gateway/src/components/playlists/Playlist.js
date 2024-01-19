import { useEffect, useState } from 'react';
import '../../styles/playlist.css'
import { Link } from 'react-router-dom';
import { PLAYLIST_ROUTE } from '../../utils/consts';

const Playlist = (data) => {
    const imageSrc = process.env.REACT_APP_CND_API_HOST + '/playlist/' + data.data.avatar;
    
    return (
        <div className='playlist'>
            <Link to={PLAYLIST_ROUTE + "/" + data.data.id}>
            <div><img src={imageSrc} className="img-playlist" /></div>
            <div>{data.data.title}</div>
            </Link>
        </div>
    )
}

export default Playlist;