import { Routes, Route, Navigate } from 'react-router-dom';
import { authRoutes, publicRoutes } from '../routes';
import { SIGNUP_ROUTE } from '../utils/consts';
import { useContext } from 'react';
import { Context } from '..';
import { refresh, userStatus } from '../http/account';

const AppRouter = () => {
    const {user} = useContext(Context)

    return (
        <Routes>
            {user.isAuth && authRoutes.map(({path, Element}) =>
                <Route key={path} path={path} element={Element} exact />
            )}
            {publicRoutes.map(({path, Element}) =>
                <Route key={path} path={path} element={Element} exact />
            )}
            <Route key="_for_all" path="*" element={<Navigate to={SIGNUP_ROUTE} replace />}/>
        </Routes>
    )
}

export default AppRouter