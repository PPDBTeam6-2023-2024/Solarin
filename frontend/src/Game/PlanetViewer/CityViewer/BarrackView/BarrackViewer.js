import Draggable from 'react-draggable'
import FriendsTab from "../../../UI/ChatMenu/Friends/FriendsTab";
import AllianceTab from "../../../UI/ChatMenu/Alliance/AllianceTab";
import RankingTab from "../../../UI/ChatMenu/Ranking/RankingTab";
import React from "react";
import './BarrackViewer.css'

function BarrackViewer(props) {
    return (
        <Draggable>
          {/*Creates the div that containing the barrack interface*/}
          <div id="BarrackViewerBox">

          </div>
        </Draggable>
    )
}
export default BarrackViewer