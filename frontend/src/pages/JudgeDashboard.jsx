import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Header from '../components/Header';
import { adjournCase, disposeCase, getAnalytics, getCases } from '../services/api';

const C = { primary: '#0f172a', gold: '#d4af37', bg: '#f1f5f9', border: '#e2e8f0' };
const card = { background: 'white', padding: '24px', borderRadius: '12px', border: `1px solid ${C.border}`, boxShadow: '0 2px 8px rgba(0,0,0,0.04)' };

export default function JudgeDashboard() {
  const nav = useNavigate();
  const [cases, setCases] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchAll = async () => {
    try {
      const [cRes, aRes] = await Promise.all([getCases(), getAnalytics()]);
      setCases(cRes.data);
      setAnalytics(aRes.data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchAll();
  }, []);

  const handleAdjourn = async (caseId) => {
    const reason = window.prompt('Reason for adjournment:') || 'Not specified';
    await adjournCase(caseId, reason);
    fetchAll();
  };

  const handleDispose = async (caseId) => {
    await disposeCase(caseId);
    fetchAll();
  };

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', background: C.bg }}>
        <Header title="Judicial Workbench" />
        <div style={{ textAlign: 'center', padding: '100px', color: '#64748b' }}>Loading cause list...</div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', background: C.bg }}>
      <Header title="Judicial Workbench" />
      <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '40px 20px' }}>
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '16px' }}>
          <button onClick={() => nav('/accounts/new')} style={{ background: C.primary, color: 'white', padding: '11px 16px', borderRadius: '8px', border: 'none', fontWeight: '700', cursor: 'pointer' }}>
            Create Account
          </button>
        </div>
        {analytics && (
          <div style={{ display: 'flex', gap: '16px', marginBottom: '30px', flexWrap: 'wrap' }}>
            {[
              { label: 'Total Cases', value: analytics.total_cases, color: C.primary },
              { label: 'Critical (>=200)', value: analytics.critical_cases, color: '#ef4444' },
              { label: 'Omega Flags', value: analytics.omega_cases, color: '#f59e0b' },
              { label: 'Undertrial', value: analytics.undertrial_cases, color: '#8b5cf6' },
              { label: 'Avg Age (days)', value: analytics.avg_age_days, color: '#0ea5e9' },
              { label: 'Over 5 Years', value: analytics.cases_over_5_years, color: '#dc2626' },
            ].map(({ label, value, color }) => (
              <div key={label} style={{ ...card, flex: 1, minWidth: '130px', textAlign: 'center', padding: '16px' }}>
                <div style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase', fontWeight: '700', letterSpacing: '1px' }}>{label}</div>
                <div style={{ fontSize: '28px', fontWeight: '800', color, marginTop: '6px' }}>{value}</div>
              </div>
            ))}
          </div>
        )}

        <div style={card}>
          <div style={{ borderBottom: `2px solid ${C.border}`, paddingBottom: '15px', marginBottom: '25px' }}>
            <h3 style={{ color: C.primary, margin: 0, fontSize: '22px' }}>AI-Prioritized Cause List</h3>
            <p style={{ color: '#64748b', fontSize: '13px', margin: '5px 0 0 0' }}>
              Ranked by JUSTIS Engine using case age, adjournments, vulnerability, and stage.
            </p>
          </div>

          {cases.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px', background: '#f8fafc', borderRadius: '8px', border: '1px dashed #cbd5e1' }}>
              <div style={{ fontSize: '24px', fontWeight: '700', color: C.primary }}>Docket Cleared</div>
            </div>
          ) : cases.map((c, i) => (
            <div
              key={c.id}
              style={{
                borderLeft: `6px solid ${c.omega ? '#f59e0b' : c.primary_case_nature === 'Criminal' ? '#ef4444' : '#3b82f6'}`,
                padding: '20px',
                margin: '16px 0',
                background: '#fff',
                borderRadius: '0 10px 10px 0',
                border: `1px solid ${C.border}`,
                boxShadow: '0 2px 6px rgba(0,0,0,0.03)',
              }}
            >
              {c.section_436a?.eligible && (
                <div style={{ background: '#fef2f2', border: '2px solid #ef4444', borderRadius: '8px', padding: '10px 14px', marginBottom: '12px' }}>
                  <strong style={{ color: '#b91c1c', fontSize: '13px' }}>Section 436A Alert</strong>
                  <p style={{ color: '#7f1d1d', fontSize: '12px', margin: '4px 0 0 0' }}>{c.section_436a.message}</p>
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '10px' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                    <strong style={{ fontSize: '17px', color: C.primary }}>#{i + 1} | {c.case_id_number}</strong>
                    <span style={{ background: c.primary_case_nature === 'Criminal' ? '#fee2e2' : '#dbeafe', color: c.primary_case_nature === 'Criminal' ? '#b91c1c' : '#1d4ed8', padding: '3px 10px', borderRadius: '20px', fontSize: '11px', fontWeight: '800', textTransform: 'uppercase' }}>
                      {c.primary_case_nature}
                    </span>
                    {c.omega && <span style={{ background: '#fef3c7', color: '#92400e', padding: '3px 10px', borderRadius: '20px', fontSize: '11px', fontWeight: '800' }}>Omega</span>}
                    {c.is_undertrial && <span style={{ background: '#f3e8ff', color: '#6b21a8', padding: '3px 10px', borderRadius: '20px', fontSize: '11px', fontWeight: '800' }}>Undertrial</span>}
                    <span style={{ background: '#ecfeff', color: '#155e75', padding: '3px 10px', borderRadius: '20px', fontSize: '11px', fontWeight: '800' }}>{c.status}</span>
                  </div>
                  <div style={{ fontSize: '13px', color: '#64748b', marginTop: '5px' }}>
                    {c.petitioner} vs {c.respondent}
                  </div>
                </div>
                <div style={{ background: c.score >= 200 ? '#ef4444' : c.score >= 80 ? '#f59e0b' : C.primary, color: 'white', padding: '8px 16px', borderRadius: '8px', fontWeight: '800', fontSize: '16px', textAlign: 'center', minWidth: '100px' }}>
                  <div>P = {c.score}</div>
                  <div style={{ fontSize: '10px', fontWeight: '400', opacity: 0.85 }}>{c.band}</div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '10px' }}>
                <span style={{ background: '#f1f5f9', padding: '4px 10px', borderRadius: '6px', fontSize: '12px', color: '#475569', fontWeight: '600' }}>Stage: {c.procedural_stage}</span>
                {c.under_sections && c.under_sections !== '-' && (
                  <span style={{ background: '#fef9c3', padding: '4px 10px', borderRadius: '6px', fontSize: '12px', color: '#713f12', fontWeight: '600' }}>Sections: {c.under_sections}</span>
                )}
                <span style={{ background: '#f0fdf4', padding: '4px 10px', borderRadius: '6px', fontSize: '12px', color: '#166534', fontWeight: '600' }}>Filed: {c.filing_date}</span>
              </div>

              <div style={{ background: '#f8fafc', padding: '12px 16px', borderRadius: '8px', border: '1px solid #e2e8f0', marginTop: '12px' }}>
                <div style={{ fontSize: '10px', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '1.2px', fontWeight: '700' }}>JUSTIS Score Breakdown</div>
                <div style={{ fontSize: '13px', color: '#1e293b', marginTop: '6px', fontFamily: 'monospace' }}>{c.explanation}</div>
              </div>

              <div style={{ display: 'flex', gap: '10px', marginTop: '14px', paddingTop: '14px', borderTop: '1px solid #f1f5f9' }}>
                <button onClick={() => handleDispose(c.id)} style={{ background: '#10b981', color: 'white', padding: '9px 18px', borderRadius: '6px', border: 'none', cursor: 'pointer', fontWeight: '700', fontSize: '13px' }}>
                  Dispose
                </button>
                <button onClick={() => handleAdjourn(c.id)} style={{ background: 'transparent', color: '#64748b', padding: '9px 18px', borderRadius: '6px', border: '1px solid #cbd5e1', cursor: 'pointer', fontWeight: '600', fontSize: '13px' }}>
                  Adjourn (+F)
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
