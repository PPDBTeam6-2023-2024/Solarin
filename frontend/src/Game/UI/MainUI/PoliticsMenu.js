import {Chart, Radar} from 'react-chartjs-2';
import { Chart as ChartJS, LineController, LineElement, PointElement, LinearScale, Title, RadialLinearScale, Filler } from 'chart.js';

ChartJS.register(LineController, LineElement, PointElement, LinearScale, Title, RadialLinearScale, Filler);


function PoliticsMenu() {
    /*THIS PAGE IS A MOCK PAGE AND NOT A FINISHED RESULT*/
    const data = {
    labels: ['Anarchism', 'Authoritarian', 'Democratic', 'Corporatism', 'Religious'],
    datasets: [
      {
        data: [0.3, 0.3, 0.5, 0.2, 0.6],
        backgroundColor: 'rgba(215,113,12, 0.6)',
        borderColor: 'rgba(220,53,16, 0.8)',
          fill: true,
        borderWidth: 3,
      },
    ],
    };

     const options= {

    scales: {
        r:{
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
            {/*Display graph about ideology*/}
            <div style={{"height": "30vw"}}>
                <Radar data={data} options={options}/>
            </div>

            {/*Demo stat*/}
            <div style={{"width": "40%"}}>
                <div style={{"whiteSpace": "nowrap", "display": "inline"}}>
                    resource production: <span style={{"color": "green", "display": "inline"}}>+3%</span>
                </div>

            </div>

            {/*Demo stat*/}
            <div style={{"width": "40%"}}>
                <div style={{"whiteSpace": "nowrap", "display": "inline"}}>
                    upgrade speed: <span style={{"color": "green", "display": "inline"}}>+20%</span>
                </div>

            </div>

            {/*Demo stat*/}
            <div style={{"width": "40%"}}>
                <div style={{"whiteSpace": "nowrap", "display": "inline"}}>
                    Army Strength: <span style={{"color": "red", "display": "inline"}}>-10%</span>
                </div>

            </div>

            {/*Demo stat*/}
            <div style={{"width": "40%"}}>
                <div style={{"whiteSpace": "nowrap", "display": "inline"}}>
                    training time: <span style={{"color": "green", "display": "inline"}}>-10%</span>
                </div>

            </div>

            {/*Demo stat*/}
            <div style={{"width": "40%"}}>
                <div style={{"whiteSpace": "nowrap", "display": "inline"}}>
                    Army movement speed <span style={{"color": "red", "display": "inline"}}>-40%</span>
                </div>

            </div>

        </>


    )


}

export default PoliticsMenu;