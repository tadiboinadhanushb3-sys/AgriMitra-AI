import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const RegisterPage = ({ onRegister }: { onRegister: (payload: { name: string; email: string; phone: string; password: string }) => Promise<void> }) => {
  const [form, setForm] = useState({ name: 'Demo Farmer', email: 'demo@agrimitra.ai', phone: '+91 98765 43210', password: 'demo123' });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (key: keyof typeof form, value: string) => setForm((prev) => ({ ...prev, [key]: value }));

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onRegister(form);
      navigate('/onboarding');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card wide">
        <div className="auth-header">
          <span className="brand-mark">AgriMitra AI</span>
          <h2>Create your farmer profile</h2>
        </div>
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="two-col">
            <label>
              Full Name
              <input value={form.name} onChange={(e) => handleChange('name', e.target.value)} required />
            </label>
            <label>
              Phone
              <input value={form.phone} onChange={(e) => handleChange('phone', e.target.value)} required />
            </label>
          </div>
          <label>
            Email
            <input type="email" value={form.email} onChange={(e) => handleChange('email', e.target.value)} required />
          </label>
          <label>
            Password
            <input type="password" value={form.password} onChange={(e) => handleChange('password', e.target.value)} required />
          </label>
          <button className="primary full" type="submit" disabled={loading}>{loading ? 'Creating...' : 'Register'}</button>
        </form>
        <div className="auth-links">
          <Link to="/login">Already have an account?</Link>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
