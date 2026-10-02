import { useState } from 'react';

const defaultNutrientValues = {
  nitrogen: 'Not available',
  phosphorus: 'Not available',
  potassium: 'Not available',
  soilPh: 'Not available',
};

const parseNumericValue = (value: string) => {
  if (!value || value.trim() === '' || value.toLowerCase() === 'not available' || value.toLowerCase() === 'n/a') {
    return null;
  }

  const numericValue = Number(value);
  return Number.isFinite(numericValue) ? numericValue : null;
};

const extractValuesFromText = (text: string) => {
  const lowerText = text.toLowerCase();
  const detectValue = (patterns: string[]) => {
    for (const pattern of patterns) {
      const regex = new RegExp(`${pattern}\\s*[:=]\\s*(\\d+(?:\\.\\d+)?)`, 'i');
      const match = text.match(regex);
      if (match && match[1]) {
        return match[1];
      }
    }
    return 'Not available';
  };

  const nutrientValues = {
    nitrogen: detectValue(['nitrogen', 'n (kg/ha)', 'n kg/ha', 'available nitrogen']),
    phosphorus: detectValue(['phosphorus', 'p (kg/ha)', 'p kg/ha', 'available phosphorus']),
    potassium: detectValue(['potassium', 'k (kg/ha)', 'k kg/ha', 'available potassium']),
    soilPh: detectValue(['ph', 'soil ph', 'soil ph value', 'ph value']),
  };

  const hasReportText = lowerText.includes('soil') || lowerText.includes('test') || lowerText.includes('nitrate') || lowerText.includes('fertility');

  if (!hasReportText) {
    return defaultNutrientValues;
  }

  return {
    nitrogen: nutrientValues.nitrogen,
    phosphorus: nutrientValues.phosphorus,
    potassium: nutrientValues.potassium,
    soilPh: nutrientValues.soilPh,
  };
};

