import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Landing from './pages/Landing';
import Login from './pages/Login';
import JudgeDashboard from './pages/JudgeDashboard';
import LawyerFiling from './pages/LawyerFiling';
import CitizenPortal from './pages/CitizenPortal';

function ProtectedRoute({ children, allowedRole }) {
  const role = localStorage.getItem('nyay_role');
  const token = localStorage.getItem('nyay_token');
  if (!token || role !== allowedRole) return <Navigate to="/" />;
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login/:role" element={<Login />} />
        <Route path="/judge" element={
          <ProtectedRoute allowedRole="judge"><JudgeDashboard /></ProtectedRoute>
        } />
        <Route path="/lawyer" element={
          <ProtectedRoute allowedRole="lawyer"><LawyerFiling /></ProtectedRoute>
        } />
        <Route path="/citizen" element={
          <ProtectedRoute allowedRole="citizen"><CitizenPortal /></ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}