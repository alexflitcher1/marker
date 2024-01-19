import { useParams } from "react-router-dom";
import Header from "../components/global/Header";
import Footer from "../components/global/Footer";

const Playlist = () => {
    const params = useParams();

    return (
        <>
        <Header />
        <Footer />
        </>
    )
}

export default Playlist;