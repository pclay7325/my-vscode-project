import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function LineChartComponent({ data }) {
  if (!data || data.length === 0) {
    return <div>No data available for Line Chart</div>;
  }

  return (
    <div id="line-chart" style={{ textAlign: 'center', marginTop: '20px' }}>
      <h3>Line Chart: Timestamp vs OEE</h3>
      <ResponsiveContainer width="95%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="oee" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default LineChartComponent;
