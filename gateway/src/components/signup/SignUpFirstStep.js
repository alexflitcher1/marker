import auth from "../../data/texts";
import '../../styles/login.css';
import { Link } from "react-router-dom";


function SignUpFirstStep({handlers, user}) {
    return (
        <main className="home">
            <div className="form_container">
                <form onSubmit={handlers.submit}>
                    <div className="input_box">
                        <input
                            name="firstName" 
                            value={user.firstName}
                            placeholder={auth.ru.firstName}
                            onChange={handlers.changeFirstName}
                            required
                        />
                    </div>
                    <div className="input_box">
                        <input 
                            name="lastName" 
                            value={user.lastName}
                            placeholder={auth.ru.lastName}
                            onChange={handlers.changeLastName}
                            required
                        />
                    </div>
                    <div className="input_box">
                        <input 
                            name="login" 
                            value={user.login}
                            placeholder={auth.ru.login}
                            onChange={handlers.changeLogin}
                            required
                        />
                        <div className="error" id="error_login"></div>
                    </div>
                    <div className="input_box">
                        <input 
                            name="email" 
                            value={user.email}
                            placeholder={auth.ru.email}
                            onChange={handlers.changeEmail}
                            required
                        />
                        <div className="error" id="error_email"></div>
                    </div>
                    <div className="input_box">
                        <input
                            name="password"
                            type="password"
                            value={user.password}
                            placeholder={auth.ru.password}
                            onChange={handlers.changePassword}
                            required
                        />
                    </div>
                    <div className="input_box">
                        <input 
                            name="relPassword" 
                            type="password"
                            value={user.relPassword}
                            placeholder={auth.ru.relPassword}
                            onChange={handlers.changeRelPassword}
                            required
                        />
                        <div className="error" id="error_password"></div>
                    </div>
                    <div className="login_signup">
                        {auth.ru.alreadyRegistred} 
                        <Link to='/login'>{auth.ru.login_link}</Link>
                    </div>
                    <button className="button">{auth.ru.sumbit}</button>
                </form>
            </div>
        </main>
    )
}

export default SignUpFirstStep