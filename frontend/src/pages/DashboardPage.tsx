import { useEffect, useState } from 'react';

const buildLinePath = (values: number[], width = 300, height = 120) => {
  const max = Math.max(...values, 100);
  const min = Math.min(...values, 0);
  const range = max - min || 1;

  return values
    .map((value, index) => {
      const x = (index / (values.length - 1)) * width;
      const y = height - ((value - min) / range) * (height - 15) - 8;
      return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
    })
    .join(' ');
};

const TrendChart = ({ values, color, labels }: { values: number[]; color: string; labels: readonly string[] }) => (
  <div className="chart-shell">
    <svg className="trend-svg" viewBox="0 0 300 120" preserveAspectRatio="none" aria-label="Trend chart">
      <defs>
        <linearGradient id={`area-${color.replace('#', '')}`} x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.35" />
          <stop offset="100%" stopColor={color} stopOpacity="0.02" />
        </linearGradient>
      </defs>
      <path d={`${buildLinePath(values)} L 300 120 L 0 120 Z`} fill={`url(#area-${color.replace('#', '')})`} opacity="0.9" />
      <path d={buildLinePath(values)} fill="none" stroke={color} strokeWidth="3" strokeLinecap="round" />
    </svg>
    <div className="chart-labels">
      {labels.map((label) => (
        <span key={label}>{label}</span>
      ))}
    </div>
  </div>
);

