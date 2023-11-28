import { useParams } from "react-router-dom";
import Footer from "../components/global/Footer";
import Header from "../components/global/Header";
import { useContext, useEffect, useState } from "react";
import "../styles/artist.css";
import { artistData, artistLike, artistLikeIds } from "../http/artists";
import { Context } from "..";
import Main from "../components/artist/Main";
import Albums from "../components/artist/Albums";
import Tracks from "../components/artist/Tracks";

const Artist = () => {
    const components = {
        1: <Main />,
        2: <Albums />,
        3: <Tracks />
    }

    const params = useParams()
    const {artist} = useContext(Context);
    const {likes} = useContext(Context);
    const [active, setActive] = useState(['active', '', '']);
    const [currentComponent, setComponent] = useState(components[1]);
    const [loading, setLoading] = useState(true);
    const [isLike, setLike] = useState(false);

    useEffect(() => {
        artistLikeIds().then(data => {
            likes.artistLikes = JSON.parse(data.request.response);
            setLike(likes.artistLikes.indexOf(params.id*1) !== -1);
        });
        artistData(params.id).then(data => {
            artist.artist = JSON.parse(data.request.response);
        }).finally(() => setLoading(false));
    }, []);

    if (loading) {
        return 'waiting..';
    }

    const backgroundUrl = process.env.REACT_APP_CND_API_HOST + '/artist-background/' + artist.artist.background;
    const avatarUrl = process.env.REACT_APP_CND_API_HOST + '/artist-avatar/' + artist.artist.avatar;

    const tabClick = (e) => {
        const id = e.target.id;
        let newActive = ['', '', ''];
        newActive[id-1] = 'active';
        setComponent(components[id])
        setActive(newActive);
    }

    const like = (e) => {
        artistLike(params.id).then(data => {
            setLike(!isLike)
        });
    }

    return (
        <>
            <Header />
            <div className='container'>
                <div className='leader__title'>Главная</div>
                <div className='user__images'>
                    <div className='user__background'><img src={backgroundUrl} /><div id='mask'></div></div>
                    <div className='user__avatar'><img src={avatarUrl} /></div>
                    <div className='user__names'>
                        <div className="title">{artist.artist.name}</div>
                        <div className="title"><div className={isLike ? 'like__artist liked' : 'like__artist like'} onClick={like}></div></div>
                    </div>
                </div>
                <div className='tabs-link'>
                    <div id="1" onClick={tabClick} className={'tab ' + active[0]}>Главная</div>
                    <div id="2" onClick={tabClick} className={'tab ' + active[1]}>Альбомы</div>
                    <div id="3" onClick={tabClick} className={'tab ' + active[2]}>Треки</div>
                </div>
                <hr />
                <div>
                    {currentComponent}
                </div>
            </div>
            <Footer />
        </>
    )
}


export default Artist