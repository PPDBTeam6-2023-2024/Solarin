import {useContext, useState} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";

import "./ArmyMapEntry.css"

function ArmyMapEntry(props) {

    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const is_owner = +(userInfo.id === props.army.owner);

    let cursor_style_class = "ArmyMapEntryPointer";

    if (props.decide_moving && !props.moving_Selected){
        if (!is_owner){
            // Display the attack cursor, when hovering on an enemy army when in decide moving mode
            cursor_style_class = 'ArmyMapEntryEnemy'
        }else{
            cursor_style_class = 'ArmyMapEntryMerge'
        }
    }

    return (
        <img key={props.index} src={props.army.src} alt="army" className={`${cursor_style_class} transition-all ease-linear`}
             style={{...props.army.style, left: `${props.army.curr_x * 100}%`, top: `${props.army.curr_y * 100}%`}}
                         onClick={props.onClick} {...{ "test": "1" }} index={props.army.id} image_type={"army"} is_owner={is_owner}/>


    )
}
export default ArmyMapEntry