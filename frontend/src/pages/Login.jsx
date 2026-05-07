import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { login } from '../services/api';

const LABELS = {
  judge: 'Judicial Authentication',
  lawyer: 'Advocate Authentication',
  citizen: 'Citizen Portal Access',
};

export default function Login() {
  const { role } = useParams();
  const nav = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const r = await login(username, password);
      if (r.data.role !== role) {
        setError(`This account does not have ${role} access.`);
        setLoading(false);
        return;
      }

      sessionStorage.setItem('nyay_role', r.data.role);
      sessionStorage.setItem('nyay_name', r.data.name || '');
      sessionStorage.setItem('nyay_username', r.data.username || username);
      nav(`/${role}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Authentication failed. Check your credentials.');
    }

    setLoading(false);
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a, #1e3a5f)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, padding: 40, width: 380, backdropFilter: 'blur(10px)' }}>
        <h3 style={{ color: 'white', textAlign: 'center', marginBottom: 30, fontWeight: 400 }}>{LABELS[role]}</h3>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 15 }}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={e => setUsername(e.target.value)}
            style={{ padding: 14, borderRadius: 8, border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(15,23,42,0.6)', color: 'white', fontSize: 16 }}
            autoFocus
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{ padding: 14, borderRadius: 8, border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(15,23,42,0.6)', color: 'white', fontSize: 16 }}
          />
          {error && <p style={{ color: '#ef4444', textAlign: 'center', margin: 0, fontSize: 13 }}>{error}</p>}
          <button type="submit" disabled={loading} style={{ background: '#d4af37', color: '#0f172a', padding: 14, borderRadius: 8, border: 'none', fontWeight: 700, cursor: 'pointer', opacity: loading ? 0.7 : 1 }}>
            {loading ? 'Verifying...' : 'Verify Identity'}
          </button>
        </form>
        <button onClick={() => nav('/accounts/new')} style={{ background: 'none', border: 'none', color: '#d4af37', width: '100%', marginTop: 14, cursor: 'pointer', textDecoration: 'underline' }}>
          Create or request a new account
        </button>
        <button onClick={() => nav('/')} style={{ background: 'none', border: 'none', color: '#64748b', width: '100%', marginTop: 20, cursor: 'pointer', textDecoration: 'underline' }}>
          Return to Portal
        </button>
      </div>
    </div>
  );
}
