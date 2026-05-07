import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Header from '../components/Header';
import { createUser, getCurrentUser } from '../services/api';

const C = { primary: '#0f172a', gold: '#d4af37', bg: '#f1f5f9', border: '#e2e8f0' };
const card = { background: 'white', padding: '28px', borderRadius: '12px', border: `1px solid ${C.border}`, boxShadow: '0 2px 8px rgba(0,0,0,0.04)' };
const inp = { width: '100%', padding: '11px', marginTop: '5px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px', outline: 'none', boxSizing: 'border-box' };

const INITIAL_FORM = {
  username: '',
  full_name: '',
  role: 'citizen',
  password: '',
  confirmPassword: '',
};

export default function CreateAccount() {
  const nav = useNavigate();
  const [loading, setLoading] = useState(true);
  const [canCreate, setCanCreate] = useState(false);
  const [form, setForm] = useState(INITIAL_FORM);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const response = await getCurrentUser();
        if (response.data.role === 'judge') {
          setCanCreate(true);
        }
      } catch {
        setCanCreate(false);
      }
      setLoading(false);
    };
    load();
  }, []);

  const updateField = (key, value) => {
    setForm((current) => ({ ...current, [key]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(null);

    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setSubmitting(true);
    try {
      const payload = {
        username: form.username.trim(),
        full_name: form.full_name.trim(),
        role: form.role,
        password: form.password,
      };
      const response = await createUser(payload);
      setSuccess(response.data);
      setForm(INITIAL_FORM);
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to create account.');
    }
    setSubmitting(false);
  };

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', background: C.bg }}>
        <Header title="Account Administration" />
        <div style={{ textAlign: 'center', padding: '100px', color: '#64748b' }}>Loading access controls...</div>
      </div>
    );
  }

  if (!canCreate) {
    return (
      <div style={{ minHeight: '100vh', background: C.bg }}>
        <Header title="Account Administration" />
        <div style={{ maxWidth: '720px', margin: '60px auto', padding: '0 20px' }}>
          <div style={card}>
            <h3 style={{ color: C.primary, marginTop: 0 }}>Judge Approval Required</h3>
            <p style={{ color: '#475569', lineHeight: 1.7 }}>
              Account creation is currently controlled from the judge or registry side so new users can be verified before receiving portal access.
            </p>
            <p style={{ color: '#64748b', lineHeight: 1.7 }}>
              Sign in with a judge account to create lawyer or citizen accounts, or return to the portal and authenticate with an existing account.
            </p>
            <div style={{ display: 'flex', gap: '12px', marginTop: '20px', flexWrap: 'wrap' }}>
              <button onClick={() => nav('/login/judge')} style={{ background: C.primary, color: 'white', padding: '12px 18px', borderRadius: '8px', border: 'none', fontWeight: '700', cursor: 'pointer' }}>
                Sign In As Judge
              </button>
              <button onClick={() => nav('/')} style={{ background: 'white', color: C.primary, padding: '12px 18px', borderRadius: '8px', border: `1px solid ${C.border}`, fontWeight: '700', cursor: 'pointer' }}>
                Return To Portal
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', background: C.bg }}>
      <Header title="Account Administration" />
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '40px 20px', display: 'grid', gridTemplateColumns: 'minmax(0, 1.1fr) minmax(280px, 0.9fr)', gap: '20px' }}>
        <div style={card}>
          <div style={{ marginBottom: '22px' }}>
            <h3 style={{ color: C.primary, margin: 0 }}>Create Verified Portal Account</h3>
            <p style={{ color: '#64748b', fontSize: '14px', marginTop: '6px' }}>
              Use this workflow to create citizen and lawyer access after identity checks are completed offline.
            </p>
          </div>

          <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '18px' }}>
            <div>
              <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>Role</label>
              <select value={form.role} onChange={(e) => updateField('role', e.target.value)} style={inp}>
                <option value="citizen">Citizen</option>
                <option value="lawyer">Lawyer</option>
                <option value="judge">Judge</option>
              </select>
            </div>
            <div>
              <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>Username</label>
              <input required value={form.username} onChange={(e) => updateField('username', e.target.value)} style={inp} placeholder="citizen_rahul" />
            </div>
            <div style={{ gridColumn: '1/-1' }}>
              <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>Full Name</label>
              <input required value={form.full_name} onChange={(e) => updateField('full_name', e.target.value)} style={inp} placeholder="Rahul Kumar" />
            </div>
            <div>
              <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>Temporary Password</label>
              <input required type="password" value={form.password} onChange={(e) => updateField('password', e.target.value)} style={inp} placeholder="Minimum 8 characters" />
            </div>
            <div>
              <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>Confirm Password</label>
              <input required type="password" value={form.confirmPassword} onChange={(e) => updateField('confirmPassword', e.target.value)} style={inp} placeholder="Repeat password" />
            </div>
            {error && (
              <div style={{ gridColumn: '1/-1', padding: '12px 14px', background: '#fef2f2', borderRadius: '8px', border: '1px solid #fecaca', color: '#991b1b', fontSize: '13px' }}>
                {error}
              </div>
            )}
            {success && (
              <div style={{ gridColumn: '1/-1', padding: '12px 14px', background: '#f0fdf4', borderRadius: '8px', border: '1px solid #bbf7d0', color: '#166534', fontSize: '13px' }}>
                Account created for <strong>{success.full_name}</strong> as <strong>{success.role}</strong> with username <strong>{success.username}</strong>.
              </div>
            )}
            <div style={{ gridColumn: '1/-1', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '8px', gap: '12px', flexWrap: 'wrap' }}>
              <button type="button" onClick={() => nav('/judge')} style={{ background: 'white', color: C.primary, padding: '12px 18px', borderRadius: '8px', border: `1px solid ${C.border}`, fontWeight: '700', cursor: 'pointer' }}>
                Back To Dashboard
              </button>
              <button type="submit" disabled={submitting} style={{ background: C.primary, color: 'white', padding: '12px 20px', borderRadius: '8px', border: 'none', fontWeight: '700', cursor: 'pointer', opacity: submitting ? 0.7 : 1 }}>
                {submitting ? 'Creating Account...' : 'Create Account'}
              </button>
            </div>
          </form>
        </div>

        <div style={{ ...card, background: '#fffdf5' }}>
          <h4 style={{ color: C.primary, marginTop: 0 }}>Operational Guidance</h4>
          <div style={{ display: 'grid', gap: '12px', fontSize: '13px', color: '#475569', lineHeight: 1.7 }}>
            <div>Use unique usernames tied to your court or registry process.</div>
            <div>Share temporary passwords through a verified offline channel, then require the user to change it after first login.</div>
            <div>Only create judge accounts for authorized internal users.</div>
            <div>Citizen self-signup is not enabled yet because identity verification and abuse controls are still missing.</div>
          </div>
        </div>
      </div>
    </div>
  );
}
