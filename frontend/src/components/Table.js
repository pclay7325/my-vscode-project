import React from 'react';

function Table({ data, columns }) {
  return (
    <div style={{ marginTop: '20px', overflowX: 'auto' }}>
      <table style={{ width: '80%', margin: '0 auto', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {columns.map((column, index) => (
              <th
                key={index}
                style={{
                  padding: '10px',
                  border: '1px solid #ddd',
                  backgroundColor: '#f8f9fa',
                }}
              >
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column, colIndex) => (
                <td
                  key={colIndex}
                  style={{ padding: '10px', border: '1px solid #ddd' }}
                >
                  {row[column]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Table;
