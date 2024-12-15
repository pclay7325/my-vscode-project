import React from 'react';
import ChartGrid from '../components/ChartGrid';
import { useContext } from 'react';
import { ChartContext } from '../context/ChartContext';

function Charts() {
  const { filteredData, paretoData } = useContext(ChartContext);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Charts Page</h1>
      <p>Here are your charts:</p>
      <ChartGrid paretoData={paretoData} filteredData={filteredData} />
    </div>
  );
}

export default Charts;
