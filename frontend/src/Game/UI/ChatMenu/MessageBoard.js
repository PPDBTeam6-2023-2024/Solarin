import React, {useEffect, useRef, useState} from "react";
import Draggable from "react-draggable";
import "./Friends/FriendOverviewEntry.css"
import axios from "axios";
import {json} from "react-router-dom";
import Message from "./Message";
import SendMessage from "./SendMessage";
import { Component } from 'react';

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

       const web_socket = new WebSocket(`ws://${"localhost:8000"}/chat/dm/${props.message_board}`, `${localStorage.getItem('access-token')}`);
        setSocket(web_socket);
    }, []);

    useEffect(() => {
        if (!socket) return;

        socket.onmessage = function (event) {
            let data = JSON.parse(event.data)
            if (data.type === "paging"){
                if (messageList.length !== 0){
                    do_scroll_down.current = false;
                }

                setMessageList(messageList => data.message.concat(messageList));

            }
            if (data.type === "new message"){
                do_scroll_down.current = true;
                setMessageList(messageList => messageList.concat(data.message));
            }

        };

        return () => {
            socket.close();
        };
    }, [socket]);


    /**
     * this effect makes sure that the message board scrolls down to the bottom of the message stream at the start of
     * the program
     * */
    const scroll_bottom = React.createRef()
    const do_scroll_down = useRef(true);
    useEffect(() => {
        if (!do_scroll_down.current) return;

        scroll_bottom.current?.scrollIntoView({ behavior: "smooth" })
    }, [scroll_bottom]);

    return (
      <>
          {/*Display the messages*/}
          <div style={{"overflow-y": "scroll", "height":"80%", "scrollbar-width:": "none", "borderBottom":"0.3vw solid var(--tertiaryColor)"}}>
              {messageList.map((d, index) => <Message key={index} message={d}/>)}
              <div ref={scroll_bottom}/>
          </div>

          <SendMessage socket={socket}/>
      </>
    )
}

export default MessageBoard