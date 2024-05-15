import { useNavigate } from "react-router-dom";

const GameOver = () => {
    const navigate = useNavigate()
    const gotoGame = async () => {
        navigate("/game", {shallow: true})
    }

    const signOut = () => {
        setIsSignedIn(false)
        localStorage.clear()
    }

    return (
        <Animated animationIn="flipInY" animationOut="fadeOut" isVisible={true}
            animationInDuration={500}>
        <button onClick={gotoGame}
                className="mt-10 bg-transparent hover:bg-white text-white-700 font-semibold hover:text-black py-6 px-20 border border-white-500 rounded text-5xl">
            PLAY AGAIN
        </button>
        <br/>
        <button onClick={signOut} value="Sign Out"
                className="my-3 justify-center rounded-md bg-transparent hover:bg-white hover:text-black px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-white-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white-600">
            Sign out
        </button>
        </Animated>
    );
};

export default GameOver;