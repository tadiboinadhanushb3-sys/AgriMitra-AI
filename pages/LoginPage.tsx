import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const LoginPage = ({ onLogin }: { onLogin: (payload: { email: string; password: string }) => Promise<void> }) => {
  const [email, setEmail] = useState('demo@agrimitra.ai');
  const [password, setPassword] = useState('demo123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await onLogin({ email, password });
      navigate('/onboarding');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <span className="brand-mark">AgriMitra AI</span>
          <h2>Welcome back</h2>
        </div>
        <p className="demo-note">Demo login: demo@agrimitra.ai / demo123</p>
        <form onSubmit={handleSubmit} className="auth-form">
          <label>
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
          </label>
          <label>
            Password
            <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
          </label>
          {error && <div className="error-box">{error}</div>}
          <button className="primary full" type="submit" disabled={loading}>{loading ? 'Signing in...' : 'Login'}</button>
        </form>
        <div className="auth-links">
          <Link to="/register">Create account</Link>
          <Link to="/">Forgot password?</Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
