import React, {useContext, useEffect, useState} from "react";
import MessageBoard from "../MessageBoard";
import axios from "axios";
import AllianceRequestEntry from "./AllianceRequestEntry";
import {UserInfoContext} from "../../../Context/UserInfoContext"
import "./AllianceTab.css"
import "../Requests/RequestButtons.css"
import AllianceMemberEntry from "./AllianceMemberEntry";


const AllianceTab = (props) => {
    const [chatOpen, setChatOpen] = useState(false)
    const [allianceRequests, setAllianceRequests] = useState([])

    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    /*In case the user is not in a faction it receives an input area to enter a Alliance name of a faction it wants to join/create*/
    const [pendingName, setPendingName] = useState("");

    /*error message in regard to errors for creating/joining an alliance*/
    const [anwserMessage, setAnwserMessage] = useState("");

    /*store the message board number*/
    const [messageBoard, setMessageBoard] = useState(-1);

    /*store the message board number*/
    const [allianceMembers, setAllianceMembers] = useState([]);

    const sendLeaveUser = async (user_id) => {
        /*
        * when we accept or reject an alliance join request we need to communicate that to the backend
        * */
        try {
            await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/chat/kick_user`,
                JSON.stringify({
                    "user_id": user_id
                }),
                {
                    headers: {
                        'content-type': 'application/json',
                        'accept': 'application/json',
                    },
                }
            )

        } catch (e) {
        }

    }


    /*
    * This function will create/try to join an alliance
    * */
    const DoAlliance = async (alliance_name, create) => {
        /*
        * change the endpoint depending on if we want to create or join an alliance.
        * */
        let end_point = "join";
        if (create) {
            end_point = "create"
        }

        try {
            /*send a post request to try and create or join the alliance*/
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/chat/${end_point}_alliance`,
                JSON.stringify({
                    "alliance_name": alliance_name
                }),
                {
                    headers: {
                        'content-type': 'application/json',
                        'accept': 'application/json',
                    },
                }
            )

            let data = response.data;

            /**
             * if alliance is created make sure locally the user is also aware of this alliance in frontend
             * */
            if (data.success === true) {
                const newUserInfo = {...userInfo, alliance: alliance_name};
                setUserInfo(newUserInfo);
            } else {
                setAnwserMessage(data.message);
            }

        } catch (e) {
        }
    }

    const getAllianceRequests = async () => {
        /*get the list of all the requests to join the alliance*/
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/chat/alliance_requests`)
            return response.data
        } catch (e) {
            return []
        }
    }

    const getMessageBoard = async () => {
        /*get messageboard for the alliance, because we do not yet have that*/
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/chat/alliance_messageboard`)
            return response.data
        } catch (e) {
            return -1
        }
    }

    const getAllianceMembers = async () => {
        /*get all members that are part of the alliance*/
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/chat/get_alliance_members`)
            return response.data
        } catch (e) {
            return -1
        }
    }

    useEffect(() => {
        async function makeOverviewEntries() {
            let data = await getAllianceRequests()
            setAllianceRequests(data)

            if (userInfo.alliance !== null) {
                data = await getMessageBoard()
                setMessageBoard(data)

                data = await getAllianceMembers()
                setAllianceMembers(data)
            }
        }

        makeOverviewEntries()
    }, [userInfo.alliance])
    return (
        <>
            {/*when the chat is not yet open*/}
            {!chatOpen &&
                <div id={"AllianceTab"} style={{"height": "93%"}}>
                    {!userInfo.alliance &&
                        <>
                            Enter Alliance Name:
                            <input name="alliance_name" value={pendingName}
                                   onChange={(event) => {
                                       setPendingName(event.target.value)
                                   }}
                                   className="bg-gray-900" required/>
                            {anwserMessage}
                            <button className="RequestButton" onClick={() => DoAlliance(pendingName, true)}> Create
                                Alliance
                            </button>
                            <button className="RequestButton" onClick={() => DoAlliance(pendingName, false)}> Join
                                Alliance
                            </button>
                        </>

                    }

                    {userInfo.alliance &&
                        <>
                            {/*this part gives an overview of the alliance, when the user is part of an alliance*/}

                            {/*visualize all alliance join requests*/}
                            <div style={{"overflowY": "scroll", "height": "85%", "scrollbarWidth:": "none"}}>
                                {
                                /*display all friend requests*/
                                allianceRequests.map((elem, index) =>
                                    <AllianceRequestEntry user={elem[0]}
                                    user_id={elem[1]}
                                    key={index}
                                    onEntryChose={
                                        () => setAllianceRequests(allianceRequests.slice(0, index).concat(allianceRequests.slice(index + 1)))
                                    }/>)
                                }
                                {
                                /*display all friend requests*/
                                allianceMembers.map((elem, index) =>
                                    <AllianceMemberEntry user={elem.name}
                                    user_id={elem.id}
                                    key={index}
                                    onEntryChose={
                                        () => setAllianceMembers(allianceMembers.slice(0, index).concat(allianceMembers.slice(index + 1)))
                                    }/>)
                                }



                            </div>
                            {/*Display the leave button*/}
                            <button className="RequestButton" onClick={() => {
                                sendLeaveUser(userInfo.id);
                                const newUserInfo = {...userInfo, alliance: null};
                                setUserInfo(newUserInfo);
                            }}> Leave Alliance
                            </button>

                            {/*button to open the alliance chat*/}
                            <button className="RequestButton" onClick={() => {
                                setChatOpen(true);
                            }}> Open Chat
                            </button>
                        </>

                    }
                </div>
            }

            {/*Display the chat of the alliance*/}
            {chatOpen && <MessageBoard message_board={messageBoard}/>}

        </>


    )
}

export default AllianceTab;