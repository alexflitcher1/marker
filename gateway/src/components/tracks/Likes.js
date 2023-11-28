import { useState } from "react"
import { likeTrack } from "../../http/tracks"

const Likes = ( { liked, id, show } ) => {
    const [isLike, setLike] = useState(!!liked)

    const like = (e) => {
        likeTrack(id).then(data => {
            setLike(!isLike)
        }).catch(error => {})
    }

    return show ? <div className={isLike ? 'like__contaiter liked' : 'like__contaiter like'} onClick={like}></div> : ''
}

export default Likes