import {useContext} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";

import "./ArmyMapEntry.css"

function ArmyMapEntry(props) {

    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const isOwner = +(userInfo.id === props.army.owner);

    let cursorStyleClass = "ArmyMapEntryPointer";

    if (props.decide_moving && !props.moving_Selected){
        if (!isOwner){
            // Display the attack cursor, when hovering on an enemy army when in decide moving mode
            cursorStyleClass = 'ArmyMapEntryEnemy'
        }else{
            cursorStyleClass = 'ArmyMapEntryMerge'
        }
    }

    return (
        <img key={props.index} src={props.army.src} alt="army" className={`${cursorStyleClass} transition-all ease-linear`}
             style={{...props.army.style, left: `${props.army.curr_x * 100}%`, top: `${props.army.curr_y * 100}%`}}
                         onClick={props.onClick} {...{ "test": "1" }} index={props.army.id} image_type={"army"} is_owner={isOwner}/>


    )
}
export default ArmyMapEntry