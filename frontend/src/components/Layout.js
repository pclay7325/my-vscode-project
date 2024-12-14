import React from 'react';
import './Layout.css'; // Add custom styles for the layout

function Layout({ children }) {
  return (
    <div className="layout">
      {/* Header */}
      <header className="header">
        <div className="container">
          <div className="logo">LOGO</div>
          <nav>
            <ul className="nav-links">
              <li><a href="/">Home</a></li>
              <li><a href="/charts">Charts</a></li>
              <li><a href="/dashboard">Dashboard</a></li>
              <li><a href="/settings">Settings</a></li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Page Content */}
      <main className="content">
        {children}
      </main>

      {/* Footer (Optional) */}
      <footer className="footer">
        <p>&copy; 2024 Your Company. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default Layout;
