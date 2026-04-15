import axios from 'axios';

const client = axios.create({ baseURL: import.meta.env.VITE_API_URL });

// Attach JWT to every request automatically
client.interceptors.request.use(config => {
  const token = localStorage.getItem('nyay_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auto-logout on 401
client.interceptors.response.use(
  r => r,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('nyay_token');
      localStorage.removeItem('nyay_role');
      window.location.href = '/';
    }
    return Promise.reject(err);
  }
);

export const login = (username, password) =>
  client.post('/auth/login', new URLSearchParams({ username, password }));

export const getCases = () => client.get('/cases');
export const createCase = (data) => client.post('/cases', data);
export const adjournCase = (id, reason) =>
  client.put(`/cases/${id}/adjourn`, null, { params: { reason } });
export const getAnalytics = () => client.get('/cases/analytics');
export const runOCR = (file) => {
  const fd = new FormData(); fd.append('file', file);
  return client.post('/ocr', fd);
};
export const runNLP = (text) => client.post('/ocr/extract', { text });
export const searchCases = (q) => client.get(`/citizen/search?q=${q}`);