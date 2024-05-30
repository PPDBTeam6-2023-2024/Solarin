import {useEffect, useState, Suspense, useRef} from "react"
import axios from 'axios'
import PlanetViewer from "./PlanetViewer/PlanetViewer"
import GalaxyViewer from "./GalaxyViewer/GalaxyViewer"
import UI from "./UI/UI"
import {ViewModeContext, View} from "./Context/ViewModeContext"
import ProfileViewer from "./UI/ProfileViewer/ProfileViewer";
import {RiArrowLeftSLine} from "react-icons/ri";
import {IoMdPlanet} from "react-icons/io";
import {UserInfoContext} from "./Context/UserInfoContext"

import {PlanetListContext} from "./Context/PlanetListContext"

import ColorManager from "./ColorManager";
import Notification from "./UI/CombatNotifications/Notification";
import MaintenanceHook from "./Hooks/MaintenanceHook";
import GlobalHook from "./Hooks/GlobalHook";
const Game = () => {
    /**
     * This Component is the general component containing the entire game
     * All game related content is part of this component
     */

    /*
    * Keep track whether the user is authenticated and its user information
    * */
    const [isAuth, setIsAuth] = useState(false)
    const [userInfo, setUserInfo] = useState(null)

    /*
    * Tracks which view the user is lookup at
    * */
    const [viewMode, setViewMode] = useState(View.PlanetView)

    /*
    * Stores the list of all planets the user can access (planets with an army or city on it)
    * */
    const [planetList, setPlanetList] = useState([])

    /*
    * Stores the index of the planet the player is currently looking at
    * By default it will display the first planet in the list
    * */
    const [planetListIndex, setPlanetListIndex] = useState(0)

    /*
    * Support the global websocket actions using a custom hook
    * */
    const [combatNotifications, setCombatNotifications] = useState([]);
    GlobalHook(setCombatNotifications)

    /*
    * Verify who the user is
    * */
    const authenticate = async () => {
        try {
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`,
         'content-type': 'application/x-www-form-urlencoded',
         'accept': 'application/json'}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/auth/me`)
            if (response.status === 200) {
                setIsAuth(true)
                setUserInfo(response.data)
            }
        } catch (error) {
            setIsAuth(false)
        }
    }

    /*
    * Empty the list of planets
    * */
    const setPlanetListToDefault = async () => {
        setPlanetList([])
    }

    const getAllPlanets = async () => {
        /*retrieve a list of planet id's and planet names to switch between them*/
        try {
            /*Make sure the user sees the right planets*/
            const response2 = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/spawn`)

            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/planets/private`)
            if (response.data.length > 0){
                setPlanetList(response.data);
            }else await setPlanetListToDefault()

            changePlanetId(response2.data.planet_id);

        } catch (error) {
            await setPlanetListToDefault()
        }
    }

    /*
    * Update the planet that we are currently looking at
    * */
    const changePlanetId = (planetId) => {
        const newIndex = planetList.findIndex(planet => planet.id === planetId);
        if (newIndex !== -1) {
            setPlanetListIndex(newIndex);
        } else {
            console.error("Planet with the given ID not found.");
        }
    };


    /*
    * When opening the game, start to authenticate the user
    * And loading all the planets
    * */
    useEffect(() => {
        authenticate()
        getAllPlanets()

    }, [])

    /*
    * Support maintenance using a custom hook
    * */

    MaintenanceHook()


    return (
        <ColorManager>
        <UserInfoContext.Provider value={[userInfo, setUserInfo]}>
        <ViewModeContext.Provider value={[viewMode, setViewMode]}>
        <PlanetListContext.Provider value={[planetList, setPlanetList]}>

            {userInfo && <Suspense fallback={<h1>Loading...</h1>}>
                <UI/>

                {combatNotifications.map((el) => <Notification won={el.won}
                                                               own_target={el.own_target}
                                                               other_target={el.other_target}/>)}


                {/*Display a planet map*/}
                {viewMode === View.PlanetView && planetList[planetListIndex] !== undefined &&
                    <div>
                        <div onClick={() => setViewMode(View.GalaxyView)}
                             className="fixed text-5xl z-10 transition ease-in-out hover:scale-150 hover:translate-x-5 hover:translate-y-1 duration-300 flex">
                            <RiArrowLeftSLine className="basis-1/4"/>
                            <IoMdPlanet/>
                        </div>
                        <PlanetViewer key={planetList[planetListIndex].id}
                                      planetName={planetList[planetListIndex].name}
                                      planetId={planetList[planetListIndex].id}
                                      planetListIndex={[planetListIndex, setPlanetListIndex]}/>
                    </div>
                }

                {/*Display the galaxy map*/}
                {viewMode === View.GalaxyView &&
                    <GalaxyViewer setViewMode={setViewMode} planetListIndex={[planetListIndex, setPlanetListIndex]} changePlanetId={changePlanetId}/>
                }

                {/*Display the profile menu*/}
                {viewMode === View.ProfileView &&
                    <ProfileViewer changePlanetByID={changePlanetId}/>
                }

            </Suspense>
            }

            {/*When a user is not authenticated, we will inform the user of that*/}
            {!userInfo && !isAuth && <h1>Not authenticated</h1>}

        </PlanetListContext.Provider>
        </ViewModeContext.Provider>
        </UserInfoContext.Provider>
        </ColorManager>)
}
export default Game