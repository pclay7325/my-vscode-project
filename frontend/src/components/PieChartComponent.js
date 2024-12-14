import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function PieChartComponent({ data }) {
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  if (!data || data.length === 0) {
    return <div>No data available for Pie Chart</div>;
  }

  return (
    <div id="pie-chart" style={{ textAlign: 'center', marginTop: '20px' }}>
      <h3>Pie Chart: OEE Distribution</h3>
      <ResponsiveContainer width="95%" height={400}>
        <PieChart>
          <Pie
            data={data}
            dataKey="oee"
            nameKey="file_id"
            cx="50%"
            cy="50%"
            outerRadius={150}
            fill="#8884d8"
            label
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PieChartComponent;
