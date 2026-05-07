import { useState } from 'react';

import Header from '../components/Header';
import { createCase, runNLP, runOCR } from '../services/api';

const C = { primary: '#0f172a', gold: '#d4af37', bg: '#f1f5f9', border: '#e2e8f0' };
const card = { background: 'white', padding: '28px', borderRadius: '12px', border: `1px solid ${C.border}`, boxShadow: '0 2px 8px rgba(0,0,0,0.04)' };
const inp = { width: '100%', padding: '11px', marginTop: '5px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px', outline: 'none', boxSizing: 'border-box' };
const REQUIRED_FIELDS = ['case_id_number', 'citizen_username'];
const FIELD_LABELS = {
  case_id_number: 'Case ID',
  citizen_username: 'Citizen Username',
  petitioner: 'Petitioner',
  respondent: 'Respondent',
  under_acts: 'Under Acts',
  under_sections: 'Under Sections',
  primary_case_nature: 'Case Nature',
  procedural_stage: 'Stage',
  custody_status: 'Custody',
  immediate_risk: 'Immediate Risk',
  estimated_severity: 'Severity',
  financial_stake: 'Financial Stake',
  is_undertrial: 'Undertrial Status',
  days_in_custody: 'Days In Custody',
};

export default function LawyerFiling() {
  const [step, setStep] = useState(1);
  const [file, setFile] = useState(null);
  const [ocrText, setOcrText] = useState('');
  const [ocrError, setOcrError] = useState('');
  const [confidence, setConfidence] = useState(null);
  const [extractionMeta, setExtractionMeta] = useState(null);
  const [reviewTouched, setReviewTouched] = useState({});
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
      setExtractionMeta(null);
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
      setReviewTouched({});
      setConfidence(r.data.confidence);
      setExtractionMeta({
        provider: r.data.provider || 'unknown',
        fieldsExtracted: r.data.fields_extracted || 0,
        missingFields: r.data.missing_fields || [],
        warnings: r.data.warnings || [],
        language: r.data.language || 'unknown',
        summary: r.data.summary || '',
      });
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
    setExtractionMeta(null);
    setReviewTouched({});
    setStep(3);
  };

  const updateField = (key, value) => {
    setForm(current => ({ ...current, [key]: value }));
    setReviewTouched(current => ({ ...current, [key]: true }));
  };

  const aiMissingFields = extractionMeta?.missingFields || [];
  const requiredAttentionFields = REQUIRED_FIELDS.filter((key) => !String(form[key] ?? '').trim());
  const attentionFields = Array.from(new Set([...aiMissingFields, ...requiredAttentionFields]));
  const reviewedCount = Object.keys(reviewTouched).length;
  const getFieldTone = (key) => {
    if (reviewTouched[key]) {
      return {
        borderColor: '#2563eb',
        background: '#eff6ff',
        label: 'Reviewed manually',
        textColor: '#1d4ed8',
      };
    }
    if (attentionFields.includes(key)) {
      return {
        borderColor: '#f59e0b',
        background: '#fff7ed',
        label: 'Needs review',
        textColor: '#b45309',
      };
    }
    if (confidence !== null && String(form[key] ?? '').trim()) {
      return {
        borderColor: '#10b981',
        background: '#f0fdf4',
        label: 'AI filled',
        textColor: '#047857',
      };
    }
    return {
      borderColor: '#cbd5e1',
      background: 'white',
      label: 'Waiting for input',
      textColor: '#64748b',
    };
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
            <button onClick={() => { setStep(1); setFile(null); setOcrText(''); setOcrError(''); setConfidence(null); setExtractionMeta(null); setReviewTouched({}); setSubmitted(false); }} style={{ background: C.gold, color: C.primary, padding: '12px 28px', borderRadius: '8px', border: 'none', fontWeight: '700', cursor: 'pointer', marginTop: '20px' }}>
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
                {loading ? 'Extracting fields...' : 'Extract Fields with AI'}
              </button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div style={card}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '22px', padding: '14px', background: '#f0fdf4', borderRadius: '8px', border: '1px solid #bbf7d0' }}>
              <div>
                <strong style={{ color: '#065f46', fontSize: '14px' }}>{confidence === null ? 'Manual Entry' : 'AI Extraction Complete'}</strong>
                <p style={{ color: '#16a34a', fontSize: '12px', margin: '3px 0 0 0' }}>Review the filing fields before submission.</p>
              </div>
              <div style={{ textAlign: 'center', minWidth: '72px' }}>
                <div style={{ fontSize: '22px', fontWeight: '800', color: confidence === null ? C.primary : confidence >= 75 ? '#16a34a' : '#d97706' }}>
                  {confidence === null ? 'Manual' : `${confidence}%`}
                </div>
                <div style={{ fontSize: '10px', color: '#64748b', textTransform: 'uppercase', letterSpacing: '1px' }}>Mode</div>
              </div>
            </div>

            {extractionMeta && (
              <div style={{ marginBottom: '18px', display: 'grid', gap: '10px' }}>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '10px' }}>
                  {[
                    ['Provider', extractionMeta.provider],
                    ['Language', extractionMeta.language],
                    ['Fields Extracted', extractionMeta.fieldsExtracted],
                    ['Needs Review', attentionFields.length],
                    ['Reviewed', reviewedCount],
                  ].map(([label, value]) => (
                    <div key={label} style={{ background: '#eff6ff', padding: '12px 14px', borderRadius: '8px', border: '1px solid #bfdbfe' }}>
                      <div style={{ fontSize: '12px', color: '#1d4ed8', fontWeight: '700' }}>{label}</div>
                      <div style={{ fontSize: '13px', color: '#1e3a8a', marginTop: '4px' }}>{value}</div>
                    </div>
                  ))}
                </div>
                {extractionMeta.summary && (
                  <div style={{ background: '#f8fafc', padding: '12px 14px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                    <div style={{ fontSize: '12px', color: '#475569', fontWeight: '700' }}>Summary</div>
                    <div style={{ fontSize: '13px', color: '#1e293b', marginTop: '4px' }}>{extractionMeta.summary}</div>
                  </div>
                )}
                {extractionMeta.missingFields.length > 0 && (
                  <div style={{ background: '#fff7ed', padding: '12px 14px', borderRadius: '8px', border: '1px solid #fdba74' }}>
                    <div style={{ fontSize: '12px', color: '#c2410c', fontWeight: '700' }}>Missing Fields</div>
                    <div style={{ fontSize: '13px', color: '#9a3412', marginTop: '4px' }}>{extractionMeta.missingFields.join(', ')}</div>
                  </div>
                )}
                {attentionFields.length > 0 && (
                  <div style={{ background: '#fffbeb', padding: '12px 14px', borderRadius: '8px', border: '1px solid #fcd34d' }}>
                    <div style={{ fontSize: '12px', color: '#b45309', fontWeight: '700' }}>Review Checklist</div>
                    <div style={{ fontSize: '13px', color: '#92400e', marginTop: '4px' }}>
                      {attentionFields.map((field) => FIELD_LABELS[field] || field).join(', ')}
                    </div>
                  </div>
                )}
                {extractionMeta.warnings.length > 0 && (
                  <div style={{ background: '#fef2f2', padding: '12px 14px', borderRadius: '8px', border: '1px solid #fecaca' }}>
                    <div style={{ fontSize: '12px', color: '#b91c1c', fontWeight: '700' }}>Warnings</div>
                    <div style={{ fontSize: '13px', color: '#991b1b', marginTop: '4px' }}>{extractionMeta.warnings.join(' ')}</div>
                  </div>
                )}
              </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.2fr) minmax(280px, 0.8fr)', gap: '20px', alignItems: 'start' }}>
              <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              {[
                ['Case ID *', 'case_id_number', 'text', true],
                ['Citizen Username *', 'citizen_username', 'text', true],
                ['Petitioner', 'petitioner', 'text', false],
                ['Respondent', 'respondent', 'text', false],
                ['Under Acts', 'under_acts', 'text', false],
                ['Under Sections', 'under_sections', 'text', false],
              ].map(([label, key, type, required]) => {
                const tone = getFieldTone(key);
                return (
                <div key={key}>
                  <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>{label}</label>
                  <input type={type} required={required} value={form[key]} onChange={e => updateField(key, e.target.value)} style={{ ...inp, borderColor: tone.borderColor, background: tone.background }} />
                  <div style={{ fontSize: '11px', color: tone.textColor, marginTop: '6px', fontWeight: '600' }}>{tone.label}</div>
                </div>
              )})}

              {[
                ['Case Nature', 'primary_case_nature', ['Criminal', 'Civil']],
                ['Stage', 'procedural_stage', ['Pre-Trial', 'Framing of Charges', 'Evidence', 'Arguments', 'Active Trial', 'Sentencing']],
                ['Custody', 'custody_status', ['None', 'Remand', 'Bail Denied']],
                ['Immediate Risk', 'immediate_risk', ['None', 'Flight Risk', 'Threat to Life', 'Loss of Livelihood']],
                ['Severity', 'estimated_severity', ['Low', 'Medium', 'High']],
              ].map(([label, key, opts]) => {
                const tone = getFieldTone(key);
                return (
                <div key={key}>
                  <label style={{ fontWeight: '600', fontSize: '13px', color: '#334155' }}>{label}</label>
                  <select value={form[key]} onChange={e => updateField(key, e.target.value)} style={{ ...inp, borderColor: tone.borderColor, background: tone.background }}>
                    {opts.map(o => <option key={o}>{o}</option>)}
                  </select>
                  <div style={{ fontSize: '11px', color: tone.textColor, marginTop: '6px', fontWeight: '600' }}>{tone.label}</div>
                </div>
              )})}

              <div style={{ gridColumn: '1/-1', background: '#f8fafc', padding: '14px', borderRadius: '8px', border: '1px dashed #cbd5e1', display: 'flex', gap: '10px', alignItems: 'center' }}>
                <input type="checkbox" checked={form.financial_stake} onChange={e => updateField('financial_stake', e.target.checked)} style={{ width: 18, height: 18, cursor: 'pointer' }} />
                <label style={{ fontWeight: '600', fontSize: '14px', color: '#334155' }}>High Financial / Property Stake</label>
              </div>

              <div style={{ gridColumn: '1/-1', background: '#f8fafc', padding: '14px', borderRadius: '8px', border: '1px dashed #f59e0b', display: 'flex', gap: '10px', alignItems: 'center' }}>
                <input type="checkbox" checked={form.is_undertrial} onChange={e => updateField('is_undertrial', e.target.checked)} style={{ width: 18, height: 18, cursor: 'pointer' }} />
                <label style={{ fontWeight: '600', fontSize: '14px', color: '#92400e' }}>Accused is Undertrial Prisoner</label>
                {form.is_undertrial && (
                  <input type="number" placeholder="Days in custody" value={form.days_in_custody} onChange={e => updateField('days_in_custody', Number(e.target.value))} style={{ ...inp, marginTop: 0, borderColor: getFieldTone('days_in_custody').borderColor, background: getFieldTone('days_in_custody').background }} />
                )}
              </div>

              <div style={{ gridColumn: '1/-1', display: 'flex', justifyContent: 'flex-end', marginTop: '10px' }}>
                <button type="submit" style={{ background: C.primary, color: 'white', padding: '12px 26px', borderRadius: '8px', border: 'none', fontWeight: '700', cursor: 'pointer' }}>
                  Submit Case
                </button>
              </div>
              </form>

              <aside style={{ background: '#f8fafc', borderRadius: '12px', border: '1px solid #e2e8f0', padding: '18px', position: 'sticky', top: '24px' }}>
                <div style={{ fontSize: '15px', fontWeight: '700', color: '#0f172a', marginBottom: '8px' }}>Source Text Reference</div>
                <p style={{ fontSize: '12px', color: '#64748b', marginTop: 0, marginBottom: '12px' }}>
                  Keep this beside the form while correcting missing or uncertain values.
                </p>
                <textarea
                  value={ocrText}
                  onChange={e => setOcrText(e.target.value)}
                  style={{ width: '100%', minHeight: '360px', padding: '12px', borderRadius: '8px', border: '1px solid #cbd5e1', fontFamily: 'monospace', fontSize: '12px', lineHeight: 1.6, background: 'white', boxSizing: 'border-box', resize: 'vertical' }}
                />
              </aside>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
