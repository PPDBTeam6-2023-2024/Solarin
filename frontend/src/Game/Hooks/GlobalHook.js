import {useEffect, useRef} from 'react';
import {useNavigate} from "react-router-dom";
import Notification from "../UI/CombatNotifications/Notification";
import DefaultNotification from "../UI/CombatNotifications/DefaultNotification";

const GlobalHook = (setNotifications, setUserInfo) => {
    /**
    * This hook handles the global websocket, and its actions (like letting the user know he/ she is game over)
    */

    /*
    * Reference to websocket
    * */
    const ws = useRef(null)

    /*
    * Way to navigate to other pages
    * */
    const navigate = useNavigate()

    /*
    * For combat we have a list of notifications,
    * but after 5 seconds we want our pop-up notifications to disappear
    * */
    const remove_notification = async(notification) => {
        await new Promise((resolve) => setTimeout(resolve, 5000))
        setNotifications(notif => notif.filter(item => item !== notification))
    }

    /*
    * Effect to handle the websocket
    * */
    useEffect(() => {
        ws.current = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/globalws/ws`, `${localStorage.getItem('access-token')}`);

        ws.current.onopen = function (event) {
            console.log('WebSocket is open now.');
        };

        ws.current.onmessage = function (event) {
            const data = JSON.parse(event.data)
            /*
            * When the user receives a death message, it means that the user has nothing left and
            * needs to be rerouted to the restart menu
            * */
            if (data.type === 'death') {
                navigate('/game-over')
            }

            /*Display a combat notification*/
            if (data.type === "combat_notification"){
                const not = (<Notification won={data.won}
                   own_target={data.own_target}
                   other_target={data.other_target}/>)

                setNotifications(notif => [...notif, not])
                remove_notification(not)
            }

            if (data.type === "city_to_close"){
                const not = (<DefaultNotification text={"City cannot be created because other city to close"}/>)

                setNotifications(notif => [...notif, not])
                remove_notification(not)
            }


            if (data.type === 'alliance') {
                setUserInfo(Info => {return {...Info, alliance: data.value}})
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





};

export default GlobalHook;