import Draggable from "react-draggable"
import resourcesJson from "./resources.json"
import { useMemo } from "react";
import Tooltip from '@mui/material/Tooltip';

const getResourceStats = (resources, resourcesInfo) => {
    const elements = []
    for (let resource in resources){
        const scale = resourcesInfo[resource].scale || 1;
        const imageSize = { width: `${scale * 24}px`, height: `${scale * 24}px` };

        elements.push(
            <Tooltip key={resource} title={resourcesInfo[resource]["description"]}>
            <div className="mr-3 bg-gradient-to-r from-gray-600 to-gray-700 p-1">
            <p>{resources[resource]["collected"]}
            <img className="inline ml-2" src={(`/images/resources/${resourcesInfo[resource]["icon"]}`)} style={imageSize} alt={resource} draggable={false}/>
            </p>
            {resources[resource]["producing"] && <p className="text-xs">{resources[resource]["producing"]}/hr</p>}
            </div>
            </Tooltip>
        )
    }
    return (<>
        {elements}
    </>
    )
}



function ResourceViewer(props) {
    const {title, resources, draggable, className} = props
    const resourcesInfo = useMemo(() => resourcesJson)
    const content = 
    <div className={className}>
        <div className="bg-gray-800 p-3 border-2 border-white">
            {title && <><h1>{title}</h1><hr className="my-2"/></>}
            <div className="flex justify-center items-center text-center">
            {getResourceStats(resources, resourcesInfo)}
            </div>
        </div>
    </div>
    return (
        <>
        {
            draggable && <Draggable>{content}</Draggable>
        }
        {
            !draggable && <>{content}</>
        }
        </>
    )
}
export default ResourceViewer