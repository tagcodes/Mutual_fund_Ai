import React from 'react';

const Navbar = () => {
  return (
    <header style={{
      height: '70px',
      backgroundColor: 'transparent',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 2rem',
      marginBottom: '1rem'
    }}>
      <div style={{ position: 'relative', width: '400px' }}>
        <span style={{ position: 'absolute', left: '15px', top: '50%', transform: 'translateY(-50%)', opacity: 0.5 }}>🔍</span>
        <input 
          type="text" 
          placeholder="Search mutual funds, stocks, or ETFs..." 
          style={{
            width: '100%',
            padding: '12px 15px 12px 45px',
            borderRadius: '12px',
            border: '1px solid var(--border-light)',
            backgroundColor: 'white',
            outline: 'none',
            fontSize: '0.85rem'
          }}
        />
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <div style={{ display: 'flex', gap: '15px' }}>
          <button style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem' }}>🔔</button>
          <button style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem' }}>❔</button>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ width: '40px', height: '40px', borderRadius: '50%', overflow: 'hidden', backgroundColor: '#e2e8f0' }}>
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="User" />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
