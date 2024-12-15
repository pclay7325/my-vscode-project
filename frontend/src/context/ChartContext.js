import React, { createContext, useState } from 'react';

export const ChartContext = createContext();

export const ChartProvider = ({ children }) => {
  const [filteredData, setFilteredData] = useState([]);
  const [paretoData, setParetoData] = useState([]);

  return (
    <ChartContext.Provider value={{ filteredData, setFilteredData, paretoData, setParetoData }}>
      {children}
    </ChartContext.Provider>
  );
};
