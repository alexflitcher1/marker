import { Link } from "react-router-dom";
import { ARTIST_ROUTE } from "../../utils/consts";
import '../../styles/artist-component.css';


const Artist = ({ data }) => {
    const avatarUrl = process.env.REACT_APP_CND_API_HOST + '/artist-avatar/';
    return (
        <div className="artist-component-link">
            <Link to={ARTIST_ROUTE + '/' + data.id}>
                <div className="artist-link">
                    <div><img src={avatarUrl + data.avatar} /></div>
                    <div>{data.name}</div>
                </div>
            </Link>
        </div>
    )
}

export default Artist