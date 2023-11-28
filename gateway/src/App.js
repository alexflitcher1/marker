import { BrowserRouter } from 'react-router-dom';
import AppRouter from './components/AppRouter';
import './styles/reset.css';
import './styles/index.css';
import { useContext, useEffect, useState } from 'react';
import { refresh, userSettings, userStatus } from './http/account';
import { Context } from './index';
import { observer } from 'mobx-react-lite';
import Play from './components/player/Play';
import { likesGet, likesIdsGet } from './http/tracks';
import Header from './components/global/Header';


const App = observer(() => {
  const {user} = useContext(Context)
  const {likes} = useContext(Context)
  const {play} = useContext(Context)
  const [loading, setLoading] = useState(true)
  
  // get user data, settings and user likes
  useEffect(() => {
    userStatus().then(data => {
      user.setUser(JSON.parse(data.request.response))
      user.setIsAuth(true)
      userSettings().then(data => {
        user.setSettings(JSON.parse(data.request.response))
        localStorage.setItem('user-settings', JSON.stringify(user.settings))
      })

    }).catch(() => {
      refresh().then(new_token => {
        localStorage.setItem('access_token', new_token.data.access_token)
      }).catch(() => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      })
    }).finally(() => setLoading(false))
  }, [])

  if (loading) {
    return 'waiting...'
  }

  return (
    <>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500&display=swap" rel="stylesheet" />
    <BrowserRouter>
      <AppRouter />
    </BrowserRouter>
    <Play />
    </>
  );
})

export default App;
