import { useEffect, useState } from 'react';

import Header from '../components/Header';
import { createUser, getUsers } from '../services/api';

const C = { primary: '#0f172a', gold: '#d4af37', bg: '#f1f5f9', border: '#e2e8f0' };
const card = { background: 'white', padding: '28px', borderRadius: '12px', border: `1px solid ${C.border}`, boxShadow: '0 2px 8px rgba(0,0,0,0.04)' };
const inp = { width: '100%', padding: '11px', marginTop: '5px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px', outline: 'none', boxSizing: 'border-box' };

const INITIAL_FORM = {
  username: '',
  full_name: '',
  role: 'lawyer',
  password: '',
  confirmPassword: '',
};

export default function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState(INITIAL_FORM);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const loadUsers = async () => {
    try {
      const response = await getUsers();
      setUsers(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to load accounts.');
    }
    setLoading(false);
  };

  useEffect(() => {
    loadUsers();
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
      await loadUsers();
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to create account.');
    }
    setSubmitting(false);
  };

  return (
    <div style={{ minHeight: '100vh', background: C.bg }}>
      <Header title="Admin Panel" />
      <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '40px 20px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '22px' }}>
        <div style={card}>
          <div style={{ marginBottom: '22px' }}>
            <h3 style={{ color: C.primary, margin: 0 }}>Create Staff Account</h3>
            <p style={{ color: '#64748b', fontSize: '14px', marginTop: '6px' }}>
              Admins create and manage registry, judge, and advocate access.
            </p>
          </div>

          <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '18px' }}>
            <div>
              <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>Role</label>
              <select value={form.role} onChange={(e) => updateField('role', e.target.value)} style={inp}>
                <option value="lawyer">Lawyer</option>
                <option value="judge">Judge</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div>
              <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>Username</label>
              <input required value={form.username} onChange={(e) => updateField('username', e.target.value)} style={inp} placeholder="advocate_mishra" />
            </div>
            <div style={{ gridColumn: '1/-1' }}>
              <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>Full Name</label>
              <input required value={form.full_name} onChange={(e) => updateField('full_name', e.target.value)} style={inp} placeholder="Adv. Priya Mishra" />
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
                Account created for <strong>{success.full_name}</strong> as <strong>{success.role}</strong>.
              </div>
            )}
            <div style={{ gridColumn: '1/-1', display: 'flex', justifyContent: 'flex-end', marginTop: '8px' }}>
              <button type="submit" disabled={submitting} style={{ background: C.primary, color: 'white', padding: '12px 20px', borderRadius: '8px', border: 'none', fontWeight: '700', cursor: 'pointer', opacity: submitting ? 0.7 : 1 }}>
                {submitting ? 'Creating Account...' : 'Create Account'}
              </button>
            </div>
          </form>
        </div>

        <div style={card}>
          <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', alignItems: 'center', marginBottom: '18px' }}>
            <div>
              <h3 style={{ color: C.primary, margin: 0 }}>Account Roster</h3>
              <p style={{ color: '#64748b', fontSize: '13px', margin: '4px 0 0 0' }}>Current staff accounts with portal access.</p>
            </div>
            <button onClick={loadUsers} style={{ background: 'white', color: C.primary, padding: '10px 14px', borderRadius: '8px', border: `1px solid ${C.border}`, fontWeight: '700', cursor: 'pointer' }}>
              Refresh
            </button>
          </div>

          {loading ? (
            <div style={{ color: '#64748b', padding: '30px', textAlign: 'center' }}>Loading accounts...</div>
          ) : users.length === 0 ? (
            <div style={{ color: '#64748b', padding: '30px', textAlign: 'center', background: '#f8fafc', borderRadius: '8px' }}>No accounts found.</div>
          ) : (
            <div style={{ display: 'grid', gap: '10px' }}>
              {users.map((user) => (
                <div key={user.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '14px', padding: '14px', border: `1px solid ${C.border}`, borderRadius: '10px', background: '#f8fafc' }}>
                  <div>
                    <div style={{ color: C.primary, fontWeight: '800' }}>{user.full_name || user.username}</div>
                    <div style={{ color: '#64748b', fontSize: '12px', marginTop: '2px' }}>@{user.username}</div>
                  </div>
                  <span style={{ background: user.role === 'admin' ? C.primary : user.role === 'judge' ? '#fef3c7' : '#dbeafe', color: user.role === 'admin' ? 'white' : user.role === 'judge' ? '#92400e' : '#1d4ed8', padding: '6px 10px', borderRadius: '999px', fontSize: '11px', fontWeight: '800', textTransform: 'uppercase' }}>
                    {user.role}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
