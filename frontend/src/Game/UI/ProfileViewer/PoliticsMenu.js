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

ChartJS.register(LineController, LineElement, PointElement, LinearScale, Title, RadialLinearScale, Filler);

// limiting function used to keep modifiers in a reasonable range [-30%, +30%]
function clamp(value) {
    return Math.min(Math.max(value, -30), 30);
}

function generateModifiers(stance) {
    const resourceProduction = Math.round(
        (stance.anarchism * 10) +   // Scale up by 10x
        (stance.democratic * 3) -   // Scale up by 10x
        (stance.theocracy * 10) -   // Scale up by 10x
        (stance.technocracy * 5) +  // Scale up by 10x
        (stance.corporate_state * 20)  // Scale up by 10x
    );

    const upgradeSpeed = Math.round(
        (stance.technocracy * 25) +  // Scale up by 10x
        (stance.democratic * 20) -   // Scale up by 10x
        (stance.authoritarian * 15) -  // Scale up by 10x
        (stance.theocracy * 20) -    // Scale up by 10x
        (stance.corporate_state * 10)  // Scale up by 10x
    );

    const armyStrength = Math.round(
        (stance.authoritarian * 30) -  // Scale up by 10x
        (stance.anarchism * 20) +    // Scale up by 10x
        (stance.theocracy * 15) -    // Scale up by 10x
        (stance.democratic * 10)    // Scale up by 10x
    );

    const trainingTime = Math.round(
        -(stance.authoritarian * 20) -  // Scale up by 10x
        (stance.technocracy * 15) -     // Scale up by 10x
        (stance.corporate_state * 10) +  // Scale up by 10x
        (stance.theocracy * 10)    // Scale up by 10x
    );

    const armyMovementSpeed = Math.round(
        (stance.anarchism * 10) -   // Scale up by 10x
        (stance.corporate_state * 30) -  // Scale up by 10x
        (stance.theocracy * 5)   // Scale up by 10x
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
    const [stanceFetched, setStanceFetched] = useState(false);

    const updateStance = async (impacts, cost) => {
    console.log("updateStance");
    setStanceFetched(false);
    try {
        const payload = {
            ...impacts,
            Cost: cost
        };
        await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/logic/update_politics`, payload);
    } catch (error) {
        console.error('Failed to update political stance:', error);
    }
};


    useEffect(() => {
        const fetchStance = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/logic/politics`);
                setStance(response.data);
            } catch (error) {
                console.error('Error while fetching political stance:', error);
            }
        };

        fetchStance();
        console.log("fetch Stance");
        setStanceFetched(true);
    }, [stanceFetched]);

    const modifiers = generateModifiers(stance);

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
                        {statName}:
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
