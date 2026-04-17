import React from 'react';

interface FundCardProps {
  name: string;
  category: string;
  risk: string;
  expenseRatio: string;
  minSip: string;
}

const FundCard: React.FC<FundCardProps> = ({ name, category, risk, expenseRatio, minSip }) => {
  const getRiskColor = (risk: string) => {
    if (risk.toLowerCase().includes('high')) return '#ef4444';
    if (risk.toLowerCase().includes('moderate')) return '#f59e0b';
    return '#10b981';
  };

  return (
    <div style={{
      backgroundColor: 'white',
      borderRadius: '20px',
      padding: '1.5rem',
      boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.05)',
      border: '1px solid var(--border-light)',
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div style={{ 
          width: '40px', 
          height: '40px', 
          backgroundColor: '#003366', 
          borderRadius: '8px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontWeight: 'bold',
          fontSize: '0.9rem'
        }}>
          HDFC
        </div>
        <span style={{ 
          fontSize: '0.65rem', 
          fontWeight: '700', 
          color: 'var(--primary-green)',
          backgroundColor: '#e6f0ed',
          padding: '4px 8px',
          borderRadius: '4px',
          textTransform: 'uppercase'
        }}>
          Top Rated
        </span>
      </div>

      <div>
        <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '0.25rem' }}>{name}</h3>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>{category}</p>
      </div>

      <div style={{ marginTop: '0.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', marginBottom: '4px' }}>
          <span style={{ fontWeight: '600', color: 'var(--text-dim)' }}>RISKOMETER</span>
          <span style={{ fontWeight: '700', color: getRiskColor(risk) }}>{risk.toUpperCase()}</span>
        </div>
        <div style={{ 
          height: '4px', 
          width: '100%', 
          backgroundColor: '#f1f5f9', 
          borderRadius: '2px',
          overflow: 'hidden'
        }}>
          <div style={{ 
            height: '100%', 
            width: risk.toLowerCase().includes('high') ? '90%' : '50%', 
            backgroundColor: getRiskColor(risk) 
          }} />
        </div>
      </div>

      <div style={{ display: 'flex', gap: '2rem', marginTop: '0.5rem' }}>
        <div>
          <p style={{ fontSize: '0.65rem', color: 'var(--text-dim)', fontWeight: '600' }}>EXPENSE RATIO</p>
          <p style={{ fontSize: '0.9rem', fontWeight: '700' }}>{expenseRatio}</p>
        </div>
        <div>
          <p style={{ fontSize: '0.65rem', color: 'var(--text-dim)', fontWeight: '600' }}>MIN SIP</p>
          <p style={{ fontSize: '0.9rem', fontWeight: '700' }}>{minSip}</p>
        </div>
      </div>

      <button style={{
        marginTop: '0.5rem',
        width: '100%',
        padding: '0.875rem',
        backgroundColor: 'transparent',
        border: '1px solid var(--border-light)',
        borderRadius: '12px',
        color: 'var(--primary-green)',
        fontWeight: '600',
        cursor: 'pointer',
        transition: 'all 0.2s ease'
      }}>
        View Performance
      </button>
    </div>
  );
};

export default FundCard;
