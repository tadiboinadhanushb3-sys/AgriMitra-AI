import { NavLink, Outlet } from 'react-router-dom';
import { motion } from 'framer-motion';

const navItems = [
  { to: '/', label: 'Dashboard', icon: '◫' },
  { to: '/farm', label: 'My Farm', icon: '⛏' },
  { to: '/crop-recommendation', label: 'Crop Recommendation', icon: '🌾' },
  { to: '/disease-detection', label: 'AI Crop Doctor', icon: '🩺' },
  { to: '/weather', label: 'Weather', icon: '☁️' },
  { to: '/market', label: 'Market', icon: '📈' },
  { to: '/calendar', label: 'Crop Calendar', icon: '🗓️' },
  { to: '/chat', label: 'AI Assistant', icon: '🤖' },
  { to: '/knowledge', label: 'Knowledge Hub', icon: '📚' },
  { to: '/reports', label: 'Reports', icon: '📄' },
];

const Layout = ({ user, onLogout }: { user: { name: string; email: string; role: string }; onLogout: () => void }) => (
  <div className="app-shell">
    <aside className="sidebar">
      <div className="brand-box">
        <div className="brand-pill">AgriMitra AI</div>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <span>{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>
      <div className="sidebar-user">
        <div>
          <strong>{user.name}</strong>
          <small>{user.role}</small>
        </div>
        <button onClick={onLogout}>Logout</button>
      </div>
    </aside>

    <main className="content-panel">
      <header className="topbar-shell">
        <div>
          <p className="eyebrow subtle">Farm control center</p>
          <h2 className="page-title">AgriMitra AI</h2>
        </div>
        <div className="topbar-actions">
          <button className="icon-button" aria-label="Notifications" type="button">
            🔔 <span>3</span>
          </button>
          <div className="profile-pill">
            <span className="profile-avatar">{user.name.charAt(0)}</span>
            <div>
              <strong>{user.name}</strong>
              <small>{user.role}</small>
            </div>
          </div>
        </div>
      </header>

      <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }}>
        <Outlet />
      </motion.div>
    </main>
  </div>
);

export default Layout;
