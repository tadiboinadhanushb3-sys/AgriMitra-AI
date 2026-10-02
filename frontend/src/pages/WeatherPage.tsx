import { useEffect, useState } from 'react';

const WeatherPage = () => {
  const [weather, setWeather] = useState<any>(null);

  useEffect(() => {
    fetch('/api/weather')
      .then((res) => res.json())
      .then(setWeather);
  }, []);

  if (!weather) return <div className="page-shell"><div className="panel">Loading weather intelligence...</div></div>;

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Weather Intelligence</p>
          <h2>Current conditions and farming guidance</h2>
        </div>
      </div>

      <div className="weather-grid">
        <div className="panel large">
          <div className="temp-block big">{weather.current.temperature}°C <small>Feels like {weather.current.feelsLike}°C</small></div>
          <div className="metric-row">
            <div>Humidity <strong>{weather.current.humidity}%</strong></div>
            <div>Rainfall <strong>{weather.current.rainfall} mm</strong></div>
            <div>Wind <strong>{weather.current.windSpeed} km/h</strong></div>
            <div>Rain probability <strong>{weather.current.rainProbability}%</strong></div>
          </div>
        </div>

        <div className="panel">
          <h3>🌾 Farming Impact</h3>
          <div className="impact-list">
            {weather.farmingImpact ? (
              Object.entries(weather.farmingImpact).map(([key, value]: [string, any]) => (
                <div key={key} className="impact-item">
                  <div>
                    <strong>{key === 'irrigation' ? 'Irrigation' : key === 'spraying' ? 'Spraying' : key === 'diseaseRisk' ? 'Disease risk' : 'Rain risk'}</strong>
                    <small>{value.detail}</small>
                  </div>
                  <span className="status-pill">{value.status}</span>
                </div>
              ))
            ) : (
              weather.actions.map((action: any) => (
                <div key={action.title} className="impact-item">
                  <div>
                    <strong>{action.title}</strong>
                    <small>{action.advice}</small>
                  </div>
                  <span className={`status-pill ${action.severity}`}>{action.title}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      <div className="forecast-grid">
        {weather.forecast.map((day: any) => (
          <div key={day.day} className="panel forecast-box">
            <strong>{day.day}</strong>
            <div>{day.temp}°C</div>
            <small>{day.condition}</small>
            <span>{day.rain} mm rain</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WeatherPage;
