import React, { useContext } from 'react';
import { ChartContext } from '../context/ChartContext';
import ChartGrid from '../components/ChartGrid';

function Charts() {
  const { filteredData, paretoData } = useContext(ChartContext);

  return (
    <div>
      <h1>Charts Page</h1>
      <ChartGrid paretoData={paretoData} filteredData={filteredData} />
    </div>
  );
}

export default Charts;
