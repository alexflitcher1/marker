import Header from '../components/global/Header';
import Footer from '../components/global/Footer';
import '../styles/profile.css';
import { useContext, useState } from 'react';
import { Context } from '..';
import { Link } from 'react-router-dom';
import Likes from '../components/profile/Likes';
import Albums from '../components/profile/Albums';
import Playlists from '../components/profile/Playlists';
import Artists from '../components/profile/Artists';

function Profile() {
    const components = {
        1: <Playlists />,
        2: <Likes />,
        3: <Albums />,
        4: <Artists />
    }

    const {user} = useContext(Context);
    const [active, setActive] = useState(['', 'active', '', '']);
    const [currentComponent, setComponent] = useState(components[2]);
    const backgroundUrl = process.env.REACT_APP_CND_API_HOST + '/background/' + user.settings.background;
    const avatarUrl = process.env.REACT_APP_CND_API_HOST + '/avatar/' + user.settings.avatar;

    const tabClick = (e) => {
        const id = e.target.id;
        let newActive = ['', '', '', ''];
        newActive[id-1] = 'active';
        setComponent(components[id])
        setActive(newActive);
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
                        <div className='title'>{user.user.firstName}</div>
                        <div className='title'>{user.user.login}</div>
                        <div className='title'>{user.user.lastName}</div>
                    </div>
                </div>
                <div className='tabs-link'>
                    <div id="1" onClick={tabClick} className={'tab ' + active[0]}>Плейлисты</div>
                    <div id="2" onClick={tabClick} className={'tab ' + active[1]}>Любимое</div>
                    <div id="3" onClick={tabClick} className={'tab ' + active[2]}>Альбомы</div>
                    <div id="4" onClick={tabClick} className={'tab ' + active[3]}>Исполнители</div>
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

export default Profile