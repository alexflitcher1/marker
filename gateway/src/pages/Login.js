import Header from '../components/global/Header';
import Footer from '../components/global/Footer';
import { useState } from 'react';
import auth from '../data/texts';
import ReactDOM from 'react-dom';
import { token } from '../http/account';

function Login() {
    const [login, setLogin] = useState('')
    const [password, setPassword] = useState('')

    const changeLogin = (e) => {
        setLogin(e.target.value)
    }

    const changePassword = (e) => {
        setPassword(e.target.value)
    }

    const submit = (e) => {
        e.preventDefault()
        token(login, password).then(data => {
            localStorage.setItem('access_token', data.data.access_token)
            localStorage.setItem('refresh_token', data.data.refresh_token)
            window.location = '/profile'
        }).catch(() => {
            let node = document.getElementById("error"); 
            let error = ReactDOM.findDOMNode(node);
            error.textContent = auth.ru.errors.errBadRequest
        })
    }

    return (
        <>
        <Header />
        <main className="home">
            <div className="form_container">
                <form onSubmit={submit}>
                    <div className="input_box">
                        <input
                            name="login" 
                            value={login}
                            placeholder={auth.ru.login}
                            onChange={changeLogin}
                            required
                        />
                    </div>
                    <div className="input_box">
                        <input
                            name="password"
                            type="password" 
                            value={password}
                            placeholder={auth.ru.password}
                            onChange={changePassword}
                            required
                        />
                        <div id="error"></div>
                    </div>
                    <button className="button">{auth.ru.signin}</button>
                </form>
            </div>
        </main>
        <Footer />
        </>
    )
}

export default Login