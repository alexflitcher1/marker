import auth from "../../data/texts";
import '../../styles/login.css';


function SignUpVerifyCode({user, mail, handlers}) {
    return (
        <main className="home">
            <div className="form_container">
                <form onSubmit={handlers.submit}>
                    <div className="input_box">
                        <input
                            name="code" 
                            value={mail.code}
                            placeholder={auth.ru.code}
                            onChange={handlers.changeCode}
                            required
                        />
                        <div className="error" id="error"></div>
                    </div>
                    <button className="button">{auth.ru.sumbit}</button>
                </form>
            </div>
        </main>
    )
}

export default SignUpVerifyCode