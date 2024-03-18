import { useState } from "react"
import { IoMdMenu, IoIosSettings } from "react-icons/io";
import { RiArrowRightSLine } from "react-icons/ri";
import { FaSignOutAlt } from "react-icons/fa";
import Settings from "../Settings/Settings";

function SideMenu(props) {
    const [menuOpen, setMenuOpen] = useState(false)
    const [settingsOpen, setSettingsOpen] = useState(false)
    const signOut = () => {
        localStorage.clear()
        props.setIsAuth(false)
    }
    const buttonStyle = "flex items-center mt-3 transition-all ease-in-out hover:scale-110"
    return(
        <>
        <Settings viewSettings={settingsOpen}/>
        <div className="right-0 fixed z-10 text-5xl text-center">
            { !menuOpen &&
            <IoMdMenu className="right-0 absolute z-20 transition ease-in-out hover:scale-125 hover:-translate-x-1 hover:translate-y-1" onClick={() => setMenuOpen(!menuOpen)}/>
            }
            <>
            <div className={`border-2 border-white bg-gray-800 transition-all duration-300 ease-out ${(menuOpen)?"opacity-100" : "opacity-0"} h-full p-5 text-center`}>
            <RiArrowRightSLine className="transition-all ease-in-out hover:scale-110 m-0 absolute" onClick={() => setMenuOpen(!menuOpen)}/>
            <br/>
            <div className="text-3xl">
            <h4 className={buttonStyle} onClick={() => {setSettingsOpen(!settingsOpen)}}><IoIosSettings className="mr-2"/>Settings</h4>
            <h4 className={buttonStyle} onClick={signOut}><FaSignOutAlt className="mr-2"/>Sign Out</h4>
            </div>
            </div>
            </>
        </div>
        </>
    )
}
export default SideMenu