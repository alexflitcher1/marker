import Signup from './pages/Signup';
import MainPage from './pages/MainPage';
import { RouteObject } from "react-router-dom";
import { MAIN_PAGE_ROUTE, SIGNUP_ROUTE, LOGIN_ROUTE, PROFILE_ROUTE, ARTIST_ROUTE } from './utils/consts';
import Login from './pages/Login';
import Profile from './pages/Profile';
import Artist from './pages/Artist';


export const authRoutes: RouteObject[] = [
    {
        path: MAIN_PAGE_ROUTE,
        Element: <MainPage />
    },
    {
        path: PROFILE_ROUTE,
        Element: <Profile />
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
    }
]