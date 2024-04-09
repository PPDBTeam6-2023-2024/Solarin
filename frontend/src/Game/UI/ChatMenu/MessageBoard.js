import React, {useEffect, useRef, useState} from "react";
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


    const scroll_bar = useRef(null);

    /**
    * makes sure that UseEffect for connecting to the websocket is not called twice
     * in react strict mode
    * */
    const is_connected = useRef(false);

   useEffect(() => {
       if (is_connected.current) return

       is_connected.current = true;

       const web_socket = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/chat/dm/${props.message_board}`, `${localStorage.getItem('access-token')}`);
        setSocket(web_socket);
    }, []);

    useEffect(() => {
        if (!socket) return;

        let loaded = false;

        socket.onmessage = (event) => {
            let data = JSON.parse(event.data)
            if (data.type === "paging"){

                /*in case we receive new pages, we don't want to scroll down fully*/
                if (loaded){
                    do_scroll_down.current = false;

                    /*
                    * calculate how much we need to scroll down to keep the messages visually on the right spot (new messages appear on top)
                    * */
                    let message_height = scroll_bar.current?.childNodes[0].clientHeight;

                    /*
                    * multiplier 1.1 makes the visuals more smooth
                    * */
                    scroll_bar.current?.scrollTo(0, (data.message.length+1)*message_height*1.1);
                }
                loaded = true;

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

    /*make sure to ask for more pages (paging) when top scrollbar has been reached*/
    useEffect(() => {
        if (scroll_bar.current === null) {return;}

        const checkPaging = () =>{
            if (scroll_bar.current?.scrollTop > 0) return;
            socket.send(
                JSON.stringify(
                {
                        type: "paging",
                        limit: 10,
                        offset: messageList.length
                      })
            )


        }
        scroll_bar.current?.addEventListener('scroll', checkPaging)

        return () => {
            /*should remove listener or dismount*/
            scroll_bar.current?.removeEventListener('scroll', checkPaging)
        };

    }, [scroll_bar, socket, messageList]);

    return (
      <>
          {/*Display the messages*/}
          <div ref={scroll_bar} style={{"overflow-y": "scroll", "height":"80%", "scrollbarWidth:": "none", "borderBottom":"0.3vw solid var(--tertiaryColor)"}}>
              {messageList.map((d, index) => <Message key={index} message={d}/>)}
              <div ref={scroll_bottom}/>
          </div>

          <SendMessage socket={socket}/>
      </>
    )
}

export default MessageBoard