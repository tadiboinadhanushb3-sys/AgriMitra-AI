import { useEffect, useState } from 'react';

const FarmPage = () => {
  const [farm, setFarm] = useState<any>(null);

  useEffect(() => {
    Promise.all([
      fetch('http://localhost:8000/api/profile'),
      fetch('http://localhost:8000/api/dashboard'),
    ])
      .then(async ([profileRes, dashboardRes]) => {
        const profile = await profileRes.json();
        const dashboard = await dashboardRes.json();
        setFarm({
          ...profile,
          ...dashboard.summary,
          weather: dashboard.weather,
          alerts: dashboard.alerts,
        });
      })
      .catch(() => {
        setFarm({
          name: 'Demo Farmer',
          location: 'Eluru, Andhra Pradesh',
          landArea: '5 acres',
          soilType: 'Loamy',
          currentCrop: 'Tomato',
          cropStage: 'Flowering',
          season: 'Rabi',
          waterStatus: 'Balanced',
          soilPH: 6.4,
          farmScore: 87,
        });
      });
  }, []);

  if (!farm) return <div className="page-shell"><div className="panel">Loading farm profile...</div></div>;

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">My Farm</p>
          <h2>Farm profile and operational overview</h2>
        </div>
      </div>

      <div className="farm-grid">
        <div className="panel large">
          <div className="panel-header">
            <h3>Farm overview</h3>
            <span className="badge success">Healthy</span>
          </div>
          <div className="summary-row">
            <div><label>Farm name</label><strong>{farm.name || 'Main Field'}</strong></div>
            <div><label>Location</label><strong>{farm.location || 'Eluru, Andhra Pradesh'}</strong></div>
            <div><label>Farm size</label><strong>{farm.landArea || '5 acres'}</strong></div>
            <div><label>Current crop</label><strong>{farm.currentCrop || 'Tomato'}</strong></div>
            <div><label>Soil type</label><strong>{farm.soilType || 'Loamy'}</strong></div>
            <div><label>Soil pH</label><strong>{farm.soilPH || 6.4}</strong></div>
            <div><label>Water availability</label><strong>{farm.waterStatus || 'Balanced'}</strong></div>
            <div><label>Current season</label><strong>{farm.season || 'Rabi'}</strong></div>
            <div><label>Farm health score</label><strong>{farm.farmScore || 87}/100</strong></div>
          </div>
        </div>

        <div className="panel">
          <h3>Field status</h3>
          <div className="farm-metrics">
            <div className="farm-metric">
              <span>Crop stage</span>
              <strong>{farm.cropStage || 'Flowering'}</strong>
            </div>
            <div className="farm-metric">
              <span>Soil moisture</span>
              <strong>{farm.soilMoisture || 68}%</strong>
            </div>
            <div className="farm-metric">
              <span>Risk level</span>
              <strong>{farm.diseaseRisk || 18}%</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FarmPage;
