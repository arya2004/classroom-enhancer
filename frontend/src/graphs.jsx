import React, { useEffect, useRef, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Chart from 'chart.js/auto';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';

const LineChart = ({ labels, data }) => {
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);
  useEffect(() => {
    const ctx = chartRef.current.getContext('2d');

    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    const chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Problem solved',
          data: data,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Question Score'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Question Number'
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Student Engagement'
          }
        }
      }
    });

    chartInstanceRef.current = chartInstance;

    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
        chartInstanceRef.current = null;
      }
    };
  }, [labels, data]);

  return <canvas ref={chartRef} />;
};

const PieChart = ({ correct, incorrect }) => {
  const data = {
    labels: ['Correct', 'Incorrect'],
    datasets: [
      {
        data: [correct, incorrect],
        backgroundColor: ['#36A2EB', '#FF6384'],
        hoverBackgroundColor: ['#36A2EB', '#FF6384'],
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
  };

  return <Pie data={data} options={options} />;
};

function Graphs() {
  const [answer, setAnswer] = useState([]);

  useEffect(() => {
    const fetchData = () => {
      axios.get('http://127.0.0.1:5000/get_answer')
        .then(response => {
          setAnswer(response.data);
          console.log(response.data);
        })
        .catch(error => {
          console.error('Error fetching times:', error);
        });
    };

    const intervalId = setInterval(fetchData, 15000);
    return () => clearInterval(intervalId);
  }, []);

  const labels = [1, 2, 3, 4, 5, 6, 7, 8, 10];
  const answerSize = answer.length;
  const numberOfOnes = answer.filter(num => num === 1).length;

  return (
    <div className="container mx-auto px-4 py-8 border border-gray-300 rounded-lg">
             <w3m-button />
      <center>
        <h1 className="mb-4 text-3xl font-extrabold text-gray-900 dark:text-red md:text-5xl lg:text-6xl">
          <span className="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">
            Engagement Analytics
          </span>
        </h1>
      </center>
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
        <div className="flex justify-between">
          <div className="flex flex-col items-center">
            <p className="text-lg font-semibold">Number of Correct Answers</p>
            <p className="text-3xl font-bold text-blue-500">{numberOfOnes}</p>
          </div>
          <div className="flex flex-col items-center">
            <p className="text-lg font-semibold">Number of Wrong Answers</p>
            <p className="text-3xl font-bold text-red-500">{answerSize - numberOfOnes}</p>
          </div>
          <div className="flex flex-col items-center">
            <p className="text-lg font-semibold">Total Questions</p>
            <p className="text-3xl font-bold text-green-500">{answerSize}</p>
          </div>
          <div className="flex flex-col items-center">
            <p className="text-lg font-semibold">Percentage</p>
            <p className="text-3xl font-bold text-pink-500">{(numberOfOnes / answerSize * 100).toFixed(2)}%</p>
          </div>
        </div>
      </div>
      <div className="py-8 grid grid-cols-2 gap-10" style={{ marginLeft:"100px"}}>
        <div>
          <h2 className="text-xl font-semibold mb-2">Line Chart</h2>
          <div className="bg-white p-4 rounded-lg shadow-md border border-gray-200">
            <LineChart labels={labels} data={answer} />
          </div>
          <br />
          <br />
          <h2 className="text-xl font-semibold mb-2">Time Of Disengagement</h2>
          <div className="bg-white p-4 rounded-lg shadow-md border border-gray-200">
            {answer.map((num, index) => (
              num === 0 ? <p key={index}><span className='text-sky-400'> Question Number {index+1}</span> {Math.round(index / 3)}min - {Math.round((index)/3)+1}min</p> : null
            ))}
          </div>
        </div>
        <div>
  <h2 className="text-xl font-semibold mb-2" style={{ marginLeft:"140px"}}>Pie Chart</h2>
  <div style={{ width: '400px', height: '400px' , marginLeft:'140px'} } className="bg-white p-4 rounded-lg shadow-md border border-gray-200">
    <PieChart correct={numberOfOnes} incorrect={answerSize - numberOfOnes} />
  </div>
</div>
      </div>
    </div>
  );
}

export default Graphs;