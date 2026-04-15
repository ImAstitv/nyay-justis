import { useNavigate } from 'react-router-dom';
const C = { primary: '#0f172a', gold: '#d4af37' };

export default function Header({ title }) {
  const nav = useNavigate();
  const logout = () => {
    localStorage.removeItem('nyay_token');
    localStorage.removeItem('nyay_role');
    nav('/');
  };
  return (
    <div style={{ background: C.primary, padding: '18px 50px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: `4px solid ${C.gold}` }}>
      <h2 style={{ color: 'white', margin: 0, fontSize: '20px' }}>
        ⚖️ न्याय <span style={{ color: C.gold, fontWeight: 400 }}>| {title}</span>
      </h2>
      <button onClick={logout} style={{ background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.3)', color: 'white', padding: '8px 16px', borderRadius: '6px', cursor: 'pointer' }}>
        Secure Logout
      </button>
    </div>
  );
}