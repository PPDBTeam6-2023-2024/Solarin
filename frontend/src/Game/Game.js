import { useEffect, useState, Suspense} from "react"
import axios from 'axios'
import PlanetViewer from "./PlanetViewer/PlanetViewer"
import GalaxyViewer from "./GalaxyViewer/GalaxyViewer"
import SideMenu from "./UI/SideMenu/SideMenu"

import { RiArrowLeftSLine } from "react-icons/ri";
import { IoMdPlanet } from "react-icons/io";

import planet_example from './Images/Planets/example.png'

// enum 
const ViewMode = {
    GalaxyView: "GalaxyView",
    PlanetView: "PLanetView",
    CityView: "CityView",
}

const Game = () => {
    const [isAuth, setIsAuth] = useState(false)
    const [userInfo, setUserInfo] = useState(null)
    const [viewMode, setViewMode] = useState(ViewMode.PlanetView)


    const authenticate = async() => {
        try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/auth/me`)
        if (response.status === 200) {
            setIsAuth(true)
            setUserInfo(response.data)
        }
        }
        catch(error) {
            setIsAuth(false)
        }
    }

    useEffect(() => {
        authenticate()
    }, [])
    return (<div className="h-screen bg-gray-900">
        {userInfo && <Suspense fallback={<h1>Loading...</h1>}>
            <SideMenu/>                
            {viewMode === ViewMode.PlanetView &&
            <>
            <div onClick={() => setViewMode(ViewMode.GalaxyView)} className="fixed text-5xl z-10 transition ease-in-out hover:scale-150 hover:translate-x-5 hover:translate-y-1 duration-300 flex">
            <RiArrowLeftSLine className="basis-1/4"/>
            <IoMdPlanet/>
            </div>
            <PlanetViewer mapImage={planet_example} planetName="Terra"/>
            </>
            }

            {viewMode === ViewMode.GalaxyView &&
            <GalaxyViewer mapImage={planet_example}/>
            }
            </Suspense>
            }
        {!userInfo && !isAuth && <h1>Not authenticated</h1>}
    </div>)
}
export default Game