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
import { useNavigate } from "react-router-dom"

import {PlanetListContext} from "./Context/PlanetListContext"
import {useSelector, useDispatch} from 'react-redux'
import {setResource, setDecreaseResource} from "../redux/slices/resourcesSlice";
import {initializeResources} from "./UI/ResourceViewer/ResourceViewer"
import {PrimaryContext, SecondaryContext, TertiaryContext, TextColorContext} from "./Context/ThemeContext";
import Notification from "./UI/CombatNotifications/Notification";
import MaintenanceHook from "./Hooks/MaintenanceHook";
const Game = () => {
    /**
     * these 2 states exist to be able to change the UI colors
     * */
    const [primaryColor, setPrimaryColor] = useState("#c88018")
    const [secondaryColor, setSecondaryColor] = useState("#c53520")
    const [tertiaryColor, setTertiaryColor] = useState("#fbfbfb")
    const [textColor, setTextColor] = useState("#ffffff")

    const [isAuth, setIsAuth] = useState(false)
    const [userInfo, setUserInfo] = useState(null)
    const [viewMode, setViewMode] = useState(View.PlanetView)
    const [planetList, setPlanetList] = useState([{"id": 1, "name": "Terra"}])
    const [planetListIndex, setPlanetListIndex] = useState(0)
    const ws = useRef(null)
    const navigate = useNavigate()

    MaintenanceHook()


    useEffect(() => {
        const getColors = async() => {
            axios.defaults.headers.common = await {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/logic/colors`)
            if (response.data === null){return}
            setPrimaryColor(response.data.primary_color);
            setSecondaryColor(response.data.secondary_color);
            setTertiaryColor(response.data.tertiary_color);
            setTextColor(response.data.text_color);
        }

        getColors();
    }, []);



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
        setPlanetList([{"id": 1, "name": "Terra"}])
    }

    const getAllPlanets = async () => {
        /*retrieve a list of planet id's and planet names to switch between them*/
        try {
            /*Make sure the user sees the right planets*/
            const response2 = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/spawn`)

            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/planets/private`)
            if (response.data.length > 0) setPlanetList(response.data)
            else await setPlanetListToDefault()

            changePlanetId(response2.data.planet_id);

        } catch (error) {
            await setPlanetListToDefault()
        }
    }

    const changePlanetId = (planetId) => {
        const newIndex = planetList.findIndex(planet => planet.id === planetId);
        if (newIndex !== -1) {
            setPlanetListIndex(newIndex);
        } else {
            console.error("Planet with the given ID not found.");
        }
    };

    /*
    * Store a list of current pop-up notifications
    * */
    const [combatNotifications, setCombatNotifications] = useState([]);
    const remove_notification = async(notification) => {
        await new Promise((resolve) => setTimeout(resolve, 5000))
        setCombatNotifications(notif => notif.filter(item => item !== notification))
    }

    useEffect(() => {
        ws.current = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/globalws/ws`, `${localStorage.getItem('access-token')}`);

        ws.current.onopen = function (event) {
            console.log('WebSocket is open now.');
        };

        ws.current.onmessage = function (event) {
            const data = JSON.parse(event.data)
            if (data.type === 'death') {
                navigate('/game-over')
            }

            /*Display a combat notification*/
            if (data.type === "combat_notification"){
                setCombatNotifications(notif => [...notif, data])
                remove_notification(data)
            }
        };

        ws.current.onclose = function (event) {
            console.log('WebSocket is closed now.');
        };

        ws.current.onerror = function (event) {
            console.error('WebSocket error observed:', event);
        };

        return () => {
            ws.current.close();
        };
    }, []);

    useEffect(() => {
        authenticate()
        getAllPlanets()
    }, [])


    return (<div className="h-screen bg-gray-900"
            style={{
                '--primaryColor': primaryColor,
                '--secundaryColor': secondaryColor,
                "--tertiaryColor": tertiaryColor,
                "--textColor": textColor,
            }}
    >
        <UserInfoContext.Provider value={[userInfo, setUserInfo]}>
            <ViewModeContext.Provider value={[viewMode, setViewMode]}>
                <PrimaryContext.Provider value={[primaryColor, setPrimaryColor]}>
                <SecondaryContext.Provider value={[secondaryColor, setSecondaryColor]}>
                <TertiaryContext.Provider value={[tertiaryColor, setTertiaryColor]}>
                <TextColorContext.Provider value={[textColor, setTextColor]}>
                <PlanetListContext.Provider value={[planetList, setPlanetList]}>

                    {userInfo && <Suspense fallback={<h1>Loading...</h1>}>
                        <UI/>

                        {combatNotifications.map((el) => <Notification won={el.won}
                                                                       own_target={el.own_target}
                                                                       other_target={el.other_target}/>)}


                        {viewMode === View.PlanetView &&
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

                        {viewMode === View.GalaxyView &&
                            <GalaxyViewer setViewMode={setViewMode} planetListIndex={[planetListIndex, setPlanetListIndex]} changePlanetId={changePlanetId}/>
                        }

                        {viewMode === View.ProfileView &&
                            <ProfileViewer changePlanetByID={changePlanetId}/>
                        }

                    </Suspense>
                    }


                    {!userInfo && !isAuth && <h1>Not authenticated</h1>}

                </PlanetListContext.Provider>
                </TextColorContext.Provider>
                </TertiaryContext.Provider>
                </SecondaryContext.Provider>
                </PrimaryContext.Provider>

            </ViewModeContext.Provider>
        </UserInfoContext.Provider>
    </div>)
}
export default Game