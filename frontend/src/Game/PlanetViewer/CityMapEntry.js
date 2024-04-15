import {useContext, useEffect} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";
import "./CityMapEntry.css"

function CityMapEntry(props) {
    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const isOwner = +(userInfo.id === props.city.controlled_by);

     let cursorStyleClass = "CityMapEntryPointer";

    if (props.decide_moving){
        if (!isOwner){
            // Display the attack cursor, when hovering on an enemy city when in decide moving mode
            cursorStyleClass = 'CityMapEntryEnemy'
        }else{
            cursorStyleClass = 'CityMapEntryEnter'
        }
    }


    return (
        <img className={`${cursorStyleClass}`} key={props.index} src={props.city.src} alt="city" style={props.city.style} onClick={props.onClick} index={props.city.id} image_type={"city"} is_owner={isOwner}/>
    )
}
export default CityMapEntry