import { useEffect, useState } from 'react';

const MarketPage = () => {
  const [market, setMarket] = useState<any>(null);

  useEffect(() => {
    fetch('/api/market')
      .then((res) => res.json())
      .then(setMarket);
  }, []);

  if (!market) return <div className="page-shell"><div className="panel">Loading market data...</div></div>;

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Market Intelligence</p>
          <h2>Current mandi and demand signals</h2>
        </div>
      </div>
      <div className="market-layout">
        <div className="panel large">
          <div className="market-summary">
            <div>
              <span>Selected crop</span>
              <h3>{market.selectedCrop}</h3>
            </div>
            <div className="price-box">₹{market.price}/quintal</div>
          </div>
          <div className="metric-row">
            <div><strong>{market.demand}</strong><small>Demand</small></div>
            <div><strong>{market.selectedLocation}</strong><small>Location</small></div>
            <div><strong>{market.updatedAt}</strong><small>Updated</small></div>
          </div>
        </div>
        <div className="panel">
          <h3>Market comparison</h3>
          <ul className="market-list">
            {market.comparisons.map((item: any) => (
              <li key={item.market}><span>{item.market}</span><strong>₹{item.price}</strong></li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default MarketPage;
