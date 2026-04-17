'use client';

import React, { useState } from 'react';
import Sidebar from '@/components/Sidebar';
import Navbar from '@/components/Navbar';
import FundCard from '@/components/FundCard';
import ChatWidget from '@/components/ChatWidget';

export default function Home() {
  const [activeFilter, setActiveFilter] = useState('All Funds');

  const filters = ['All Funds', 'Large Cap', 'Index Funds', 'Mid Cap', 'Small Cap', 'ELSS Tax Saver'];

  const funds = [
    { name: 'HDFC Index Nifty 50', category: 'Passive Equity Fund', risk: 'Moderate', expenseRatio: '0.20%', minSip: '₹100' },
    { name: 'HDFC Mid Cap Fund', category: 'Equity: Mid Cap', risk: 'Very High', expenseRatio: '0.77%', minSip: '₹1,000' },
    { name: 'HDFC Large Cap Fund', category: 'Equity: Large Cap', risk: 'Very High', expenseRatio: '0.89%', minSip: '₹1,000' },
    { name: 'HDFC ELSS Tax Saver', category: 'Section 80C Optimized', risk: 'High', expenseRatio: '0.91%', minSip: '₹500' },
    { name: 'HDFC Focused Fund', category: 'Equity Mutual Fund', risk: 'Very High', expenseRatio: '0.95%', minSip: '₹1,000' },
    { name: 'HDFC Equity Fund', category: 'Multi Cap Strategy', risk: 'Very High', expenseRatio: '0.85%', minSip: '₹500' },
  ];

  return (
    <main style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      
      <div style={{ 
        flex: 1, 
        marginLeft: 'var(--sidebar-width)', 
        paddingLeft: '1rem',
        paddingRight: '1rem',
        display: 'flex', 
        flexDirection: 'column' 
      }}>
        <Navbar />

        <div style={{ padding: '1rem 2rem' }}>
          <section style={{ marginBottom: '2.5rem' }}>
            <h2 style={{ fontSize: '2.2rem', fontWeight: '800', color: 'var(--text-main)', marginBottom: '0.75rem' }}>
              Curated Mutual Funds
            </h2>
            <p style={{ color: 'var(--text-dim)', maxWidth: '700px', lineHeight: '1.6', fontSize: '1.05rem' }}>
              Discover high-performing funds selected based on historical market trends. 
              Our digital curator analyzes thousands of data points to bring you the best opportunities.
            </p>
          </section>

          <section style={{ display: 'flex', gap: '12px', marginBottom: '2.5rem', flexWrap: 'wrap' }}>
            {filters.map(filter => (
              <button
                key={filter}
                onClick={() => setActiveFilter(filter)}
                style={{
                  padding: '10px 24px',
                  borderRadius: '100px',
                  border: 'none',
                  backgroundColor: activeFilter === filter ? 'var(--primary-green)' : '#e2e8f0',
                  color: activeFilter === filter ? 'white' : 'var(--text-main)',
                  fontWeight: '600',
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                  transition: 'background-color 0.2s ease'
                }}
              >
                {filter}
              </button>
            ))}
          </section>

          <section style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', 
            gap: '2rem',
            marginBottom: '4rem'
          }}>
            {funds.map((fund, idx) => (
              <FundCard key={idx} {...fund} />
            ))}
          </section>

          <section style={{
            background: 'linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%)',
            borderRadius: '24px',
            padding: '3rem',
            color: 'white',
            position: 'relative',
            overflow: 'hidden',
            marginBottom: '4rem'
          }}>
            <div style={{ position: 'relative', zIndex: 1 }}>
              <h3 style={{ fontSize: '2rem', fontWeight: '800', marginBottom: '1rem' }}>
                Start your SIP today with just ₹100.
              </h3>
              <p style={{ maxWidth: '600px', marginBottom: '2rem', opacity: 0.9, lineHeight: '1.6' }}>
                Small, consistent investments can lead to massive wealth over time. 
                Use our calculator to see your potential growth.
              </p>
              <button style={{
                padding: '1rem 2.5rem',
                backgroundColor: 'white',
                color: 'var(--primary-green)',
                border: 'none',
                borderRadius: '12px',
                fontWeight: '700',
                cursor: 'pointer',
                fontSize: '1rem'
              }}>
                Open Calculator
              </button>
            </div>
            {/* Abstract Background patterns */}
            <div style={{ 
              position: 'absolute', 
              right: '-50px', 
              bottom: '-50px', 
              width: '300px', 
              height: '300px', 
              backgroundColor: 'rgba(255,255,255,0.1)', 
              borderRadius: '50%' 
            }} />
          </section>
        </div>
      </div>

      <ChatWidget />
    </main>
  );
}
