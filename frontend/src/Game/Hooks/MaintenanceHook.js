import {useEffect, useRef, useState} from 'react';
import {initializeResources} from "../UI/ResourceViewer/ResourceViewer";
import {useDispatch, useSelector} from "react-redux";
import {setDecreaseResource} from "../../redux/slices/resourcesSlice";

const MaintenanceHook = () => {
    /**
    * This hook handles the maintenance costs, and visually reducing it from the user its account.
    * Maintenance cost are costs the user need to maintain its cities and armies. This being an IDLE mechanic,
    * we cannot constantly sync each second with the backend. That is why based on the maintenance cost,
    * we will mimic the resources updates on the frontend
    * This hook makes sure, the resources are properly updated based on the maintenance cost
    * */
    const dispatch = useDispatch()
    const resources = useSelector((state) => state.resources.resources)

    /*
    * Use a websocket to realtime update information about the maintenance of an army
    * */
    const [maintenanceWebsocket, setMaintenanceWebsocket] = useState(null);

    /*
    * Tracks whether the websocket has been established
    * */
    const isConnected = useRef(false);

    /*
    * To be able to simulate the change of maintenance live, will retrieve the maintenance rate and
    * mimic this on the frontend
    * */
    const [maintenanceCost, setMaintenanceCost] = useState({});
    const [maintenanceCheckable, setMaintenanceCheckable] = useState(false);
    useEffect(() => {
        if (isConnected.current) return

        isConnected.current = true;

        /*
        * establish the maintenance websocket
        * */
        const webSocket = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/logic/maintenance`,
            `${localStorage.getItem('access-token')}`);
        setMaintenanceWebsocket(webSocket);

        /*
        * Send a request to access the maintenance cost
        * */
        webSocket.onopen = () => {
            webSocket.send(
                JSON.stringify(
                    {
                        type: "get_maintenance_cost",
            }))
        }

        /*
        * Update current resources amount
        * */
        initializeResources(dispatch)

    }, []);

    /*
    * make sure we wait a given time before being able to check the maintenance (to prevent high traffic usage)
    * */
    const checkable_maintenance = async(delay) => {
        /*
        * Set the maintenance to not checkable, till after the timeout
        * */
        setMaintenanceCheckable(false)
        await new Promise((resolve) => setTimeout(resolve, delay*1000))
        setMaintenanceCheckable(true)
    }


    /*
    * Handle maintenance websocket actions
    * */
    useEffect(() => {
        if (!maintenanceWebsocket) return;

        if (!isConnected.current) return

        maintenanceWebsocket.onmessage = (event) => {
            let data = JSON.parse(event.data)
            if (data.type === "update_cost") {
                /*
                * When we get an update_cost action, we will update the websocket costs
                * Resync the resources, and handle the maintenance checkable
                * */

                setMaintenanceCost(data.maintenance_cost)
                initializeResources(dispatch)

                checkable_maintenance(data.checkin)

            }

        };

        return () => {
            maintenanceWebsocket.close();
        };

    }, [maintenanceWebsocket]);

    /*Check if resources <= 0, if so calibrate with backend*/
    useEffect(() => {
        /*
        * prevent checking when not check-able, this useEffect is triggered, after every change of the resources,
        * so we can check when we ran out of a needed resource
        * */
        if (!maintenanceCheckable){return}
        Object.entries(resources).forEach((resource) => {
            if (maintenanceCost[resource[0]] === undefined){return}

            /*
            * Check if resource == 0
            * */
            if (resource[1] <= 0){

                /*
                * Send a new check request
                * */
                const sendCheck = async() => {
                    maintenanceWebsocket.send(
                    JSON.stringify(
                        {
                            type: "get_maintenance_cost",
                    }))
                }

                sendCheck()
            }

        })
    }, [resources])

    /*
    * Visually mimic the resource reduction, so the client has the feeling the resources are updated live
    * */
    useEffect(() => {
        /*
        * For each maintenance cost resource, we will set an interval in which we reduce the resource by 1
        * */
        let intervals = []
        Object.entries(maintenanceCost).forEach((element) => {
            /*
            * Only make intervals for resources that have a cost > 0/h
            * */
            if (element[1] !== 0){
                const makeInterval = async() => {
                    /*
                    * Wait a short amount of time before starting the interval, the reason for this is rounding.
                    * Resources are not stored as real numbers, so in the backend some rounding occurs.
                    * Frontend cannot be aware of this rounding, but using this delay the user will not be aware of
                    * such rounding occurring.
                    * */
                    await new Promise((resolve) => setTimeout(resolve, 2*Math.floor(1000*3600/element[1])))

                    /*
                    * To avoid cpu intensiveness, we will maximally update the maintenance of each
                    * resource every second
                    * */
                    let interval_change = 1;
                    let interval_duration = 1000*3600/element[1];
                    if (interval_duration < 1000){
                        const d = Math.ceil(1000/interval_duration)
                        interval_duration *= d;
                        interval_change *= d;
                    }

                    /*
                    * Create the interval to slowly decrease the resource amount of the user
                    * */
                    const interval = setInterval(() => {
                        dispatch(setDecreaseResource({"resource": element[0], "amount": interval_change}))
                    }, Math.floor(interval_duration))
                    intervals.push(interval)
                }
                makeInterval()

            }

        });

        /*
        * When the maintenance cost changes, we will also clear the intervals
        * */
        return () => {
            intervals.forEach((interval) => {
                clearInterval(interval)
            })
            intervals = []

        };

    }, [maintenanceCost]);

};

export default MaintenanceHook;