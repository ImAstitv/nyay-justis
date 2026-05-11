import axios from 'axios';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      sessionStorage.removeItem('nyay_role');
      sessionStorage.removeItem('nyay_name');
      sessionStorage.removeItem('nyay_username');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const login = (username, password) =>
  client.post('/auth/login', new URLSearchParams({ username, password }));

export const logout = () => client.post('/auth/logout');
export const getCurrentUser = () => client.get('/auth/me');
export const createUser = (data) => client.post('/auth/users', data);
export const getUsers = () => client.get('/auth/users');
export const getCases = () => client.get('/cases');
export const createCase = (data) => client.post('/cases', data);
export const adjournCase = (id, reason) =>
  client.put(`/cases/${id}/adjourn`, null, { params: { reason } });
export const disposeCase = (id) => client.put(`/cases/${id}/dispose`);
export const getAnalytics = () => client.get('/cases/analytics');
export const runOCR = (file) => {
  const fd = new FormData();
  fd.append('file', file);
  return client.post('/ocr', fd);
};
export const runNLP = (text) => client.post('/ocr/extract', { text });
