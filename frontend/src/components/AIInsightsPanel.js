// AIInsightsPanel.js - Displays AI-Driven Insights
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AIInsightsPanel() {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get('/api/insights')
      .then((response) => {
        setInsights(response.data);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to fetch AI insights');
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading AI insights...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (insights.length === 0) return <div>No AI insights available</div>;

  return (
    <div style={{ padding: '10px', backgroundColor: '#f9f9f9', borderRadius: '5px' }}>
      <h3 style={{ textAlign: 'center' }}>AI-Driven Insights</h3>
      <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
        {insights.map((insight, index) => (
          <li
            key={index}
            style={{
              marginBottom: '10px',
              padding: '10px',
              backgroundColor: '#fff',
              borderRadius: '5px',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
            }}
          >
            <strong>{insight.title}:</strong> {insight.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AIInsightsPanel;
