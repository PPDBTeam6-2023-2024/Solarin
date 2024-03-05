import { useState } from "react"
import { IoMdMenu } from "react-icons/io";
import { RiArrowRightSLine } from "react-icons/ri";

function SideMenu() {
    const [menuOpen, setMenuOpen] = useState(false)
    return(
        <div className="right-0 fixed z-10 text-5xl text-center">
            { !menuOpen &&
            <IoMdMenu className="right-0 absolute z-20 transition ease-in-out hover:scale-125 hover:-translate-x-1 hover:translate-y-1" onClick={() => setMenuOpen(!menuOpen)}/>
            }
            <>
            <div className={`border-2 border-white bg-gray-800 transition-all duration-300 ease-out ${(menuOpen)?"opacity-100" : "opacity-0"} h-full p-5 text-center`}>
            <RiArrowRightSLine className="transition-all ease-in-out hover:scale-110" onClick={() => setMenuOpen(!menuOpen)}/>
            </div>
            </>
        </div>
    )
}
export default SideMenu