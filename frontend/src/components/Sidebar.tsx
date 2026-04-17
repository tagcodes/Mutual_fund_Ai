import React from 'react';

const Sidebar = () => {
  const menuItems = [
    { name: 'Dashboard', icon: '📊' },
    { name: 'Mutual Funds', icon: '🏛️', active: true },
    { name: 'Stocks', icon: '📈' },
    { name: 'Portfolio', icon: '💼' },
    { name: 'Reports', icon: '📄' },
  ];

  return (
    <aside style={{
      width: 'var(--sidebar-width)',
      height: '100vh',
      backgroundColor: 'var(--sidebar-white)',
      borderRight: '1px solid var(--border-light)',
      display: 'flex',
      flexDirection: 'column',
      padding: '2rem 1.5rem',
      position: 'fixed',
      left: 0,
      top: 0
    }}>
      <div style={{ marginBottom: '3rem' }}>
        <h1 style={{ 
          color: 'var(--primary-green)', 
          fontSize: '1.5rem', 
          fontWeight: 'bold',
          letterSpacing: '-0.02em'
        }}>
          FintechCurator
        </h1>
        <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '0.25rem' }}>
          INVESTMENT HUB
        </p>
      </div>

      <nav style={{ flex: 1 }}>
        {menuItems.map((item) => (
          <div key={item.name} style={{
            display: 'flex',
            alignItems: 'center',
            padding: '0.875rem 1rem',
            marginBottom: '0.5rem',
            borderRadius: '12px',
            cursor: 'pointer',
            backgroundColor: item.active ? '#e6f0ed' : 'transparent',
            color: item.active ? 'var(--primary-green)' : 'var(--text-main)',
            fontWeight: item.active ? '600' : '400',
            transition: 'all 0.2s ease'
          }}>
            <span style={{ marginRight: '1rem', fontSize: '1.2rem' }}>{item.icon}</span>
            <span style={{ fontSize: '0.925rem' }}>{item.name}</span>
          </div>
        ))}
      </nav>

      <div style={{
        marginTop: 'auto',
        padding: '1.5rem',
        backgroundColor: '#f8fafc',
        borderRadius: '16px',
        textAlign: 'center'
      }}>
        <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginBottom: '1rem' }}>
          Premium Growth
        </p>
        <button style={{
          width: '100%',
          padding: '0.75rem',
          backgroundColor: 'var(--primary-green)',
          color: 'white',
          border: 'none',
          borderRadius: '12px',
          fontWeight: '600',
          cursor: 'pointer'
        }}>
          Invest Now
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
