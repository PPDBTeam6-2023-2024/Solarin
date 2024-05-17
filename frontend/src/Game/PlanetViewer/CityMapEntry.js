import {useContext, useEffect} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";
import { GiSkullCrossedBones } from "react-icons/gi";
import "./CityMapEntry.css"
import { IoMdFlag } from "react-icons/io";

function CityMapEntry(props) {
    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const isOwner = +(userInfo.id === props.city.controlled_by);
    const isAllied = userInfo.alliance && props.city.alliance === userInfo.alliance
    const cityType = (!isAllied && !isOwner) ? "enemy" : (isOwner) ? "own" : "ally"

    let cursorStyleClass = "CityMapEntryPointer";

    if (props.decide_moving){
        if (!isOwner){
            // Display the attack cursor, when hovering on an enemy city when in decide moving mode
            cursorStyleClass = 'CityMapEntryEnemy'
        }else{
            cursorStyleClass = 'CityMapEntryEnter'
        }
    }
    const cityOnClick = (e) => {
        props.onClick(e, {
            on_arrive: true,
            target_type: (isOwner) ? "enter" : "attack_city",
            target_id: props.city.id
        })
    }
    return (
        <div className={`${cursorStyleClass}`} onClick={cityOnClick}>
            <div className="z-20 absolute opacity-80 pointer-events-none"
                 style={{transform: 'translate(-50%, -50%)',
                     left: `${props.city.x * 100}%`, top: `${props.city.y * 100}%`}}>
            { cityType === "enemy" &&
                <GiSkullCrossedBones className={"bg-red-800 p-2 text-5xl rounded-3xl border border-white"}/>
            }
            { cityType === "ally" &&
                <IoMdFlag className={"bg-blue-800 p-2 text-5xl border border-white rounded-3xl"}/>
            }
            </div>
            <img  key={props.index} src={props.city.src} alt="city" style={props.city.style}/>
        </div>
    )
}
export default CityMapEntry