import { Link } from 'react-router-dom'
import header from '../../data/header'
import '../../styles/header.css'
import { useContext } from 'react';
import { Context } from '../..';
import { MAIN_PAGE_ROUTE, PROFILE_ROUTE, SIGNUP_ROUTE } from '../../utils/consts';

function Header() {
    const {user} = useContext(Context)
    
    return (
        <header className="header">
            <nav className="nav">
                <Link to={MAIN_PAGE_ROUTE} className='nav_logo'>{header.projectName}</Link>
                <ul className="nav_items">
                    <li className="nav_item">
                        <Link to={MAIN_PAGE_ROUTE} className='nav_link'>{header.ru.home}</Link>
                    </li>
                </ul>
                {user.isAuth ? 
                <button className="button" id="form-open"><Link to={PROFILE_ROUTE} className='nav_link'>Профиль</Link></button>
                :
                <button className="button" id="form-open"><Link to={SIGNUP_ROUTE} className='nav_link'>{header.ru.login}</Link></button>
                }
            </nav>
      </header>
    )
}

export default Header