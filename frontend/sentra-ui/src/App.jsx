// frontend/src/App.jsx
import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  // State to store the REAL data from Python
  const [apiResult, setApiResult] = useState(null);
  
  const resultRef = useRef(null);
  const fileInputRef = useRef(null);

  // --- File Handling Logic ---
  const handleFiles = (files) => {
    const fileList = Array.from(files);
    const pdfs = fileList.filter(file => file.type === "application/pdf");
    setUploadedFiles((prev) => [...prev, ...pdfs]);
    setIsDragging(false);
  };

  const removeFile = (index, e) => {
    e.stopPropagation(); 
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const onFileSelect = (e) => handleFiles(e.target.files);
  const handleDragOver = (e) => { e.preventDefault(); setIsDragging(true); };
  const handleDragLeave = () => { setIsDragging(false); };
  const handleDrop = (e) => { e.preventDefault(); handleFiles(e.dataTransfer.files); };

  const handleBoxClick = (e) => {
    if (e.target.tagName !== 'BUTTON' && !e.target.classList.contains('remove-file-btn')) {
      fileInputRef.current.click();
    }
  };

  // --- API Connection: Upload ---
  const startUpload = async () => {
    if (uploadedFiles.length === 0) return;
    
    const formData = new FormData();
    uploadedFiles.forEach(file => {
      formData.append("files", file);
    });

    try {
      alert(`Uploading ${uploadedFiles.length} files...`);
      await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      alert("Success! Documents indexed.");
      setUploadedFiles([]);
    } catch (error) {
      console.error(error);
      alert("Upload failed. Is the backend running?");
    }
  };

  // --- API Connection: Analyze ---
  const handleEvaluate = async () => {
    if (!input.trim()) return;
    
    setIsLoading(true);
    setShowResult(false);

    try {
      // Call Python Backend
      const response = await axios.post("http://localhost:8000/analyze", {
        text: input
      });

      setApiResult(response.data); // Store the real answer
      setShowResult(true);
      
      // Smooth scroll to result
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);

    } catch (error) {
      console.error(error);
      alert("Analysis failed. Make sure backend is running on port 8000.");
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function for dynamic styling
  const getRiskColorClass = (level) => {
    if (level === 'High') return 'risk-high';
    if (level === 'Medium') return 'risk-medium';
    return 'risk-low';
  };

  return (
    <div className="sentra-layout">
      <nav className="top-bar">
        <div className="container-wide">
          <div className="brand">SENTRA</div>
          <div className="nav-menu">
            <span>Governance</span>
            <span>Compliance</span>
            <span>API</span>
          </div>
        </div>
      </nav>

      <main className="main-content">
        <section className="hero-section">
          <div className="badge">v1.0 Decision Intelligence</div>
          <h1 className="hero-title">AI Policy Governance</h1>
          <p className="hero-subtitle">
            Automate policy enforcement and decision intelligence with Sentra's 
            enterprise-grade evaluation engine.
          </p>
        </section>

        {/* Upload Section */}
        <section className="page-block upload-wrapper">
          <div 
            className={`upload-box ${isDragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={handleBoxClick}
          >
            <h3>Contextualize Documentation</h3>
            <p>Drop policy PDFs here or click to explore</p>
            
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={onFileSelect} 
              style={{ display: 'none' }} 
              multiple 
              accept=".pdf"
            />
            
            <button className="btn-secondary" onClick={(e) => {
               e.stopPropagation();
               fileInputRef.current.click();
            }}>
              Select Files
            </button>

            {uploadedFiles.length > 0 && (
              <div className="file-preview-area">
                {uploadedFiles.map((file, idx) => (
                  <div key={idx} className="file-chip">
                    <span className="file-name">{file.name}</span>
                    <button 
                      className="remove-file-btn" 
                      onClick={(e) => removeFile(idx, e)}
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {uploadedFiles.length > 0 && (
            <button className="btn-upload-standalone" onClick={startUpload}>
              Upload {uploadedFiles.length} Files to Engine
            </button>
          )}
        </section>

        {/* Input Section */}
        <section className="page-block">
          <h2 className="section-heading">Decision Input</h2>
          <div className="input-card-bg">
            <textarea
              className="decision-textarea"
              placeholder="Example: Can an intern work remotely using a personal laptop?"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button 
              className="btn-primary" 
              onClick={handleEvaluate}
              disabled={isLoading}
            >
              {isLoading ? "Analyzing Policies..." : "Evaluate Decision"}
            </button>
          </div>
        </section>

        {/* Dynamic Results Section */}
        {showResult && apiResult && (
          <section className="results-container fade-in" ref={resultRef}>
            <div className="res-card">
              <span className="res-label">Evaluation Result</span>
              
              <div className="res-row">
                <strong>Risk Level:</strong> 
                <span className={`risk-tag ${getRiskColorClass(apiResult.riskLevel)}`}>
                   {apiResult.riskLevel}
                </span>
              </div>
              
              <div className="res-row">
                <strong>Policy Evidence:</strong> 
                <span>{apiResult.evidence}</span>
              </div>
              
              <div className="res-row">
                <strong>Recommendation:</strong> 
                <span>{apiResult.recommendation}</span>
              </div>
            </div>
            
            <div className="res-card">
              <span className="res-label">Reasoning</span>
              <p className="res-text">{apiResult.reasoning}</p>
            </div>

            {apiResult.alternatives && (
              <div className="res-card accent-left">
                <span className="res-label">Safer Alternative</span>
                <p className="res-text">{apiResult.alternatives}</p>
              </div>
            )}
          </section>
        )}
      </main>

      <footer className="page-footer">© 2026 SENTRA AI</footer>
    </div>
  );
}

export default App;