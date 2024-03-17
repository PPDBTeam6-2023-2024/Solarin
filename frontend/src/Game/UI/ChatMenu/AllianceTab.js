import React, {useEffect, useState} from "react";
import FriendOverviewEntry from "./Friends/FriendOverviewEntry";
import MessageBoard from "./MessageBoard";
import axios from "axios";
import FriendRequestEntry from "./Friends/FriendRequestEntry";

const AllianceTab = (props) => {
    const [chatOpen, setChatOpen] = useState(false)
    const [allianceRequests, setAllianceRequests] = useState([])
    return (
        <>
            {!chatOpen &&
                <div style={{"overflow-y": "scroll", "height":"85%", "scrollbar-width:": "none"}}>
                    {
                    /*display all friend requests*/
                    allianceRequests.map((elem, index) => <FriendRequestEntry user={elem[0]} user_id={elem[1]} key={index}
                                                                            onEntryChose={
                        () => setAllianceRequests(allianceRequests.slice(0 , index).concat(allianceRequests.slice(index+1)))
                    }/>)
                    }
                </div>

            }
        </>



    )
}

export default AllianceTab;