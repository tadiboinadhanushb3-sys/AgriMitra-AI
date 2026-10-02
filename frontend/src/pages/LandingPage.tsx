import { Link } from 'react-router-dom';

const features = [
  { title: 'Crop Recommendation', description: 'AI-driven crop suitability guidance tuned to your soil and season.' },
  { title: 'Disease Detection', description: 'Identify crop stress and disease patterns from leaf imagery.' },
  { title: 'Weather Intelligence', description: 'Translate rainfall, humidity, and wind into farm-ready steps.' },
  { title: 'Market Intelligence', description: 'Track mandi prices and demand for better harvest timing.' },
  { title: 'Crop Calendar', description: 'Plan every farm activity from sowing to harvest.' },
  { title: 'AI Farming Assistant', description: 'Ask quick questions and get context-aware guidance.' },
];

const steps = [
  'Tell us about your farm.',
  'AI analyzes your conditions.',
  'Get personalized recommendations.',
  'Monitor crop health throughout the cycle.',
];

const LandingPage = () => (
  <div className="landing-page">
    <header className="topbar">
      <div className="brand">AgriMitra AI</div>
      <div className="nav-actions">
        <Link to="/login">Login</Link>
        <Link className="primary" to="/register">Get Started</Link>
      </div>
    </header>

    <section className="hero">
      <div className="hero-copy">
        <p className="eyebrow">From Seed to Harvest — AI Guidance for Every Decision</p>
        <h1>Smart Farming. Smarter Decisions.</h1>
        <p className="subtitle">
          AI-powered crop recommendations, disease detection, weather intelligence, market insights and personalized farm guidance — all in one place.
        </p>
        <div className="hero-cta">
          <Link className="primary" to="/login">Get Started</Link>
          <a href="#features">Explore AgriMitra</a>
        </div>
      </div>
      <div className="hero-visual">
        <div className="farmer-card">
          <div className="farmer-avatar" />
          <div className="mini-card card-one">Crop Suitability: 94%</div>
          <div className="mini-card card-two">Disease Risk: Low</div>
          <div className="mini-card card-three">Rain Expected: 18 mm</div>
          <div className="mini-card card-four">Market Demand: High</div>
        </div>
      </div>
    </section>

    <section className="section why">
      <div className="section-heading">
        <p className="eyebrow">Why AgriMitra?</p>
        <h2>Farm decisions become clearer with actionable intelligence.</h2>
      </div>
      <div className="problem-grid">
        <div className="problem-card">Difficult crop selection</div>
        <div className="problem-card">Late disease identification</div>
        <div className="problem-card">Weather uncertainty</div>
        <div className="problem-card">Limited expert access</div>
        <div className="problem-card">Scattered market information</div>
        <div className="problem-card">Lack of personalized planning</div>
      </div>
    </section>

    <section id="features" className="section">
      <div className="section-heading">
        <p className="eyebrow">AI-Powered Features</p>
        <h2>Everything a modern farmer needs in one digital assistant.</h2>
      </div>
      <div className="feature-grid">
        {features.map((feature) => (
          <div key={feature.title} className="feature-card">
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </section>

    <section className="section how-it-works">
      <div className="section-heading">
        <p className="eyebrow">How It Works</p>
        <h2>From field inputs to smarter actions.</h2>
      </div>
      <div className="steps-grid">
        {steps.map((step, idx) => (
          <div className="step-card" key={step}>
            <div className="step-number">0{idx + 1}</div>
            <p>{step}</p>
          </div>
        ))}
      </div>
    </section>

    <section className="section preview-panel">
      <div className="snapshot-box">
        <div className="snapshot-header">Smart Farming Dashboard Preview</div>
        <div className="snapshot-grid">
          <div className="snapshot-stat">Farm Score<br /><strong>87/100</strong></div>
          <div className="snapshot-stat">Weather<br /><strong>Suitable</strong></div>
          <div className="snapshot-stat">Health<br /><strong>Healthy</strong></div>
          <div className="snapshot-stat">Market<br /><strong>High demand</strong></div>
        </div>
      </div>
    </section>

    <section className="section cta-banner">
      <h2>Start Your Smart Farming Journey</h2>
      <Link className="primary" to="/login">Get Started</Link>
    </section>
  </div>
);

export default LandingPage;
