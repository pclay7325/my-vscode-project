import React from 'react';

function Navbar() {
  return (
    <nav
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '10px 20px',
        backgroundColor: '#f8f9fa',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
        position: 'sticky',
        top: '0',
        zIndex: '1000',
      }}
    >
      {/* Left section */}
      <div>
        <a
          href="/"
          style={{
            margin: '0 15px',
            textDecoration: 'none',
            color: '#000',
            fontWeight: 'bold',
          }}
        >
          Dashboards
        </a>
        <a
          href="/apps"
          style={{
            margin: '0 15px',
            textDecoration: 'none',
            color: '#000',
          }}
        >
          Apps
        </a>
        <a
          href="/automations"
          style={{
            margin: '0 15px',
            textDecoration: 'none',
            color: '#000',
          }}
        >
          Automations
        </a>
        <a
          href="/shop-floor"
          style={{
            margin: '0 15px',
            textDecoration: 'none',
            color: '#000',
          }}
        >
          Shop Floor
        </a>
      </div>

      {/* Right section */}
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <span style={{ marginRight: '15px', fontWeight: 'bold', color: '#555' }}>
          PC
        </span>
        <img
          src="https://via.placeholder.com/30"
          alt="Profile"
          style={{
            width: '30px',
            height: '30px',
            borderRadius: '50%',
            border: '1px solid #ddd',
          }}
        />
      </div>
    </nav>
  );
}

export default Navbar;
