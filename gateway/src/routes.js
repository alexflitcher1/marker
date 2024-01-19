import Signup from './pages/Signup';
import MainPage from './pages/MainPage';
import { MAIN_PAGE_ROUTE, SIGNUP_ROUTE, LOGIN_ROUTE, PROFILE_ROUTE, ARTIST_ROUTE, SEARCH_ROUTE, PLAYLIST_NEW_ROUTE, PLAYLIST_ROUTE } from './utils/consts';
import Login from './pages/Login';
import Profile from './pages/Profile';
import Artist from './pages/Artist';
import Search from './pages/Search';
import PlaylistNew from './pages/PlaylistNew';
import Playlist from './pages/Playlist';


export const authRoutes = [
    {
        path: MAIN_PAGE_ROUTE,
        Element: <MainPage />
    },
    {
        path: PROFILE_ROUTE,
        Element: <Profile />
    },
    {
        path: PLAYLIST_NEW_ROUTE,
        Element: <PlaylistNew />
    }
]

export const publicRoutes = [
    {
        path: SIGNUP_ROUTE,
        Element: <Signup />
    },
    {
        path: LOGIN_ROUTE,
        Element: <Login />
    },
    {
        path: ARTIST_ROUTE + '/:id',
        Element: <Artist />
    },
    {
        path: SEARCH_ROUTE + '/:query',
        Element: <Search />
    },
    {
        path: PLAYLIST_ROUTE + '/:id',
        Element: <Playlist />
    }
]