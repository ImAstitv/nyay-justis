import { useNavigate } from 'react-router-dom';

const C = { gold: '#d4af37', primary: '#0f172a' };

export default function Landing() {
  const nav = useNavigate();

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', alignItems: 'center', padding: '15px 50px', borderBottom: `3px solid ${C.gold}` }}>
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg" style={{ height: 70, marginRight: 20 }} alt="Emblem" />
        <div>
          <div style={{ fontWeight: 'bold', fontSize: 13 }}>Supreme Court of India</div>
          <div style={{ fontWeight: 'bold', fontSize: 24, textTransform: 'uppercase' }}>NYAY-JUSTIS</div>
          <div style={{ fontSize: 13 }}>Judicial Priority Scheduling Initiative</div>
        </div>
      </div>
      <div style={{ flex: 1, background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 40 }}>
        <h1 style={{ fontSize: '5rem', fontWeight: 800, color: 'white', margin: 0, textShadow: '2px 2px 8px rgba(0,0,0,0.5)' }}>Nyay</h1>
        <p style={{ color: '#94a3b8', fontSize: '1.1rem', marginBottom: 8 }}>Judicial Priority Scheduling Initiative</p>
        <p style={{ color: C.gold, letterSpacing: 4, fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', marginBottom: 50 }}>Powered by JUSTIS Engine v2.0</p>
        <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap', justifyContent: 'center' }}>
          {[
            { role: 'admin', label: 'Admin', color: C.gold, textColor: C.primary },
            { role: 'judge', label: 'Judge', color: 'rgba(255,255,255,0.1)', textColor: 'white', border: `1px solid ${C.gold}` },
            { role: 'lawyer', label: 'Advocate', color: 'rgba(255,255,255,0.1)', textColor: 'white', border: `1px solid ${C.gold}` },
          ].map(({ role, label, color, textColor, border }) => (
            <button key={role} onClick={() => nav(`/login/${role}`)}
              style={{ background: color, color: textColor, padding: '14px 32px', borderRadius: 8, border: border || 'none', cursor: 'pointer', fontWeight: 700, fontSize: 16 }}>
              {label}
            </button>
          ))}
        </div>
        <p style={{ position: 'absolute', bottom: 20, color: '#64748b', fontSize: 12, textAlign: 'center' }}>
          System Disclaimer: NYAY-JUSTIS assists judicial scheduling. Final authority rests with the Honorable Court.
        </p>
      </div>
    </div>
  );
}
