import { useEffect, useState } from 'react';

const cropStages: Record<string, { label: string; stages: string[] }> = {
  Tomato: {
    label: 'Tomato',
    stages: ['Planting', 'Germination', 'Growth', 'Fertilization', 'Disease Monitoring', 'Flowering', 'Harvest'],
  },
  Chilli: {
    label: 'Chilli',
    stages: ['Nursery', 'Transplanting', 'Vegetative Growth', 'Flowering', 'Fruit Setting', 'Harvest'],
  },
  Groundnut: {
    label: 'Groundnut',
    stages: ['Sowing', 'Germination', 'Vegetative Growth', 'Pegging', 'Pod Formation', 'Harvest'],
  },
};

const CalendarPage = () => {
  const [calendar, setCalendar] = useState<any>(null);
  const [selectedCrop, setSelectedCrop] = useState('Tomato');

  useEffect(() => {
    fetch('/api/calendar')
      .then((res) => res.json())
      .then(setCalendar);
  }, []);

  const timeline = calendar?.timeline || [
    { name: 'Planting', status: 'completed' },
    { name: 'Germination', status: 'completed' },
    { name: 'Growth', status: 'in-progress' },
    { name: 'Fertilization', status: 'pending' },
    { name: 'Disease Monitoring', status: 'pending' },
    { name: 'Flowering', status: 'pending' },
    { name: 'Harvest', status: 'pending' },
  ];

  if (!calendar) return <div className="page-shell"><div className="panel">Loading crop calendar...</div></div>;

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Crop Calendar</p>
          <h2>{selectedCrop} growth timeline</h2>
        </div>
        <select className="compact-select" value={selectedCrop} onChange={(e) => setSelectedCrop(e.target.value)}>
          {Object.keys(cropStages).map((crop) => (
            <option key={crop} value={crop}>{crop}</option>
          ))}
        </select>
      </div>

      <div className="timeline-grid">
        {timeline.map((item: any, idx: number) => (
          <div key={`${item.name}-${idx}`} className={`timeline-step ${item.status}`}>
            <div className="step-index">{idx + 1}</div>
            <strong>{item.name}</strong>
            <span>{item.status}</span>
          </div>
        ))}
      </div>

      <div className="panel">
        <h3>Today’s recommended activities</h3>
        <ul>
          {(calendar.recommendedActivities || [
            'Monitor leaf health for early blight signs',
            'Check soil moisture before evening irrigation',
            'Review nutrient application for flowering stage',
          ]).map((item: string) => <li key={item}>{item}</li>)}
        </ul>
      </div>
    </div>
  );
};

export default CalendarPage;