const CropRecommendationPage = () => {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [hasSoilReport, setHasSoilReport] = useState<'yes' | 'no'>('no');
  const [soilReportFile, setSoilReportFile] = useState<File | null>(null);
  const [extractedValues, setExtractedValues] = useState(defaultNutrientValues);
  const [reportMessage, setReportMessage] = useState('No soil test report provided. Use known farm information and proceed with a preliminary recommendation.');
  const [form, setForm] = useState({
    soilType: 'Loamy',
    soilPh: 'Not available',
    nitrogen: 'Not available',
    phosphorus: 'Not available',
    potassium: 'Not available',
    temperature: '30',
    humidity: '68',
    rainfall: '900',
    season: 'Rabi',
    waterAvailability: 'Moderate',
  });

  const handleChange = (key: string, value: string) => setForm((prev) => ({ ...prev, [key]: value }));

  const handleSoilReportUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    setSoilReportFile(file);
    setHasSoilReport('yes');
    setReportMessage(`Soil test report uploaded: ${file.name}. Review and confirm the extracted values below before generating a recommendation.`);

    try {
      const fileText = file.name.toLowerCase().endsWith('.txt') || file.name.toLowerCase().endsWith('.csv') ? await file.text() : '';
      const extracted = fileText ? extractValuesFromText(fileText) : defaultNutrientValues;
      setExtractedValues(extracted);

      setForm((prev) => ({
        ...prev,
        soilPh: extracted.soilPh,
        nitrogen: extracted.nitrogen,
        phosphorus: extracted.phosphorus,
        potassium: extracted.potassium,
      }));
    } catch {
      setExtractedValues(defaultNutrientValues);
      setForm((prev) => ({
        ...prev,
        soilPh: 'Not available',
        nitrogen: 'Not available',
        phosphorus: 'Not available',
        potassium: 'Not available',
      }));
      setReportMessage('The uploaded file could not be parsed automatically. Please verify the values below or continue with known field information.');
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    const payload = {
      hasSoilReport: hasSoilReport === 'yes',
      soilReportSource: soilReportFile ? soilReportFile.name : hasSoilReport === 'yes' ? 'Uploaded soil report' : 'No soil report',
      soilType: form.soilType,
      ph: parseNumericValue(form.soilPh),
      nitrogen: parseNumericValue(form.nitrogen),
      phosphorus: parseNumericValue(form.phosphorus),
      potassium: parseNumericValue(form.potassium),
      temperature: Number(form.temperature),
      humidity: Number(form.humidity),
      rainfall: Number(form.rainfall),
      season: form.season,
      waterAvailability: form.waterAvailability,
      location: 'Eluru, Andhra Pradesh',
      landArea: '5 acres',
      previousCrop: 'Rice',
      budget: '₹35,000',
    };

    const res = await fetch('http://localhost:8000/api/crop-recommendation/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Crop Recommendation Engine</p>
          <h2>AI-powered crop suitability analysis</h2>
        </div>
      </div>

      <div className="recommendation-layout">
        <div className="panel form-panel">
          <h3>Field details</h3>

          <div className="soil-report-toggle">
            <label className="toggle-label">Do you have a soil test report?</label>
            <div className="segmented-control">
              <button
                type="button"
                className={hasSoilReport === 'yes' ? 'active' : ''}
                onClick={() => setHasSoilReport('yes')}
              >
                Yes
              </button>
              <button
                type="button"
                className={hasSoilReport === 'no' ? 'active' : ''}
                onClick={() => {
                  setHasSoilReport('no');
                  setSoilReportFile(null);
                  setExtractedValues(defaultNutrientValues);
                  setForm((prev) => ({
                    ...prev,
                    soilPh: 'Not available',
                    nitrogen: 'Not available',
                    phosphorus: 'Not available',
                    potassium: 'Not available',
                  }));
                  setReportMessage('No soil test report provided. Use known farm information and continue with a preliminary recommendation.');
                }}
              >
                No
              </button>
            </div>
          </div>

          {hasSoilReport === 'yes' && (
            <div className="soil-report-box">
              <label className="upload-label">
                Upload soil test PDF or image
                <input type="file" accept=".pdf,.png,.jpg,.jpeg,.webp,.txt,.csv" onChange={handleSoilReportUpload} />
              </label>

              <div className="report-note">
                {reportMessage}
              </div>

              <div className="extracted-values">
                <h4>Verified soil values from uploaded report</h4>
                <div className="form-grid">
                  <label>
                    Nitrogen (N)
                    <input value={form.nitrogen} onChange={(e) => handleChange('nitrogen', e.target.value)} placeholder="Not available" />
                  </label>
                  <label>
                    Phosphorus (P)
                    <input value={form.phosphorus} onChange={(e) => handleChange('phosphorus', e.target.value)} placeholder="Not available" />
                  </label>
                  <label>
                    Potassium (K)
                    <input value={form.potassium} onChange={(e) => handleChange('potassium', e.target.value)} placeholder="Not available" />
                  </label>
                  <label>
                    Soil pH
                    <input value={form.soilPh} onChange={(e) => handleChange('soilPh', e.target.value)} placeholder="Not available" />
                  </label>
                </div>
              </div>
            </div>
          )}

          {hasSoilReport === 'no' && (
            <div className="soil-report-box muted-box">
              <strong>Since no soil report is available, continue with known field information only.</strong>
              <p>Optional values such as N, P, K and pH remain <strong>Not available</strong> unless you upload a report later.</p>
            </div>
          )}

          <div className="form-grid">
            <label>
              Soil type
              <select value={form.soilType} onChange={(e) => handleChange('soilType', e.target.value)}>
                <option>Loamy</option>
                <option>Clay</option>
                <option>Sandy</option>
                <option>Black Soil</option>
              </select>
            </label>
            <label>
              Temperature (°C)
              <input value={form.temperature} onChange={(e) => handleChange('temperature', e.target.value)} />
            </label>
            <label>
              Humidity (%)
              <input value={form.humidity} onChange={(e) => handleChange('humidity', e.target.value)} />
            </label>
            <label>
              Rainfall (mm)
              <input value={form.rainfall} onChange={(e) => handleChange('rainfall', e.target.value)} />
            </label>
            <label>
              Season
              <select value={form.season} onChange={(e) => handleChange('season', e.target.value)}>
                <option>Rabi</option>
                <option>Kharif</option>
                <option>Summer</option>
              </select>
            </label>
            <label>
              Water availability
              <select value={form.waterAvailability} onChange={(e) => handleChange('waterAvailability', e.target.value)}>
                <option>Low</option>
                <option>Moderate</option>
                <option>High</option>
              </select>
            </label>
          </div>

          <div className="how-to-get-soil-test">
            <strong>How to get a soil test?</strong>
            <p>Farmers can visit recognized soil-testing laboratories, agricultural universities, Krishi Vigyan Kendras, or local agriculture department services to collect a soil sample and receive a formal nutrient report.</p>
          </div>

          <button className="primary" onClick={handleSubmit} disabled={loading}>{loading ? 'Analyzing field...' : 'Generate recommendation'}</button>
        </div>

        <div className="panel result-panel">
          {result ? (
            <>
              <div className="result-header">
                <div>
                  <span className="eyebrow">{result.recommendationType || 'Preliminary Recommendation'}</span>
                  <h3>{result.recommendedCrop.name}</h3>
                </div>
                <div className="suitability">{result.recommendedCrop.suitability}%</div>
              </div>

              <div className="report-note inline-note">
                {result.soilDataStatus || 'Soil test information is not available for this recommendation.'}
              </div>

              {result.notes && (
                <div className="info-block">
                  <strong>Field note</strong>
                  <ul>
                    {result.notes.map((note: string) => <li key={note}>{note}</li>)}
                  </ul>
                </div>
              )}

              <div className="progress-stack">
                <div className="progress-row">
                  <span>Suitability</span>
                  <strong>{result.recommendedCrop.suitability}%</strong>
                </div>
                <div className="progress-bar">
                  <span style={{ width: `${result.recommendedCrop.suitability}%` }} />
                </div>
              </div>

              <div className="crop-fact-grid">
                <div className="crop-fact"><strong>Water</strong><span>{result.recommendedCrop.waterNeed}</span></div>
                <div className="crop-fact"><strong>Yield</strong><span>High</span></div>
                <div className="crop-fact"><strong>Duration</strong><span>{result.recommendedCrop.duration}</span></div>
                <div className="crop-fact"><strong>Season</strong><span>{result.recommendedCrop.season}</span></div>
              </div>

              <div className="info-block">
                <strong>Why this crop is recommended</strong>
                <ul>
                  {result.recommendedCrop.why.map((reason: string) => <li key={reason}>{reason}</li>)}
                </ul>
              </div>

              <div className="alt-list">
                {result.alternatives.map((alt: any) => (
                  <div key={alt.name} className="alt-item">
                    <strong>{alt.name}</strong>
                    <span>{alt.suitability}% suitability</span>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="empty-state">Input field conditions to generate a recommendation.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CropRecommendationPage;
