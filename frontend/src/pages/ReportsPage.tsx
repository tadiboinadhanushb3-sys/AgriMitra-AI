import { useEffect, useState } from 'react';

const ReportsPage = () => {
  const [report, setReport] = useState<any>(null);

  useEffect(() => {
    fetch('/api/reports')
      .then((res) => res.json())
      .then(setReport);
  }, []);

  if (!report) return <div className="page-shell"><div className="panel">Preparing report...</div></div>;

  const handleDownload = () => {
    window.print();
  };

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">Reports</p>
          <h2>Farm report summary</h2>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h3>{report.summary.farmer}</h3>
          <button className="primary" type="button" onClick={handleDownload}>Download Report as PDF</button>
        </div>

        <div className="summary-row">
          <div><label>Location</label><strong>{report.summary.location}</strong></div>
          <div><label>Current crop</label><strong>{report.summary.currentCrop}</strong></div>
          <div><label>Crop stage</label><strong>{report.summary.cropStage}</strong></div>
          <div><label>Status</label><strong>{report.summary.status}</strong></div>
        </div>

        <div className="report-sections">
          {report.reportSections.map((section: string) => (
            <span key={section} className="badge report-badge">{section}</span>
          ))}
        </div>

        <div className="report-details">
          <div className="report-box">
            <strong>Farm information</strong>
            <p>Land size: 5 acres · Soil type: Loamy · Water availability: Moderate</p>
          </div>
          <div className="report-box">
            <strong>Soil analysis</strong>
            <p>pH is 6.4 with balanced nutrient profile and suitable root-zone moisture.</p>
          </div>
          <div className="report-box">
            <strong>AI recommendations</strong>
            <p>Reduce heavy irrigation today and continue observing leaf health under moderate humidity.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportsPage;
