import {useContext} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";
import { GiSkullCrossedBones } from "react-icons/gi";
import "./CityMapEntry.css"
import { IoMdFlag } from "react-icons/io";

function CityMapEntry(props) {
    /**
     * This component visualizes the city on the planet map
     * */
    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const isOwner = +(userInfo.id === props.city.controlled_by);
    const isAllied = userInfo.alliance && props.city.alliance === userInfo.alliance
    const cityType = (!isAllied && !isOwner) ? "enemy" : (isOwner) ? "own" : "ally"

    /*
    * Depending on the relation of the user with the city, the cursor icon will change, while being in move select
    * mode with a selected army
    * */
    let cursorStyleClass = "CityMapEntryPointer";
    if (props.decide_moving){
        if (!isOwner){
            /*Display the attack cursor, when hovering on an enemy city when in decide moving mode*/
            cursorStyleClass = 'CityMapEntryEnemy'
        }else{
            /*Display the enter cursor, when hovering on an enemy city when in decide moving mode*/
            cursorStyleClass = 'CityMapEntryEnter'
        }
    }
    const cityOnClick = (e) => {
        /*
        * We will let the backend know what we want to do when we arrive at the destination (enter/attack with the army)
        * Using this function, we will make the proper request format
        * */
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
            {/*In case the city belongs to an ally/enemy, we will display an additional texture to indicate this*/}
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