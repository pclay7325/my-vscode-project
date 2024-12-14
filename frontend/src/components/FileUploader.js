import React, { useState, useMemo } from 'react';
import Papa from 'papaparse';
import * as XLSX from 'xlsx';
import Table from './Table';
import BarChartComponent from './BarChartComponent';
import PieChartComponent from './PieChartComponent';
import LineChartComponent from './LineChartComponent';
import ChartjsParetoChart from './ChartjsParetoChart';
import { transformParetoData } from '../utils/transformParetoData';

function FileUploader() {
  const [filteredData, setFilteredData] = useState([]);
  const [columns, setColumns] = useState([]);
  const [selectedMetric, setSelectedMetric] = useState('oee');

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const fileType = file.name.split('.').pop().toLowerCase();

      if (fileType === 'csv') {
        Papa.parse(file, {
          header: true,
          skipEmptyLines: true,
          complete: (result) => {
            setFilteredData(result.data);
            setColumns(Object.keys(result.data[0] || {}));
          },
        });
      } else if (fileType === 'xlsx' || fileType === 'xls') {
        const reader = new FileReader();
        reader.onload = (event) => {
          const binaryData = event.target.result;
          const workbook = XLSX.read(binaryData, { type: 'binary' });
          const sheet = workbook.Sheets[workbook.SheetNames[0]];
          const parsedData = XLSX.utils.sheet_to_json(sheet);
          setFilteredData(parsedData);
          setColumns(Object.keys(parsedData[0] || {}));
        };
        reader.readAsBinaryString(file);
      } else {
        alert('Unsupported file type! Please upload a CSV or Excel file.');
      }
    }
  };

  const paretoData = useMemo(() => transformParetoData(filteredData, selectedMetric), [filteredData, selectedMetric]);

  console.log('Filtered Data:', filteredData);
  console.log('Columns:', columns);
  console.log('Pareto Data:', paretoData);

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h2>Upload a Dataset</h2>
      <input type="file" accept=".csv, .xls, .xlsx" onChange={handleFileUpload} />

      {filteredData.length > 0 && (
        <>
          <Table data={filteredData} columns={columns} />

          <label>
            Select Metric:
            <select value={selectedMetric} onChange={(e) => setSelectedMetric(e.target.value)}>
              {columns.map((key) => (
                <option key={key} value={key}>
                  {key.toUpperCase()}
                </option>
              ))}
            </select>
          </label>

          <ChartjsParetoChart data={paretoData} />

          {/* Render Other Charts */}
          <BarChartComponent data={filteredData} />
          <PieChartComponent data={filteredData} />
          <LineChartComponent data={filteredData} />
        </>
      )}
    </div>
  );
}

export default FileUploader;
