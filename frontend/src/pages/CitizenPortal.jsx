import { useState } from 'react';
import { searchCases } from '../services/api';
import Header from '../components/Header';

const C = { primary: '#0f172a', gold: '#d4af37', bg: '#f1f5f9', border: '#e2e8f0' };
const card = { background: 'white', padding: '24px', borderRadius: '12px', border: `1px solid ${C.border}`, boxShadow: '0 2px 8px rgba(0,0,0,0.04)' };

export default function CitizenPortal() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const r = await searchCases(query);
      setResults(r.data); setSearched(true);
    } catch { alert('Search failed. Backend may be waking up — try again in 30 seconds.'); }
    setLoading(false);
  };

  const bandColor = (band) => ({
    bg: band?.includes('High') ? '#fee2e2' : band?.includes('Medium') ? '#fef9c3' : '#dcfce7',
    text: band?.includes('High') ? '#b91c1c' : band?.includes('Medium') ? '#92400e' : '#065f46',
    border: band?.includes('High') ? '#ef4444' : band?.includes('Medium') ? '#f59e0b' : '#10b981',
  });

  return (
    <div style={{ minHeight: '100vh', background: C.bg }}>
      <Header title="Citizen Case Status Portal" />
      <div style={{ maxWidth: '760px', margin: '0 auto', padding: '40px 20px' }}>

        <div style={card}>
          <h3 style={{ color: C.primary, marginBottom: '6px' }}>🔍 Track Your Case</h3>
          <p style={{ color: '#64748b', fontSize: '13px', marginBottom: '18px' }}>Enter your Case Number (CNR) to check status and priority band.</p>
          <form onSubmit={handleSearch} style={{ display: 'flex', gap: '12px' }}>
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder="e.g. CRM/2026/0001"
              style={{ flex: 1, padding: '12px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px', outline: 'none' }} />
            <button type="submit" disabled={loading} style={{ background: C.primary, color: 'white', padding: '12px 22px', borderRadius: '6px', border: `1px solid ${C.gold}`, fontWeight: '600', cursor: 'pointer', whiteSpace: 'nowrap' }}>
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>
        </div>

        {searched && results.length === 0 && (
          <div style={{ ...card, marginTop: '20px', textAlign: 'center', padding: '50px' }}>
            <div style={{ fontSize: '36px' }}>🔎</div>
            <h4 style={{ color: C.primary, marginTop: '12px' }}>No cases found for "{query}"</h4>
            <p style={{ color: '#64748b', fontSize: '13px' }}>Check the case number and try again.</p>
          </div>
        )}

        {results.map(c => {
          const bc = bandColor(c.band);
          return (
            <div key={c.id} style={{ ...card, marginTop: '20px', borderLeft: `6px solid ${bc.border}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
                <div>
                  <h3 style={{ color: C.primary, margin: 0 }}>{c.case_id_number}</h3>
                  <p style={{ color: '#64748b', fontSize: '13px', margin: '3px 0 0 0' }}>{c.primary_case_nature} · {c.procedural_stage}</p>
                </div>
                <div style={{ background: bc.bg, color: bc.text, padding: '10px 20px', borderRadius: '10px', fontWeight: '800', fontSize: '15px' }}>
                  {c.band}
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginTop: '18px' }}>
                <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '10px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '700', letterSpacing: '1px' }}>Filed On</div>
                  <div style={{ fontSize: '15px', color: C.primary, fontWeight: '600', marginTop: '4px' }}>{c.filing_date}</div>
                </div>
                <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '10px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '700', letterSpacing: '1px' }}>Current Stage</div>
                  <div style={{ fontSize: '15px', color: C.primary, fontWeight: '600', marginTop: '4px' }}>{c.procedural_stage}</div>
                </div>
              </div>

              <div style={{ background: '#f8fafc', padding: '14px', borderRadius: '8px', border: '1px solid #e2e8f0', marginTop: '14px' }}>
                <div style={{ fontSize: '10px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '700', letterSpacing: '1px' }}>Description</div>
                <div style={{ fontSize: '15px', color: C.primary, fontWeight: '600', marginTop: '4px' }}>{c.description}</div>
              </div>
            </div>
          );
        })}
              </div>
    </div>
  );
}