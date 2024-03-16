import React, {useEffect, useRef, useState} from "react";
import Draggable from "react-draggable";
import "./Friends/FriendOverviewEntry.css"
import axios from "axios";
import {json} from "react-router-dom";
import Message from "./Message";
import SendMessage from "./SendMessage";

function MessageBoard(props) {
    /**
     * This shows the message stream of a message board
     * */

    const [socket, setSocket] = useState(null);
    const [messageList, setMessageList] = useState([]);


    /**
    * makes sure that UseEffect for connecting to the websocket is not called twice
     * in react strict mode
    * */
    const is_connected = useRef(false);

   useEffect(() => {
       if (is_connected.current) return

       is_connected.current = true;

       console.log("messageboard", props.message_board)
       const web_socket = new WebSocket(`ws://${"localhost:8000"}/chat/dm/${props.message_board}`, `${localStorage.getItem('access-token')}`);
        setSocket(web_socket);
    }, []);

    useEffect(() => {
        if (!socket) return;

        socket.onmessage = function (event) {
            let data = JSON.parse(event.data)
            if (data.type === "paging"){
                setMessageList(messageList => data.message.concat(messageList));

            }
            if (data.type === "new message"){
                messageList.push(...data.message);

                setMessageList(messageList => messageList.concat(data.message));
            }

        };


        return () => {
            socket.close();
        };
    }, [socket]);

    return (
      <>
          {/*Display the messages*/}
          <div style={{"overflow-y": "scroll", "height":"80%", "scrollbar-width:": "none", "borderBottom":"0.3vw solid var(--tertiaryColor)"}}>
              {messageList.map((d, index) => <Message key={index} message={d}/>)}
          </div>

          <SendMessage socket={socket}/>
      </>
    )
}

export default MessageBoard