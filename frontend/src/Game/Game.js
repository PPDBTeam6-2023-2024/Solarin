import {useEffect, useState, Suspense} from "react"
import axios from 'axios'
import PlanetViewer from "./PlanetViewer/PlanetViewer"
import GalaxyViewer from "./GalaxyViewer/GalaxyViewer"
import UI from "./UI/UI"
import {ViewModeContext, View} from "./Context/ViewModeContext"
import ProfileViewer from "./UI/MainUI/ProfileViewer";
import {RiArrowLeftSLine} from "react-icons/ri";
import {IoMdPlanet} from "react-icons/io";
import {UserInfoContext} from "./Context/UserInfoContext"

import planet_example from './Images/Planets/example.png'
import {PlanetListContext} from "./Context/PlanetListContext"

const Game = () => {
    const [isAuth, setIsAuth] = useState(false)
    const [userInfo, setUserInfo] = useState(null)
    const [viewMode, setViewMode] = useState(View.PlanetView)
    const [planetList, setPlanetList] = useState([[1, "Terra"]])
    const [planetListIndex, setPlanetListIndex] = useState(0)

    const authenticate = async () => {
        try {
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/auth/me`)
            if (response.status === 200) {
                setIsAuth(true)
                setUserInfo(response.data)
            }
        } catch (error) {
            setIsAuth(false)
        }
    }

    const setPlanetListToDefault = async () => {
        setPlanetList([[1, "Terra"]])
    }

    const getAllPlanets = async () => {
        /*retrieve a list of planet id's and planet names to switch between them*/
        try {
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/planets`)
            if (response.data.length > 0) setPlanetList(response.data)
            else setPlanetListToDefault()
        } catch (error) {
            setPlanetListToDefault()
        }
    }

    const changePlanetId = (planetId) => {
        const newIndex = planetList.findIndex(planet => planet[0] === planetId);
        if (newIndex !== -1) {
            setPlanetListIndex(newIndex);
        } else {
            console.error("Planet with the given ID not found.");
        }
    };


    useEffect(() => {
        authenticate()
        getAllPlanets()
    }, [])
    return (<div className="h-screen bg-gray-900">
        <UserInfoContext.Provider value={[userInfo, setUserInfo]}>
            <ViewModeContext.Provider value={[viewMode, setViewMode]}>
                <PlanetListContext.Provider value={[planetList, setPlanetList]}>

                    {userInfo && <Suspense fallback={<h1>Loading...</h1>}>
                        <UI/>
                        {viewMode === View.PlanetView &&
                            <>
                                <div onClick={() => setViewMode(View.GalaxyView)}
                                     className="fixed text-5xl z-10 transition ease-in-out hover:scale-150 hover:translate-x-5 hover:translate-y-1 duration-300 flex">
                                    <RiArrowLeftSLine className="basis-1/4"/>
                                    <IoMdPlanet/>
                                </div>
                                <PlanetViewer mapImage={planet_example} planetName={planetList[planetListIndex][1]}
                                              planetId={planetList[planetListIndex][0]}
                                              planetListIndex={[planetListIndex, setPlanetListIndex]}/>
                            </>
                        }

                        {viewMode === View.GalaxyView &&
                            <GalaxyViewer mapImage={planet_example}/>
                        }

                        {viewMode === View.ProfileView &&
                            <ProfileViewer changePlanetByID={changePlanetId}/>
                        }

                    </Suspense>
                    }


                    {!userInfo && !isAuth && <h1>Not authenticated</h1>}

                </PlanetListContext.Provider>
            </ViewModeContext.Provider>
        </UserInfoContext.Provider>
    </div>)
}
export default Game