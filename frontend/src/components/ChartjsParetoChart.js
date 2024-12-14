import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, Tooltip, Legend);

function ChartjsParetoChart({ data = [] }) {
  if (!data || data.length === 0) {
    return <div>No data available for Pareto Chart</div>;
  }

  const categories = data.map((item) => item.file_id);
  const values = data.map((item) => item.value);
  const cumulativePercentages = data.map((item) => item.cumulativePercent.toFixed(2));

  const chartData = {
    labels: categories,
    datasets: [
      {
        type: 'bar',
        label: 'OEE Value',
        data: values,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        type: 'line',
        label: 'Cumulative Percent',
        data: cumulativePercentages,
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        tension: 0.4,
        yAxisID: 'y2',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      tooltip: {
        callbacks: {
          label: function (context) {
            if (context.datasetIndex === 0) {
              return `OEE Value: ${context.raw}`;
            }
            return `Cumulative Percent: ${context.raw}%`;
          },
        },
      },
      legend: { position: 'bottom' },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'OEE Value' },
      },
      y2: {
        beginAtZero: true,
        position: 'right',
        title: { display: true, text: 'Cumulative Percent (%)' },
        ticks: {
          callback: (value) => `${value}%`,
        },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
}

export default ChartjsParetoChart;
