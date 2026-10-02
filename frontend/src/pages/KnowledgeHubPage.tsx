import { useEffect, useState } from 'react';

const knowledgeCards = [
  { title: 'Crop Farming Guides', icon: '🌱', article: 'Crop farming begins with healthy soil, timely planting, and consistent observation. A balanced crop plan helps reduce input waste and improves yield stability.' },
  { title: 'Common Crop Diseases', icon: '🦠', article: 'Early detection is essential. Monitor leaf color, wetness, and spread patterns to prevent fungal outbreaks before they affect the whole field.' },
  { title: 'Smart Irrigation', icon: '💧', article: 'Irrigation should be guided by moisture level, crop stage, and rainfall forecasts. Drip systems and scheduled checks improve efficiency and reduce stress on roots.' },
  { title: 'Soil Management', icon: '🧪', article: 'Soil pH, organic matter, and nutrient balance influence root development and crop resilience. Periodic soil testing supports better decisions.' },
  { title: 'Fertilizer Management', icon: '🌾', article: 'Apply nutrients based on crop stage and soil analysis. Excess fertilizer can damage roots, waste cost, and lower quality produce.' },
  { title: 'Seasonal Farming Tips', icon: '🌧️', article: 'Seasonal planning helps farmers reduce crop stress. Adjust irrigation, disease monitoring, and sowing timing according to weather patterns.' },
];

const KnowledgeHubPage = () => {
  const [knowledge, setKnowledge] = useState<any>(null);
  const [selectedArticle, setSelectedArticle] = useState<string | null>(knowledgeCards[0].article);

  useEffect(() => {
    fetch('/api/knowledge')
      .then((res) => res.json())
      .then((payload) => {
        setKnowledge(payload);
        if (payload?.featured?.length) setSelectedArticle(payload.featured[0].summary);
      });
  }, []);

  if (!knowledge) return <div className="page-shell"><div className="panel">Loading knowledge hub...</div></div>;

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Knowledge Hub</p>
          <h2>Practical learning resources for smarter farm decisions.</h2>
        </div>
      </div>

      <div className="knowledge-grid">
        {knowledgeCards.map((item) => (
          <button key={item.title} type="button" className="panel article-card" onClick={() => setSelectedArticle(item.article)}>
            <span className="article-icon">{item.icon}</span>
            <span className="badge">Learning</span>
            <h3>{item.title}</h3>
            <p>{item.article}</p>
          </button>
        ))}
      </div>

      <div className="panel article-detail">
        <h3>Featured insight</h3>
        <p>{selectedArticle || 'Pick a learning card to read a short guide.'}</p>
      </div>

      <div className="panel">
        <h3>FAQ</h3>
        <ul>
          {knowledge.faqs.map((item: any) => (
            <li key={item.q}><strong>{item.q}</strong> — {item.a}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default KnowledgeHubPage;
