import { useNavigate } from "react-router-dom";
import {Animated} from "react-animated-css";
import ParticlesApp from "../Login/Particles";

const GameOver = () => {
    const navigate = useNavigate()
    const gotoGame = async () => {
        navigate("/game", {shallow: true})
    }

    const signOut = () => {
        localStorage.clear()
        navigate("/")
    }

    return (
        <div className="min-h-screen flex justify-center text-center z-10 bg-black">
            <div className="mt-20">
                <Animated animationIn="fadeInDownBig" animationOut="fadeOut" isVisible={true}>
                    <h1 className="text-7xl lg:text-9xl">GAME OVER</h1>
                </Animated>

                <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                </div>
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
            </div>
        </div>
    );
};

export default GameOver;