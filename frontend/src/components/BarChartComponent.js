import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function BarChartComponent({ data }) {
  if (!data || data.length === 0) {
    return <div>No data available for Bar Chart</div>;
  }

  return (
    <div id="bar-chart" style={{ textAlign: 'center', marginTop: '20px' }}>
      <h3>Bar Chart: File ID vs OEE</h3>
      <ResponsiveContainer width="95%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="file_id" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="oee" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default BarChartComponent;
