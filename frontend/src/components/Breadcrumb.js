import React from 'react';

function Breadcrumb({ paths = [], onNavigate }) {
  return (
    <div
      style={{
        padding: '10px 20px',
        backgroundColor: '#e9ecef',
        display: 'flex',
        gap: '5px',
      }}
    >
      {paths.map((path, index) => (
        <span
          key={index}
          onClick={() => onNavigate && onNavigate(path)}
          style={{
            fontWeight: index === paths.length - 1 ? 'bold' : 'normal',
            cursor: index < paths.length - 1 ? 'pointer' : 'default',
            color: index < paths.length - 1 ? '#007bff' : 'black',
          }}
        >
          {path}
          {index < paths.length - 1 && ' / '}
        </span>
      ))}
    </div>
  );
}

export default Breadcrumb; // Ensure this is present!
