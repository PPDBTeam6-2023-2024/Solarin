import React, {useEffect, useState} from "react";
import FriendOverviewEntry from "./Friends/FriendOverviewEntry";
import MessageBoard from "./MessageBoard";
import axios from "axios";
import FriendRequestEntry from "./Friends/FriendRequestEntry";
const getDMOverview = async() => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/chat/dm_overview`)
        return response.data
    }
    catch(e) {return []}
}

const getFriendRequests = async() => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/chat/friend_requests`)
        return response.data
    }
    catch(e) {return []}
}


const DmTab = (props) => {
    const [friendRequests, setFriendRequests] = useState([])
    const [dmData, setDmData] = useState([])
    const [dmIndex, setDmIndex] = useState(-1)

    //syntax is not great, but apparently the proper way to retrieve async information from a sync function
    //This function reads the data from the RESTAPI request, and will use its data to amek  the DMOverview


    useEffect(() => {
        async function makeOverviewEntries() {
            let data = await getDMOverview()
            setDmData(data)

            data = await getFriendRequests()
            setFriendRequests(data)
        }
        makeOverviewEntries()
    }, [])


    return (
        <>
            {dmIndex === -1 && <div style={{"overflow-y": "scroll", "height":"85%", "scrollbar-width:": "none"}}>
                    {
                    /*display all friend requests*/
                    friendRequests.map((elem, index) => <FriendRequestEntry user={elem[0]} user_id={elem[1]} key={index}
                                                                            onEntryChose={
                        () => setFriendRequests(friendRequests.slice(0 , index).concat(friendRequests.slice(index+1)))
                    }/>)
                    }
                    {
                    /*display all the friend overview entries we just retrieved*/
                    dmData.map((elem, index) => <FriendOverviewEntry user={elem[0]} message={elem[1]} key={index} onEntryClick={() => setDmIndex(index)}></FriendOverviewEntry>)
                    }


            </div>}
            {/*Open a component for the dm between the 2 users that were just selected*/}
            {dmIndex !== -1 && <MessageBoard message_board={dmData.slice(dmIndex , dmIndex+1)[0][2]}/>}
        </>


    )
}

export default DmTab;