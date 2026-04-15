import { useNavigate } from 'react-router-dom';
const C = { gold: '#d4af37', primary: '#0f172a' };

export default function Landing() {
  const nav = useNavigate();
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', alignItems: 'center', padding: '15px 50px', borderBottom: `3px solid ${C.gold}` }}>
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg" style={{ height: 70, marginRight: 20 }} alt="Emblem" />
        <div>
          <div style={{ fontWeight: 'bold', fontSize: 13 }}>भारत का सर्वोच्च न्यायालय</div>
          <div style={{ fontWeight: 'bold', fontSize: 24, textTransform: 'uppercase' }}>Supreme Court of India</div>
          <div style={{ fontSize: 13 }}>|| यतो धर्मस्ततो जय: ||</div>
        </div>
      </div>
      <div style={{ flex: 1, background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 40 }}>
        <h1 style={{ fontSize: '5rem', fontWeight: 800, color: 'white', margin: 0, textShadow: '2px 2px 8px rgba(0,0,0,0.5)' }}>न्याय</h1>
        <p style={{ color: '#94a3b8', fontSize: '1.1rem', marginBottom: 8 }}>Judicial Priority Scheduling Initiative</p>
        <p style={{ color: C.gold, letterSpacing: 4, fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', marginBottom: 50 }}>Powered by JUSTIS Engine v2.0</p>
        <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap', justifyContent: 'center' }}>
          {[
            { role: 'judge', label: '⚖️ Judge', color: C.gold, textColor: C.primary },
            { role: 'lawyer', label: '📄 Advocate', color: 'rgba(255,255,255,0.1)', textColor: 'white', border: `1px solid ${C.gold}` },
            { role: 'citizen', label: '👤 Citizen', color: 'rgba(16,185,129,0.2)', textColor: '#10b981', border: '1px solid #10b981' },
          ].map(({ role, label, color, textColor, border }) => (
            <button key={role} onClick={() => nav(`/login/${role}`)}
              style={{ background: color, color: textColor, padding: '14px 32px', borderRadius: 8, border: border || 'none', cursor: 'pointer', fontWeight: 700, fontSize: 16 }}>
              {label}
            </button>
          ))}
        </div>
        <p style={{ position: 'absolute', bottom: 20, color: '#64748b', fontSize: 12, textAlign: 'center' }}>
          System Disclaimer: न्याय assists judicial scheduling. Final authority rests with the Hon'ble Court.
        </p>
      </div>
    </div>
  );
}