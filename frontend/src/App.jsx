import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Landing from './pages/Landing';
import Login from './pages/Login';
import JudgeDashboard from './pages/JudgeDashboard';
import LawyerFiling from './pages/LawyerFiling';
import CitizenPortal from './pages/CitizenPortal';
import CreateAccount from './pages/CreateAccount';

function ProtectedRoute({ children, allowedRole }) {
  const role = sessionStorage.getItem('nyay_role');
  if (!role || role !== allowedRole) return <Navigate to="/" />;
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
        <Route path="/accounts/new" element={<CreateAccount />} />
      </Routes>
    </BrowserRouter>
  );
}
