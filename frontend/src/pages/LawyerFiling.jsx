import { useState } from 'react';

import Header from '../components/Header';
import { createCase, runNLP, runOCR } from '../services/api';

const C = { primary: '#0f172a', gold: '#d4af37', bg: '#f1f5f9', border: '#e2e8f0' };
const card = { background: 'white', padding: '28px', borderRadius: '12px', border: `1px solid ${C.border}`, boxShadow: '0 2px 8px rgba(0,0,0,0.04)' };
const inp = { width: '100%', padding: '11px', marginTop: '5px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px', outline: 'none', boxSizing: 'border-box' };

export default function LawyerFiling() {
  const [step, setStep] = useState(1);
  const [file, setFile] = useState(null);
  const [ocrText, setOcrText] = useState('');
  const [ocrError, setOcrError] = useState('');
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [form, setForm] = useState({
    case_id_number: '',
    citizen_username: '',
    primary_case_nature: 'Civil',
    procedural_stage: 'Pre-Trial',
    custody_status: 'None',
    immediate_risk: 'None',
    financial_stake: false,
    estimated_severity: 'Low',
    petitioner: '',
    respondent: '',
    under_acts: '',
    under_sections: '',
    is_undertrial: false,
    days_in_custody: 0,
  });

  const handleOCR = async () => {
    if (!file) {
      alert('Select a file first.');
      return;
    }

    setLoading(true);
    setOcrError('');
    try {
      const r = await runOCR(file);
      setOcrText(r.data.text);
      setStep(2);
    } catch (err) {
      setOcrError(err.response?.data?.detail || 'OCR failed. Continue with manual entry.');
    }
    setLoading(false);
  };

  const handleNLP = async () => {
    setLoading(true);
    try {
      const r = await runNLP(ocrText);
      setForm(f => ({ ...f, ...r.data.fields }));
      setConfidence(r.data.confidence);
      setStep(3);
    } catch {
      alert('NLP parsing failed.');
    }
    setLoading(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createCase(form);
    setSubmitted(true);
  };

  const handleManualEntry = () => {
    setConfidence(null);
    setStep(3);
  };

  const StepBar = () => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', background: 'white', padding: '18px 28px', borderRadius: '10px', border: `1px solid ${C.border}`, marginBottom: '24px' }}>
      {[['1', 'Upload'], ['2', 'OCR Extract'], ['3', 'Review + Submit']].map(([n, label], idx) => (
        <div key={n} style={{ display: 'contents' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: step >= Number(n) ? C.primary : '#94a3b8', fontWeight: step >= Number(n) ? '700' : '400', fontSize: '14px' }}>
            <div style={{ width: 26, height: 26, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '12px', fontWeight: '700', background: step > Number(n) ? '#10b981' : step === Number(n) ? C.primary : '#e2e8f0', color: step >= Number(n) ? 'white' : '#94a3b8' }}>
              {step > Number(n) ? 'OK' : n}
            </div>
            {label}
          </div>
          {idx < 2 && <div style={{ flex: 1, height: 2, background: step > Number(n) ? '#10b981' : '#e2e8f0', borderRadius: 2 }} />}
        </div>
      ))}
    </div>
  );

  if (submitted) {
    return (
      <div style={{ minHeight: '100vh', background: C.bg }}>
        <Header title="Smart E-Filing Portal" />
        <div style={{ maxWidth: '560px', margin: '80px auto', padding: '0 20px', textAlign: 'center' }}>
          <div style={card}>
            <div style={{ fontSize: '26px', marginBottom: '16px', fontWeight: '700', color: '#065f46' }}>Case Filed Successfully</div>
            <p style={{ color: '#64748b', marginTop: '8px' }}>Submitted to the JUSTIS priority queue for scoring and scheduling review.</p>
            <div style={{ marginTop: '20px', padding: '14px', background: '#f0fdf4', borderRadius: '8px', border: '1px solid #bbf7d0' }}>
              <strong style={{ color: '#065f46' }}>CNR: {form.case_id_number}</strong>
            </div>
            <button onClick={() => { setStep(1); setFile(null); setOcrText(''); setOcrError(''); setConfidence(null); setSubmitted(false); }} style={{ background: C.gold, color: C.primary, padding: '12px 28px', borderRadius: '8px', border: 'none', fontWeight: '700', cursor: 'pointer', marginTop: '20px' }}>
              File Another Case
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', background: C.bg }}>
      <Header title="Smart E-Filing Portal" />
      <div style={{ maxWidth: '860px', margin: '0 auto', padding: '36px 20px' }}>
        <StepBar />

        {step === 1 && (
          <div style={card}>
            <h3 style={{ color: C.primary, marginBottom: '6px' }}>Upload Case Document</h3>
            <p style={{ color: '#64748b', fontSize: '13px', marginBottom: '22px' }}>Upload a scanned FIR, petition, or court order. If OCR fails, continue with manual entry.</p>
            <div style={{ border: '2px dashed #cbd5e1', borderRadius: '10px', padding: '48px', textAlign: 'center', background: '#f8fafc', cursor: 'pointer' }} onClick={() => document.getElementById('file-in').click()} onDragOver={e => e.preventDefault()} onDrop={e => { e.preventDefault(); setFile(e.dataTransfer.files[0]); }}>
              <div style={{ fontSize: '18px', marginBottom: '10px', fontWeight: '700', color: C.primary }}>Document Upload</div>
              <p style={{ color: C.primary, fontWeight: '600', margin: 0 }}>{file ? file.name : 'Click or drag and drop'}</p>
              <p style={{ color: '#94a3b8', fontSize: '12px', marginTop: '6px' }}>JPG, PNG, PDF supported</p>
              <input id="file-in" type="file" accept="image/*,.pdf" style={{ display: 'none' }} onChange={e => setFile(e.target.files[0])} />
            </div>
            {ocrError && (
              <div style={{ marginTop: '18px', padding: '12px 14px', background: '#fef2f2', borderRadius: '8px', border: '1px solid #fecaca', color: '#991b1b', fontSize: '13px' }}>
                {ocrError}
              </div>
            )}
            <div style={{ textAlign: 'right', marginTop: '22px' }}>
              <button onClick={handleManualEntry} type="button" style={{ background: 'transparent', color: C.primary, padding: '12px 20px', borderRadius: '6px', border: '1px solid #cbd5e1', fontWeight: '600', cursor: 'pointer', marginRight: '10px' }}>
                Enter Manually
              </button>
              <button onClick={handleOCR} disabled={loading} type="button" style={{ background: C.primary, color: 'white', padding: '12px 24px', borderRadius: '6px', border: `1px solid ${C.gold}`, fontWeight: '600', cursor: 'pointer', opacity: loading ? 0.7 : 1 }}>
                {loading ? 'Extracting...' : 'Run OCR'}
              </button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div style={card}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
              <div>
                <h3 style={{ color: C.primary, margin: 0 }}>Extracted Text</h3>
              </div>
              <button onClick={() => setStep(1)} style={{ background: 'none', border: '1px solid #cbd5e1', color: '#64748b', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer', fontSize: '13px' }}>Re-upload</button>
            </div>
            <textarea value={ocrText} onChange={e => setOcrText(e.target.value)} style={{ width: '100%', height: '260px', padding: '14px', borderRadius: '8px', border: '1px solid #e2e8f0', fontFamily: 'monospace', fontSize: '13px', lineHeight: 1.7, background: '#f8fafc', resize: 'vertical', boxSizing: 'border-box' }} />
            <p style={{ color: '#94a3b8', fontSize: '12px', marginTop: '6px' }}>Edit the text above before parsing if needed.</p>
            <div style={{ textAlign: 'right', marginTop: '18px' }}>
              <button onClick={handleNLP} disabled={loading} type="button" style={{ background: C.gold, color: C.primary, padding: '12px 24px', borderRadius: '6px', border: 'none', fontWeight: '700', cursor: 'pointer', opacity: loading ? 0.7 : 1 }}>
                {loading ? 'Parsing...' : 'Parse with NLP'}
              </button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div style={card}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '22px', padding: '14px', background: '#f0fdf4', borderRadius: '8px', border: '1px solid #bbf7d0' }}>
              <div>
                <strong style={{ color: '#065f46', fontSize: '14px' }}>{confidence === null ? 'Manual Entry' : 'NLP Extraction Complete'}</strong>
                <p style={{ color: '#16a34a', fontSize: '12px', margin: '3px 0 0 0' }}>Review the filing fields before submission.</p>
              </div>
              <div style={{ textAlign: 'center', minWidth: '72px' }}>
                <div style={{ fontSize: '22px', fontWeight: '800', color: confidence === null ? C.primary : confidence >= 75 ? '#16a34a' : '#d97706' }}>
                  {confidence === null ? 'Manual' : `${confidence}%`}
                </div>
                <div style={{ fontSize: '10px', color: '#64748b', textTransform: 'uppercase', letterSpacing: '1px' }}>Mode</div>
              </div>
            </div>

            <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              {[
                ['Case ID *', 'case_id_number', 'text', true],
                ['Citizen Username *', 'citizen_username', 'text', true],
                ['Petitioner', 'petitioner', 'text', false],
                ['Respondent', 'respondent', 'text', false],
                ['Under Acts', 'under_acts', 'text', false],
                ['Under Sections', 'under_sections', 'text', false],
              ].map(([label, key, type, required]) => (
                <div key={key}>
                  <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>{label}</label>
                  <input type={type} required={required} value={form[key]} onChange={e => setForm({ ...form, [key]: e.target.value })} style={{ ...inp, borderColor: form[key] ? '#10b981' : '#cbd5e1' }} />
                </div>
              ))}

              {[
                ['Case Nature', 'primary_case_nature', ['Criminal', 'Civil']],
                ['Stage', 'procedural_stage', ['Pre-Trial', 'Framing of Charges', 'Evidence', 'Arguments', 'Active Trial', 'Sentencing']],
                ['Custody', 'custody_status', ['None', 'Remand', 'Bail Denied']],
                ['Immediate Risk', 'immediate_risk', ['None', 'Flight Risk', 'Threat to Life', 'Loss of Livelihood']],
                ['Severity', 'estimated_severity', ['Low', 'Medium', 'High']],
              ].map(([label, key, opts]) => (
                <div key={key}>
                  <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>{label}</label>
                  <select value={form[key]} onChange={e => setForm({ ...form, [key]: e.target.value })} style={{ ...inp, borderColor: '#10b981' }}>
                    {opts.map(o => <option key={o}>{o}</option>)}
                  </select>
                </div>
              ))}

              <div style={{ gridColumn: '1/-1', background: '#f8fafc', padding: '14px', borderRadius: '8px', border: '1px dashed #cbd5e1', display: 'flex', gap: '10px', alignItems: 'center' }}>
                <input type="checkbox" checked={form.financial_stake} onChange={e => setForm({ ...form, financial_stake: e.target.checked })} style={{ width: 18, height: 18, cursor: 'pointer' }} />
                <label style={{ fontWeight: '600', fontSize: '14px', color: '#334155' }}>High Financial / Property Stake</label>
              </div>

              <div style={{ gridColumn: '1/-1', background: '#f8fafc', padding: '14px', borderRadius: '8px', border: '1px dashed #f59e0b', display: 'flex', gap: '10px', alignItems: 'center' }}>
                <input type="checkbox" checked={form.is_undertrial} onChange={e => setForm({ ...form, is_undertrial: e.target.checked })} style={{ width: 18, height: 18, cursor: 'pointer' }} />
                <label style={{ fontWeight: '600', fontSize: '14px', color: '#92400e' }}>Accused is Undertrial Prisoner</label>
                {form.is_undertrial && (
                  <input type="number" placeholder="Days in custody" value={form.days_in_custody} onChange={e => setForm({ ...form, days_in_custody: Number(e.target.value) })} style={{ ...inp, marginTop: 0 }} />
                )}
              </div>

              <div style={{ gridColumn: '1/-1', display: 'flex', justifyContent: 'flex-end', marginTop: '10px' }}>
                <button type="submit" style={{ background: C.primary, color: 'white', padding: '12px 26px', borderRadius: '8px', border: 'none', fontWeight: '700', cursor: 'pointer' }}>
                  Submit Case
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
