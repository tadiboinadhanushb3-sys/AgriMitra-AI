import { ChangeEvent, useState } from 'react';

const DiseaseDetectionPage = () => {
  const [result, setResult] = useState<any>(null);
  const [image, setImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFile = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setImage(String(reader.result));
    reader.readAsDataURL(file);
  };

  const handleAnalyze = async () => {
    setLoading(true);
    const formData = new FormData();
    if (image) {
      const blob = await fetch(image).then((res) => res.blob());
      formData.append('file', blob, 'leaf-image.jpg');
    }
    const res = await fetch('http://localhost:8000/api/disease-detection/analyze', {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">AI Crop Doctor</p>
          <h2>Upload a leaf image and let AgriMitra analyze it.</h2>
        </div>
      </div>
      <div className="disease-layout">
        <div className="panel upload-panel">
          <div className="upload-box">
            {image ? <img src={image} alt="uploaded leaf" /> : <div className="upload-placeholder">Drop or select a leaf image</div>}
          </div>
          <input type="file" accept="image/*" onChange={handleFile} />
          <button className="primary" onClick={handleAnalyze} disabled={loading}>{loading ? 'Analyzing leaf...' : 'Analyze'}</button>
        </div>
        <div className="panel result-panel">
          {result ? (
            <>
              <h3>{result.disease}</h3>
              <div className="confidence">Model confidence: {result.confidence}%</div>
              <div className="info-block">
                <strong>Symptoms</strong>
                <ul>{result.symptoms.map((s: string) => <li key={s}>{s}</li>)}</ul>
              </div>
              <div className="info-block">
                <strong>Immediate actions</strong>
                <ul>{result.actions.map((a: string) => <li key={a}>{a}</li>)}</ul>
              </div>
              <p className="muted">AI result — verify severe cases with an agricultural expert.</p>
            </>
          ) : (
            <div className="empty-state">No diagnosis yet. Upload an image to begin.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DiseaseDetectionPage;
