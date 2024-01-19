import { useEffect, useState } from "react"
import Footer from "../components/global/Footer"
import Header from "../components/global/Header"
import { uploadPlaylistAvatar } from "../http/cdn"
import { playlistsCreate } from "../http/playlists"
import { redirect } from "react-router-dom"
import { PROFILE_ROUTE } from "../utils/consts"

const PlaylistNew = () => {
    const [title, setTitle] = useState('Новый плейлист')
    const [description, setDescription] = useState('Новый плейлист')

    const changeTitle = (e) => {
        setTitle(e.target.value)
    }

    const changeDescription = (e) => {
        setDescription(e.target.value)
    }

    const submit = (e) => {
        e.preventDefault()
        if (e.target[2].files[0]) {
            const formData = new FormData()
            formData.append("file", e.target[2].files[0]);
            uploadPlaylistAvatar(formData).then(data => {
                playlistsCreate(title, data.data, description).then(data => {
                    window.location = PROFILE_ROUTE
                })
            })
        } else {
            playlistsCreate(title, "default.jpg", description).then(data => {
                window.location = PROFILE_ROUTE
            })
        }
    }

    return (
        <>
        <Header/>
        <div className="container">
            <div className='leader__title'>Новый плейлист</div>
            <div className="form_container">
                <form onSubmit={submit} enctype='multipart/form-data'>
                    <div className="input_box">
                        <input 
                            name="title"
                            placeholder="Название плейлиста"
                            onChange={changeTitle}
                            value={title}
                            required
                        />
                    </div>
                    <div className="input_box">
                        <textarea 
                            name="description"
                            placeholder="Описание плейлиста"
                            onChange={changeDescription}
                            value={description}
                            required
                        />
                    </div>
                    Аватар плейлиста
                    <div className="input_box">
                        <input 
                            name="avatar"
                            type="file"
                            placeholder="Аватар плейлиста"
                        />
                    </div>
                    <button className="button">Создать</button>
                </form>
            </div>
        </div>
        <Footer/>
        </>
    )
}

export default PlaylistNew