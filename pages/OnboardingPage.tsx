import { useState } from 'react';

const steps = ['Personal Details', 'Farm Details', 'Preferences', 'Complete Profile'];

const OnboardingPage = () => {
  const [step, setStep] = useState(0);
  const [data, setData] = useState({
    name: 'Demo Farmer',
    phone: '+91 98765 43210',
    email: 'demo@agrimitra.ai',
    location: 'Eluru, Andhra Pradesh',
    area: '5 acres',
    soil: 'Loamy',
    irrigation: 'Drip',
    water: 'Moderate',
    previousCrop: 'Rice',
    season: 'Rabi',
    budget: '₹35,000',
    preferredCrops: 'Tomato, Chilli',
  });

  const next = () => setStep((s) => Math.min(3, s + 1));
  const back = () => setStep((s) => Math.max(0, s - 1));

  const renderStep = () => {
    if (step === 0) {
      return (
        <div className="onboarding-grid">
          <label>Farmer name<input value={data.name} onChange={(e) => setData({ ...data, name: e.target.value })} /></label>
          <label>Phone<input value={data.phone} onChange={(e) => setData({ ...data, phone: e.target.value })} /></label>
          <label>Location<input value={data.location} onChange={(e) => setData({ ...data, location: e.target.value })} /></label>
          <label>Email<input value={data.email} onChange={(e) => setData({ ...data, email: e.target.value })} /></label>
        </div>
      );
    }
    if (step === 1) {
      return (
        <div className="onboarding-grid">
          <label>Land area<input value={data.area} onChange={(e) => setData({ ...data, area: e.target.value })} /></label>
          <label>Soil type<input value={data.soil} onChange={(e) => setData({ ...data, soil: e.target.value })} /></label>
          <label>Irrigation type<input value={data.irrigation} onChange={(e) => setData({ ...data, irrigation: e.target.value })} /></label>
          <label>Previous crop<input value={data.previousCrop} onChange={(e) => setData({ ...data, previousCrop: e.target.value })} /></label>
          <label>Available water<input value={data.water} onChange={(e) => setData({ ...data, water: e.target.value })} /></label>
        </div>
      );
    }
    if (step === 2) {
      return (
        <div className="onboarding-grid">
          <label>Season<input value={data.season} onChange={(e) => setData({ ...data, season: e.target.value })} /></label>
          <label>Budget<input value={data.budget} onChange={(e) => setData({ ...data, budget: e.target.value })} /></label>
          <label>Preferred crops<input value={data.preferredCrops} onChange={(e) => setData({ ...data, preferredCrops: e.target.value })} /></label>
        </div>
      );
    }
    return (
      <div className="summary-box">
        <h3>Your farm intelligence profile is ready.</h3>
        <ul>
          <li><strong>Farmer:</strong> {data.name}</li>
          <li><strong>Location:</strong> {data.location}</li>
          <li><strong>Area:</strong> {data.area}</li>
          <li><strong>Soil:</strong> {data.soil}</li>
          <li><strong>Season:</strong> {data.season}</li>
          <li><strong>Preferred crops:</strong> {data.preferredCrops}</li>
        </ul>
      </div>
    );
  };

  return (
    <div className="page-shell onboarding-shell">
      <div className="panel">
        <div className="section-heading">
          <p className="eyebrow">Farm onboarding</p>
          <h2>Build your field profile</h2>
        </div>
        <div className="progress-row">
          {steps.map((item, idx) => (
            <div key={item} className={`progress-item ${idx <= step ? 'active' : ''}`}>
              {String(idx + 1).padStart(2, '0')}
            </div>
          ))}
        </div>
        <div className="form-card">{renderStep()}</div>
        <div className="button-row">
          {step > 0 && <button className="secondary" onClick={back}>Back</button>}
          {step < 3 ? <button className="primary" onClick={next}>Next</button> : <button className="primary" onClick={() => window.location.href = '/'}>Continue to dashboard</button>}
        </div>
      </div>
    </div>
  );
};

export default OnboardingPage;
