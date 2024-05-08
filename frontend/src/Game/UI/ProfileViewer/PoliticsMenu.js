import {Chart, Radar} from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    RadialLinearScale,
    Filler
} from 'chart.js';
import PoliticsDecision from "./PoliticsDecision";
import axios from "axios";
import {useEffect, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {setResources} from "../../../redux/slices/resourcesSlice";

ChartJS.register(LineController, LineElement, PointElement, LinearScale, Title, RadialLinearScale, Filler);

// limiting function used to keep modifiers in a reasonable range [-30%, +30%]
function clamp(value) {
    return Math.min(Math.max(value, -30), 30);
}

function generateModifiers(stance) {
    const resourceProduction = Math.round(
        (stance.anarchism * 10) +
        (stance.democratic * 3) -
        (stance.theocracy * 10) -
        (stance.technocracy * 5) +
        (stance.corporate_state * 20)
    );

    const upgradeSpeed = Math.round(
        (stance.technocracy * 25) +
        (stance.democratic * 20) -
        (stance.authoritarian * 15) -
        (stance.theocracy * 20) -
        (stance.corporate_state * 10)
    );

    const armyStrength = Math.round(
        (stance.authoritarian * 30) -
        (stance.anarchism * 20) +
        (stance.theocracy * 15) -
        (stance.democratic * 10)
    );

    const trainingTime = Math.round(
        -(stance.authoritarian * 20) -
        (stance.technocracy * 15) -
        (stance.corporate_state * 10) +
        (stance.theocracy * 10)
    );

    const armyMovementSpeed = Math.round(
        (stance.anarchism * 10) -
        (stance.corporate_state * 30) -
        (stance.theocracy * 5)
    );

    return {
        resourceProduction: clamp(resourceProduction),
        upgradeSpeed: clamp(upgradeSpeed),
        armyStrength: clamp(armyStrength),
        trainingTime: clamp(trainingTime),
        armyMovementSpeed: clamp(armyMovementSpeed)
    };
}

// Helper function to format the modifiers as a string with a sign
function formatModifier(value) {
    return `${value >= 0 ? '+' : ''}${value}%`;
}

function PoliticsMenu() {
    const [stance, setStance] = useState({});
    const [stanceFetched, setStanceFetched] = useState(false)

    const dispatch = useDispatch()

    const updateStance = async (impacts, cost) => {
        /*Update political information*/
        try {
            const payload = {
                ...impacts,
                Cost: cost
            };
            console.log(payload);
            await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/logic/update_politics`, payload);
            setStanceFetched(false)

            /*Recalibrate the resources*/
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/logic/resources`);
            if (response.status === 200) {
                dispatch(setResources(response.data))
            }
            fetchStance();

        } catch (error) {
            console.error('Failed to update political stance:', error);
        }
    };

    const fetchStance = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/logic/politics`);
            setStance(response.data);
            setStanceFetched(true)
        } catch (error) {
            console.error('Error while fetching political stance:', error);
        }
    };

    useEffect(() => {

        fetchStance();
    }, []);

    const modifiers = generateModifiers(stance);
    console.log(stance)
    const data = {
        labels: ['Anarchism', 'Authoritarian', 'Democratic', 'Corporate state', 'Theocracy', 'Technocracy'],
        datasets: [
            {
                data: [stance.anarchism, stance.authoritarian, stance.democratic, stance.corporate_state, stance.theocracy, stance.technocracy],
                backgroundColor: 'rgba(215,113,12, 0.6)',
                borderColor: 'rgba(220,53,16, 0.8)',
                fill: true,
                borderWidth: 3,
            },
        ],
    };

    const options = {
        scales: {
            r: {
                ticks: {
                    display: false,
                    beginAtZero: true,
                    max: 1,
                    min: 0,
                    stepSize: 1
                },
                grid: {
                    display: true,
                    color: 'white',
                    lineWidth: 0.1
                },
                angleLines: {
                    display: true,
                    color: 'white',
                    lineWidth: 0.3
                }
            },
            maintainAspectRatio: true
        }
    };

    return (
        <>
            <div style={{height: "30vw"}}>
                <Radar data={data} options={options}/>
            </div>
            {Object.entries(modifiers).map(([statName, statValue]) => (
                <div key={statName} style={{width: "40%"}}>
                    <div style={{whiteSpace: "nowrap", display: "inline"}}>
                        {statName.replace(/([A-Z])/g, ' $1').trim()}:
                        <span style={{
                            color: statValue === 0 ? "#777" : (statValue > 0 ? "green" : "red"),
                            display: "inline"
                        }}>
                        {formatModifier(statValue)}
                    </span>
                    </div>
                </div>
            ))}
            <div>
                Decisions:
                <PoliticsDecision updateStance={updateStance}/>
            </div>
        </>
    );
}

export default PoliticsMenu;
