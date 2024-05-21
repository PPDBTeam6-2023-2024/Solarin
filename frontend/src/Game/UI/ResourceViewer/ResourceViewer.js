import resourcesJson from "./resources.json"
import {useMemo, useState, useEffect} from "react";
import Tooltip from '@mui/material/Tooltip';
import {IoMdClose} from "react-icons/io";
import WindowUI from "../WindowUI/WindowUI";
import axios from 'axios'
import {useDispatch, useSelector} from 'react-redux'
import {setResources} from "../../../redux/slices/resourcesSlice";


export const initializeResources = async (dispatch) => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`,
         'content-type': 'application/x-www-form-urlencoded',
         'accept': 'application/json', "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/logic/resources`);
        if (response.status === 200) {
            dispatch(setResources(response.data))
        }
    } catch (error) {
        console.error("Failed to fetch resources", error);
    }
}

export const Resources = () => {
    const resourcesInfo = useMemo(() => resourcesJson)
    const dispatch = useDispatch()
    const resources = useSelector((state) => state.resources.resources)

    const getResourceField = (resource, field, altValue) => {
        if (resourcesInfo[resource] && resourcesInfo[resource][field]) return resourcesInfo[resource][field]
        return altValue
    }
    useEffect(() => {
        initializeResources(dispatch)
    }, [])
    return (
        <>

            {Object.entries(resources).map((resource) =>
                <Tooltip key={resource} title={getResourceField(resource[0], "description", "")}>
                    <div className="mr-3 p-1 max-h-9 shrink-0 relative">
                        <p><span style={{"fontSize": "1.4vw"}}>{resource[1]}</span>
                            {getResourceField(resource[0], "icon", null) &&
                                <img className="inline ml-2 max-w-10 max-h-10 w-auto h-auto"
                                     src={(`/images/resources/${getResourceField(resource[0], "icon", "")}`)}
                                     alt={resource[0]} draggable={false}/>
                            }
                            {
                                getResourceField(resource[0], "icon", null) === null &&
                                resource[0]
                            }
                        </p>
                    </div>
                </Tooltip>)}
        </>
    )
}


export default function ResourceViewer(props) {
    const {title = "Resources", className} = props
    const [hideButton, setHideButton] = useState(false)
    return (
        <WindowUI hideState={hideButton} windowName="Resource Viewer">
            <div className={className}>
                <div className="bg-gray-800 p-3 border-2 border-white">
                    <IoMdClose onClick={() => setHideButton(!hideButton)}/>
                    {title && <><h1>{title}</h1>
                        <hr className="my-2"/>
                    </>}
                    <div className="flex justify-center items-center text-center">
                        <Resources/>
                    </div>
                </div>
            </div>
        </WindowUI>
    )
}
