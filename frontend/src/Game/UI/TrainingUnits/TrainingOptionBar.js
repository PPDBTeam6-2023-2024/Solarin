import React, {useEffect, useState} from "react";
import './TrainingViewer.css'
import './TrainingOptionBar.css'
import TrainingOptionEntry from "./TrainingOptionEntry";
import TrainingOptionAdder from "./TrainingOptionAdder";

function TrainingOptionBar(props) {
    /*
    * In the training menu we can choose new units we want to train
    * This component will have the list of units we can train
    * */

    const [selected, setSelected] = useState("");

    const [troopsJson, setTroopsJson] = useState({});

    useEffect(() => {
        const importTroopsJson = async () => {
            try {
                const module = await import(`./../troops_${props.buildingType}.json`);
                setTroopsJson(module.default);
            } catch (error) {
                console.error("Error importing troops data: ", error);
            }
        };

        importTroopsJson();
    }, [props.buildingType]);

    const changeSelected = (key) => {
        if (selected === key) {
            setSelected("")
        } else {
            setSelected(key)
        }
    }
    return (
        <>
            <div className="TrainingOptionList">
                {Object.keys(troopsJson).map((key, index) =>


                    <>
                        {selected === key ?
                            <TrainingOptionEntry key={index} type={key} image={troopsJson[key]["icon"]} select={true}
                                                 onSelect={() => changeSelected(key)}/> :
                            <TrainingOptionEntry key={index} type={key} image={troopsJson[key]["icon"]} select={false}
                                                 onSelect={() => changeSelected(key)}/>
                        }
                    </>
                )
                }
            </div>
            {selected !== "" && <TrainingOptionAdder onTrain={props.onTrain} type={selected}/>}
        </>
    )
}

export default TrainingOptionBar