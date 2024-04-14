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
            he
        </>


    )


}

export default PoliticsMenu;