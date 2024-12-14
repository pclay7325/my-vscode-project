import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MainContent() {
  const [kpiData, setKpiData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get('http://127.0.0.1:8000/api/kpi_records/')
      .then((response) => {
        setKpiData(response.data);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to fetch KPI data');
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (kpiData.length === 0) return <div>No KPI data available</div>;

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h2>Key Performance Indicators</h2>
      <table style={{ margin: '0 auto', borderCollapse: 'collapse', width: '80%' }}>
        <thead>
          <tr style={{ backgroundColor: '#f8f9fa' }}>
            <th>File ID</th>
            <th>Timestamp</th>
            <th>Availability</th>
            <th>Performance</th>
            <th>Quality</th>
            <th>OEE</th>
          </tr>
        </thead>
        <tbody>
          {kpiData.map((kpi, index) => (
            <tr key={index}>
              <td>{kpi.file_id}</td>
              <td>{kpi.timestamp}</td>
              <td>{kpi.availability}</td>
              <td>{kpi.performance}</td>
              <td>{kpi.quality}</td>
              <td>{kpi.oee}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MainContent;
