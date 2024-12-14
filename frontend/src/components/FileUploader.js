import React, { useState, useMemo } from 'react';
import Papa from 'papaparse';
import * as XLSX from 'xlsx';
import Table from './Table';
import BarChartComponent from './BarChartComponent';
import PieChartComponent from './PieChartComponent';
import LineChartComponent from './LineChartComponent';
import ChartjsParetoChart from './ChartjsParetoChart';
import Layout from './Layout';
import { transformParetoData } from '../utils/transformParetoData';

function FileUploader() {
  const [filteredData, setFilteredData] = useState([]);
  const [columns, setColumns] = useState([]);
  const [selectedMetric, setSelectedMetric] = useState('oee'); // Default metric for Pareto Chart

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

  return (
    <Layout>
      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <h2>Upload a Dataset</h2>
        <input
          type="file"
          accept=".csv, .xls, .xlsx"
          onChange={handleFileUpload}
          style={{ margin: '10px 0' }}
        />

        {filteredData.length > 0 && (
          <>
            <label style={{ marginTop: '20px', display: 'block' }}>
              Select Metric:
              <select
                value={selectedMetric}
                onChange={(e) => setSelectedMetric(e.target.value)}
                style={{
                  marginLeft: '10px',
                  padding: '5px',
                  borderRadius: '5px',
                }}
              >
                {columns.map((key) => (
                  <option key={key} value={key}>
                    {key.toUpperCase()}
                  </option>
                ))}
              </select>
            </label>

            <div className="chart-grid">
              {/* Pareto Chart */}
              <div className="chart-container">
                <h3>Pareto Chart</h3>
                <ChartjsParetoChart data={paretoData} />
              </div>

              {/* Bar Chart */}
              <div className="chart-container">
                <h3>Bar Chart</h3>
                <BarChartComponent data={filteredData} />
              </div>

              {/* Pie Chart */}
              <div className="chart-container">
                <h3>Pie Chart</h3>
                <PieChartComponent data={filteredData} />
              </div>

              {/* Line Chart */}
              <div className="chart-container">
                <h3>Line Chart</h3>
                <LineChartComponent data={filteredData} />
              </div>
            </div>
          </>
        )}
      </div>
    </Layout>
  );
}

export default FileUploader;
