import React, {useEffect, useRef, useState} from "react";
import "./Friends/FriendOverviewEntry.css"
import Message from "./Message";
import SendMessage from "./SendMessage";


function MessageBoard(props) {
    /**
     * This shows the message stream of a message board
     * */

    const [socket, setSocket] = useState(null);
    const [messageList, setMessageList] = useState([]);


    const scrollBar = useRef(null);

    /**
     * makes sure that UseEffect for connecting to the websocket is not called twice
     * in react strict mode
     * */
    const isConnected = useRef(false);

    useEffect(() => {
        if (isConnected.current) return

        isConnected.current = true;

        const webSocket = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/chat/dm/${props.message_board}`, `${localStorage.getItem('access-token')}`);
        setSocket(webSocket);
    }, []);

    useEffect(() => {
        if (!socket) return;

        let loaded = false;

        socket.onmessage = (event) => {
            let data = JSON.parse(event.data)
            if (data.type === "paging") {

                /*in case we receive new pages, we don't want to scroll down fully*/
                if (loaded) {
                    doScrollDown.current = false;

                    /*
                    * calculate how much we need to scroll down to keep the messages visually on the right spot (new messages appear on top)
                    * */
                    let message_height = scrollBar.current?.childNodes[0].clientHeight;

                    /*
                    * multiplier 1.1 makes the visuals more smooth
                    * */
                    scrollBar.current?.scrollTo(0, (data.message.length + 1) * message_height * 1.1);
                }
                loaded = true;

                setMessageList(messageList => data.message.concat(messageList));

            }
            if (data.type === "new message") {
                doScrollDown.current = true;
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
    const scrollBottom = React.createRef()
    const doScrollDown = useRef(true);
    useEffect(() => {
        if (!doScrollDown.current) return;

        scrollBottom.current?.scrollIntoView({behavior: "smooth"})

    }, [scrollBottom]);

    /*make sure to ask for more pages (paging) when top scrollbar has been reached*/
    useEffect(() => {
        if (scrollBar.current === null) {
            return;
        }

        const checkPaging = () => {
            if (scrollBar.current?.scrollTop > 0) return;
            socket.send(
                JSON.stringify(
                    {
                        type: "paging",
                        limit: 10,
                        offset: messageList.length
                    })
            )


        }
        scrollBar.current?.addEventListener('scroll', checkPaging)

        return () => {
            /*should remove listener or dismount*/
            scrollBar.current?.removeEventListener('scroll', checkPaging)
        };

    }, [scrollBar, socket, messageList]);

    return (
        <>
            {/*Display the messages*/}
            <div ref={scrollBar} style={{
                "overflow-y": "scroll",
                "height": "80%",
                "scrollbarWidth:": "none",
                "borderBottom": "0.3vw solid var(--tertiaryColor)"
            }}>
                {messageList.map((d, index) => <Message key={index} message={d}/>)}
                <div ref={scrollBottom}/>
            </div>

            <SendMessage socket={socket}/>
        </>
    )
}

export default MessageBoard