const DashboardPage = () => {
  const [data, setData] = useState<any>(null);
  const [range, setRange] = useState<'7' | '30' | '90'>('30');

  useEffect(() => {
    fetch('/api/dashboard')
      .then((res) => res.json())
      .then((payload) => setData(payload))
      .catch(() =>
        setData({
          farmer: { name: 'Demo Farmer', location: 'Eluru, Andhra Pradesh', landArea: '5 acres', soilType: 'Loamy', currentCrop: 'Tomato', cropStage: 'Flowering' },
          summary: {
            farmScore: 87,
            soilMoisture: 68,
            temperature: 29,
            rainfall: 18,
            soilPH: 6.4,
            diseaseRisk: 18,
            irrigationStatus: 'Balanced',
            weatherSuitability: 92,
            soilCondition: 85,
            waterStatus: 80,
            marketCondition: 88,
          },
          weather: { temperature: 29, humidity: 68, rainProbability: 62, windSpeed: 13, feelsLike: 32 },
          tasks: [{ title: 'Irrigation review', time: 'Today · 7:30 AM', status: 'pending' }],
          insight: { title: 'AgriMitra Insight', text: 'Rainfall is expected within the next 24 hours. Review irrigation timing before watering the field.' },
          aiRecommendation: {
            title: 'Today’s AI Recommendation',
            message: 'Based on current soil moisture, temperature and weather conditions, irrigation is not required today.',
            confidence: 'High confidence',
            reasons: ['Soil moisture is within the ideal range for tomato roots.'],
          },
          analytics: {
            farmHealth: [78, 80, 82, 85, 86, 88, 87],
            soilMoisture: [60, 62, 65, 67, 63, 68, 69],
            temperature: [28, 29, 30, 29, 31, 30, 29],
            cropHealth: [72, 75, 78, 80, 83, 84, 87],
          },
          alerts: [{ type: 'Weather', severity: 'warning', message: 'High humidity may increase disease risk.' }],
        })
      );
  }, []);

  if (!data) {
    return (
      <div className="page-shell">
        <div className="panel">Loading farm intelligence...</div>
      </div>
    );
  }

  const summary = data.summary || {};
  const chartMap = {
    '7': {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      farmHealth: data.analytics?.farmHealth || [75, 78, 82, 83, 86, 88, 87],
      soilMoisture: data.analytics?.soilMoisture || [60, 62, 65, 67, 63, 68, 69],
      temperature: data.analytics?.temperature || [28, 29, 30, 29, 31, 30, 29],
      cropHealth: data.analytics?.cropHealth || [72, 75, 78, 80, 83, 84, 87],
    },
    '30': {
      labels: ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7'],
      farmHealth: [72, 75, 78, 80, 82, 84, 87],
      soilMoisture: [58, 61, 64, 66, 67, 69, 68],
      temperature: [27, 28, 29, 30, 30, 31, 29],
      cropHealth: [70, 73, 76, 78, 81, 84, 87],
    },
    '90': {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
      farmHealth: [68, 70, 72, 76, 80, 83, 87],
      soilMoisture: [56, 58, 60, 63, 64, 66, 68],
      temperature: [26, 27, 28, 29, 30, 31, 29],
      cropHealth: [66, 69, 72, 76, 79, 83, 87],
    },
  } as const;

  const activeChart = chartMap[range];

  const metricCards = [
    { label: 'Farm Health Score', value: `${summary.farmScore ?? 87}/100`, tone: 'accent', detail: 'Overall field vitality' },
    { label: 'Soil Moisture', value: `${summary.soilMoisture ?? 68}%`, tone: '', detail: 'Root-zone moisture' },
    { label: 'Temperature', value: `${summary.temperature ?? data.weather?.temperature ?? 29}°C`, tone: '', detail: 'Current field temp' },
    { label: 'Rainfall', value: `${summary.rainfall ?? 18} mm`, tone: '', detail: 'Recent rainfall' },
    { label: 'Soil pH', value: `${summary.soilPH ?? 6.4}`, tone: '', detail: 'Balanced condition' },
    { label: 'Disease Risk', value: `${summary.diseaseRisk ?? 18}%`, tone: '', detail: 'Low fungal pressure' },
    { label: 'Water / Irrigation', value: summary.irrigationStatus ?? 'Balanced', tone: '', detail: 'Irrigation status' },
  ];

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Good morning, {data.farmer?.name || 'Farmer'}</p>
          <h2>Here is your farm intelligence for today.</h2>
        </div>
      </div>

      <section className="stats-grid">
        {metricCards.map((card) => (
          <div key={card.label} className={`stat-card ${card.tone}`}>
            <span>{card.label}</span>
            <strong>{card.value}</strong>
            <small>{card.detail}</small>
          </div>
        ))}
      </section>

      <section className="ai-recommendation panel">
        <div className="panel-header compact">
          <div>
            <p className="eyebrow">🤖 AI Recommendation</p>
            <h3>{data.aiRecommendation?.title || 'Today’s AI Recommendation'}</h3>
          </div>
          <span className="badge success">{data.aiRecommendation?.confidence || 'High confidence'}</span>
        </div>
        <p className="lead-copy">{data.aiRecommendation?.message || 'Based on current soil moisture, temperature and weather conditions, irrigation is not required today.'}</p>
        <div className="recommendation-points">
          {(data.aiRecommendation?.reasons || ['Soil moisture is within the ideal range.']).map((reason: string) => (
            <span key={reason}>✓ {reason}</span>
          ))}
        </div>
      </section>

      <section className="dashboard-main">
        <div className="panel chart-panel large">
          <div className="panel-header">
            <h3>Farm trend analytics</h3>
            <div className="range-filter">
              {(['7', '30', '90'] as const).map((item) => (
                <button
                  key={item}
                  type="button"
                  className={range === item ? 'range-button active' : 'range-button'}
                  onClick={() => setRange(item)}
                >
                  {item === '7' ? '7 Days' : item === '30' ? '30 Days' : '3 Months'}
                </button>
              ))}
            </div>
          </div>

          <div className="chart-grid">
            <div className="chart-card">
              <h4>Farm health</h4>
              <TrendChart values={activeChart.farmHealth} color="#2d7d4a" labels={activeChart.labels} />
            </div>
            <div className="chart-card">
              <h4>Soil moisture</h4>
              <TrendChart values={activeChart.soilMoisture} color="#4cb6d7" labels={activeChart.labels} />
            </div>
            <div className="chart-card">
              <h4>Temperature</h4>
              <TrendChart values={activeChart.temperature} color="#f2a65a" labels={activeChart.labels} />
            </div>
            <div className="chart-card">
              <h4>Crop health</h4>
              <TrendChart values={activeChart.cropHealth} color="#7d9f4c" labels={activeChart.labels} />
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header"><h3>Weather</h3><span className="badge">Updated</span></div>
          <div className="temp-block">{data.weather?.temperature ?? 29}°C <small>Feels like {data.weather?.feelsLike ?? 32}°C</small></div>
          <div className="metric-row">
            <div>Humidity <strong>{data.weather?.humidity ?? 68}%</strong></div>
            <div>Rain probability <strong>{data.weather?.rainProbability ?? 62}%</strong></div>
            <div>Wind <strong>{data.weather?.windSpeed ?? 13} km/h</strong></div>
          </div>
          <div className="insight-box">
            <h4>{data.insight?.title || 'AgriMitra Insight'}</h4>
            <p>{data.insight?.text || 'Rainfall is expected within the next 24 hours.'}</p>
          </div>
        </div>
      </section>

      <section className="dashboard-columns">
        <div className="panel">
          <div className="panel-header"><h3>Today’s tasks</h3></div>
          <ul className="task-list">
            {(data.tasks || []).map((task: any) => (
              <li key={task.title}>
                <span className="dot" />
                <span>{task.title}</span>
                <small>{task.time}</small>
              </li>
            ))}
          </ul>
        </div>

        <div className="panel">
          <div className="panel-header"><h3>Market Outlook</h3></div>
          <div className="market-box">
            <strong>{data.market?.crop || 'Tomato'}</strong>
            <span>₹{data.market?.price || 2380}/quintal</span>
            <small>{data.market?.trend || 'Rising'} demand</small>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header"><h3>Smart Alerts</h3></div>
          <ul className="alert-list">
            {(data.alerts || []).map((item: any) => (
              <li key={item.message}>
                <span className={`severity ${item.severity}`}>{item.type}</span>
                <span>{item.message}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
};

export default DashboardPage;
