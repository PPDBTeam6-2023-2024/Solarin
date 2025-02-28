import {useContext, useState} from "react"
import {IoMdMenu, IoIosSettings} from "react-icons/io";
import {RiArrowRightSLine} from "react-icons/ri";
import {FaSignOutAlt} from "react-icons/fa";
import Settings from "../Settings/Settings";
import {useNavigate} from "react-router-dom";
import {PrimaryContext, SecondaryContext, TertiaryContext} from "../../Context/ThemeContext";

// display the hamburger menu in the top right
function SideMenu(props) {
    const [menuOpen, setMenuOpen] = useState(false)
    const [settingsOpen, setSettingsOpen] = useState(false)
    const navigate = useNavigate()
    const signOut = () => {
        localStorage.clear()
        navigate("/")
    }
    const buttonStyle = "flex items-center mt-3 transition-all ease-in-out hover:scale-110"

    const [primaryColor, setPrimaryColor] = useContext(PrimaryContext);
    const [secondaryColor, setSecondaryColor] = useContext(SecondaryContext);
    const [tertiaryColor, setTertiaryColor] = useContext(TertiaryContext);

    return (
        <>
            <Settings viewSettings={settingsOpen} onClose={() => setSettingsOpen(false)}/>
            <div className="right-0 fixed z-10 text-5xl text-center">
                {!menuOpen &&
                    <IoMdMenu
                        className="right-0 absolute z-20 transition ease-in-out hover:scale-125 hover:-translate-x-1 hover:translate-y-1"
                        onClick={() => setMenuOpen(!menuOpen)}/>
                }
                <>
                    <div
                    className={`transition-all duration-300 ease-out ${(menuOpen) ? "" : "hidden"} h-full p-5 text-center`}
                    style={{
                        "backgroundImage": `linear-gradient(5deg, ${primaryColor}, ${secondaryColor}`,
                        "border": `solid 0.2vw ${tertiaryColor}`
                    }}
                    >
                        <RiArrowRightSLine className="transition-all ease-in-out hover:scale-110 m-0 absolute"
                                           onClick={() => setMenuOpen(!menuOpen)}/>
                        <br/>
                        <div className="text-3xl">
                            <h4 className={buttonStyle} onClick={() => {
                                setSettingsOpen(!settingsOpen)
                            }}><IoIosSettings className="mr-2"/>Settings</h4>
                            <h4 className={buttonStyle} onClick={signOut}><FaSignOutAlt className="mr-2"/>Sign Out</h4>
                        </div>
                    </div>
                </>
            </div>
        </>
    )
}

export default SideMenu