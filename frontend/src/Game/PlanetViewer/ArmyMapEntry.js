import {useContext, useEffect} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";
import generalsInfo from '../UI/ArmyViewer/generals.json'
import { FaSkull, FaFlag } from "react-icons/fa"
import { RxSewingPinFilled } from "react-icons/rx";


import "./ArmyMapEntry.css"

function ArmyMapEntry(props) {
    /**
     * This component visualizes an army on the planet map
     * */

    /*
    * Retrieve user information
    * */
    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    /*
    * indicates whether the user is the owner of the army or not
    * */
    const isOwner = +(userInfo.id === props.army.owner)

    /*
    * indicates if the user is in the same alliance as the army
    * */
    const isAllied = userInfo.alliance && props.army.alliance === userInfo.alliance

    /*
    * Depending on the relation of the user with the army, the cursor icon will change, while being in move select
    * mode
    * */
    let cursorStyleClass = "ArmyMapEntryPointer";
    const armyType = (!isAllied && !isOwner) ? "enemy" : (isOwner) ? "own" : "ally"
    if (props.decide_moving && !props.moving_Selected){
        if (armyType === "enemy"){
            /*Display the attack cursor, when hovering on an enemy army when in decide moving mode*/
            cursorStyleClass = 'ArmyMapEntryEnemy'
        } else if(armyType === "own") {
            /*Display the merge cursor, when hovering on an enemy army when in decide moving mode*/
            cursorStyleClass = 'ArmyMapEntryMerge'
        }
    }
    const armyOnClick = (e) => {
        /*
        * We will let the backend know what we want to do when we arrive at the destination (merge/attack with the army)
        * Using this function, we will make the proper request format
        * */
        if(armyType !== "ally") {
            props.onClick(e, {
                on_arrive: true,
                target_type: (isOwner) ? "merge" : "attack_army",
                target_id: props.army.id
            })
        }
        else props.onClick(e)
    }
    return (
        <div className={`${cursorStyleClass} transition-all text-center ease-linear`}
             onClick={armyOnClick}
             style={{
                 ...props.army.style,
                 left: `${props.army.curr_x * 100}%`,
                 top: `${props.army.curr_y * 100}%`,
                 zIndex: 50,
             }}>
            {/*The visualization depends on the relation between the user and the army (own, ally, enemy)*/}
            {
                armyType === "enemy" &&
                <FaSkull className={"inline bg-red-900 m-auto text-5xl rounded-xl p-2"}/>
            }
            {
                armyType === "own" &&
                <div className={"inline bg-blue-400 text-4xl rounded-xl px-2 m-auto"}>{props.army.id}</div>
            }
            {
                armyType === "ally" &&
                <FaFlag className={"inline bg-blue-900 m-auto text-5xl rounded-xl p-2"}/>
            }
            <RxSewingPinFilled className={"text-center m-auto"}/>
            <h1 className={"mt-1"}>{props.army.username}{(isOwner ? "(You)" : "")}</h1>
        </div>
    )
}

export default ArmyMapEntry