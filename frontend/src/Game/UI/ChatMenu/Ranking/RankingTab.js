import React, {useEffect, useState, useContext} from "react";
import "../Alliance/AllianceTab.css"
import "../Requests/RequestButtons.css"
import axios from "axios";
import RankingEntry from "./RankingEntry";

const getRanking = async() => {
    try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/chat/ranking`)
        return response.data
    }
    catch(e) {return []}
}

const RankingTab = (props) => {

    const [ranking, setRanking] = useState([]);

    useEffect(() => {
        async function makeRankingEntries() {
            let data = await getRanking()
            setRanking(data)
        }
        makeRankingEntries()
    }, [])



    return (
        <div style={{"overflow-y": "scroll", "height":"93%", "scrollbar-width:": "none"}}>
            {/*Ranking entry containing the rank column headers*/}
            <RankingEntry key={"header"} user={"username"} quantity={"quantity"} index={"ranking"}/>

            {/*Display the Rank entries*/
                ranking.map((elem, index) => <RankingEntry key={index} user={elem[0]} quantity={elem[1]} index={index+1}/>)
            }
        </div>
    )
}

export default RankingTab;