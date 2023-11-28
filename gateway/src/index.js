import React, { createContext } from 'react';
import ReactDOM from 'react-dom/client';

import App from './App';
import UserStore from './store/UserStore';
import TracksStore from './store/TracksStore';
import PlayStore from './store/PlayStore';
import LikesStore from './store/LikesStore';
import ArtistStore from './store/ArtistStore';

export const Context = createContext(null)

const root = ReactDOM.createRoot(document.getElementById('root'));

const stores = {
  user: new UserStore(),
  tracks: new TracksStore(),
  play: new PlayStore(),
  likes: new LikesStore(),
  artist: new ArtistStore()
}


root.render(
  <React.StrictMode>
    <Context.Provider value={stores}>
      <div className='content'>
        <App />
      </div>
    </Context.Provider>
  </React.StrictMode>
);