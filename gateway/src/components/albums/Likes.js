import { useState } from "react"
import { albumLike } from "../../http/albums"

const Likes = ( { liked, id, show } ) => {
    const [isLike, setLike] = useState(!!liked);

    const like = (e) => {
        albumLike(id).then(data => {
            setLike(!isLike)
        })
    }

    return (
        <>
        {show ?  
        <div className="like-album">
            <div className={isLike ? 'like__album liked' : 'like__album like'} onClick={like}></div>
        </div>
        : ''}
        </>
    )
}

export default Likes