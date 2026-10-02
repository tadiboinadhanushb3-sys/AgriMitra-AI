import { Routes, Route, Navigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import CropRecommendationPage from './pages/CropRecommendationPage';
import DiseaseDetectionPage from './pages/DiseaseDetectionPage';
import WeatherPage from './pages/WeatherPage';
import MarketPage from './pages/MarketPage';
import CalendarPage from './pages/CalendarPage';
import ChatBotPage from './pages/ChatBotPage';
import KnowledgeHubPage from './pages/KnowledgeHubPage';
import ReportsPage from './pages/ReportsPage';
import FarmPage from './pages/FarmPage';
import OnboardingPage from './pages/OnboardingPage';
import Layout from './components/Layout';

const APP_API = 'http://localhost:8000';

type AuthSession = {
  token: string;
  user: {
    name: string;
    email: string;
    role: string;
    location: string;
  };
};

const safeLoadSession = (): AuthSession | null => {
  const raw = localStorage.getItem('agrimitra-session');
  if (!raw) return null;
  try {
    return JSON.parse(raw) as AuthSession;
  } catch {
    return null;
  }
};

const App = () => {
  const [loading, setLoading] = useState(true);
  const [session, setSession] = useState<AuthSession | null>(() => safeLoadSession());

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1800);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (session) localStorage.setItem('agrimitra-session', JSON.stringify(session));
    else localStorage.removeItem('agrimitra-session');
  }, [session]);

  const handleLogin = async (payload: { email: string; password: string }) => {
    const response = await fetch(`${APP_API}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Login failed');
    setSession({ token: data.token, user: data.user });
  };

  const handleRegister = async (payload: { name: string; email: string; phone: string; password: string }) => {
    const response = await fetch(`${APP_API}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Registration failed');
    setSession({ token: data.token, user: data.user });
  };

  const renderLoader = () => (
    <div className="loading-screen">
      <div className="loading-scene" />
      <div className="loading-overlay" />
      <div className="loading-content">
        <div className="brand-mark">AgriMitra AI</div>
        <h1>One Digital Assistant for Smarter Farming Decisions.</h1>
        <div className="loading-steps">
          <span>Understanding your farm...</span>
          <span>Checking field conditions...</span>
          <span>Preparing intelligent recommendations...</span>
          <span>Connecting farming intelligence...</span>
        </div>
        <div className="loading-spinner" />
      </div>
    </div>
  );

  if (loading) return renderLoader();

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
      <Route path="/register" element={<RegisterPage onRegister={handleRegister} />} />
      <Route path="/onboarding" element={session ? <OnboardingPage /> : <Navigate to="/login" replace />} />
      <Route
        path="/*"
        element={session ? <Layout user={session.user} onLogout={() => setSession(null)} /> : <Navigate to="/login" replace />}
      >
        <Route index element={<DashboardPage />} />
        <Route path="farm" element={<FarmPage />} />
        <Route path="crop-recommendation" element={<CropRecommendationPage />} />
        <Route path="disease-detection" element={<DiseaseDetectionPage />} />
        <Route path="weather" element={<WeatherPage />} />
        <Route path="market" element={<MarketPage />} />
        <Route path="calendar" element={<CalendarPage />} />
        <Route path="chat" element={<ChatBotPage />} />
        <Route path="knowledge" element={<KnowledgeHubPage />} />
        <Route path="reports" element={<ReportsPage />} />
      </Route>
    </Routes>
  );
};

export default App;
