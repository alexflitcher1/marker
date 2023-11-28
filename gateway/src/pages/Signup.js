import Footer from "../components/global/Footer";
import Header from "../components/global/Header";
import auth from "../data/texts";
import { useContext, useState } from 'react';
import '../styles/login.css';
import ReactDOM from 'react-dom';
import SignUpFirstStep from "../components/signup/SignUpFirstStep";
import SignUpVerifyCode from "../components/signup/SignUpVerifyCode";
import {token, signup, create, userStatus, userSettings} from '../http/account'
import { Context } from '..';
import { useNavigate } from "react-router-dom";


function SignUp() {
    const [firstName, setFirstName] = useState('')
    const [lastName, setLastName] = useState('')
    const [login, setLogin] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [relPassword, setRelPassword] = useState('')
    const [isSecondStep, setStep] = useState(false)
    const [code, setCode] = useState('')
    const [valid, setValid] = useState(true)
    const history = useNavigate()

    const {user} = useContext(Context)

    const mail = {
        email: email,
        code: code
    }

    const userData = {
        firstName: firstName,
        lastName: lastName,
        login: login,
        email: email,
        password: password,
        relPassword: relPassword 
    }

    function changeFirstName(e) {
        setFirstName(e.target.value)
    }

    function changeLastName(e) {
        setLastName(e.target.value)
    }

    function changeLogin(e) {
        setLogin(e.target.value)

        let node = document.getElementById("error_login"); 
        let error = ReactDOM.findDOMNode(node);
        if (userData.login.length < 3) {
            error.textContent = auth.ru.errors.login
            setValid(false)
        } else {
            error.textContent = ''
            setValid(true)
        }
    }

    function changeEmail(e) {
        setEmail(e.target.value)
        
        const re = new RegExp(/^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$/, "img"); 
        const node = document.getElementById("error_email"); 
        let error = ReactDOM.findDOMNode(node);
        if (!re.exec(e.target.value)) {
            error.textContent = auth.ru.errors.email
            setValid(false)
        } else {
            error.textContent = ''
            setValid(true)
        }
    }

    function changePassword(e) {
        setPassword(e.target.value)
    }

    function changeRelPassword(e) {
        setRelPassword(e.target.value)
        const node = document.getElementById("error_password"); 
        let error = ReactDOM.findDOMNode(node);
        if (userData.password !== e.target.value) {
            error.textContent = auth.ru.errors.password
            setValid(false)
        } else {
            error.textContent = ''
            setValid(true)
        }
    }
    
    async function submit(e) {
        e.preventDefault()
        if (!valid) {
            return 0;
        }
        
        await signup(userData).then(() => {
            setStep(!isSecondStep)
        }).catch((error) => {
            if (error.code == 'ERR_BAD_REQUEST') {
                let node = document.getElementById("error_password"); 
                let error = ReactDOM.findDOMNode(node);
                if (userData.password !== e.target.value) {
                    error.textContent = auth.ru.errors.errBadRequest
                } else {
                    error.textContent = ''
                }
            }
        })
    }

    async function submitForMail(e) {
        e.preventDefault(e)
        await create(userData, mail).then(data => {
            const tokens = async () => {
                await token(userData.login, userData.password).then(data => {
                    localStorage.setItem('access_token', data.data.access_token)
                    localStorage.setItem('refresh_token', data.data.refresh_token)
                    window.location = '/'
                }).catch(error => {

                })
            }
            tokens()
        }).catch(error => {
            if (error.code == 'ERR_BAD_REQUEST') {
                let node = document.getElementById("error"); 
                let error = ReactDOM.findDOMNode(node);
                if (userData.password !== e.target.value) {
                    error.textContent = auth.ru.errors.errBadRequest
                } else {
                    error.textContent = ''
                }
            }
        })
    }

    function changeCode(e) {
        setCode(e.target.value)
    }

    const handlersForFirst = {
        submit: submit,
        changeFirstName: changeFirstName,
        changeLastName: changeLastName,
        changeLogin: changeLogin,
        changePassword: changePassword,
        changeEmail: changeEmail,
        changeRelPassword: changeRelPassword
    }

    const handlersForMail = {
        submit: submitForMail,
        changeCode: changeCode
    }

    return (
        <>
            <Header />
                {isSecondStep ? 
                    <SignUpVerifyCode 
                        handlers={handlersForMail}
                        mail={mail} 
                    />
                    : 
                    <SignUpFirstStep 
                        handlers={handlersForFirst} 
                        user={userData}
                    /> 
                }
            <Footer />
        </>
    )
}

export default SignUp