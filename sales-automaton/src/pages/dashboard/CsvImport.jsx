import { useState } from "react";
import api from "../../api/client";
import "../../styles/csvImport.css";

export default function CsvImport() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const upload = async () => {
    const form = new FormData();
    form.append("file", file);

    const res = await api.post(
      "/leads/import/csv/",
      form,
      { headers: { "Content-Type": "multipart/form-data" } }
    );

    setResult(res.data);
  };

  return (
    <div className="csv-page">
      <div className="csv-container">

        <h2 className="csv-title">Import Leads (CSV)</h2>

        <input
          className="csv-file-input"
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button
          className="csv-button"
          onClick={upload}
          disabled={!file}
        >
          Import
        </button>

        {result && (
          <div className="csv-result">
            Successfully imported <b>{result.created}</b> leads.
          </div>
        )}

      </div>
    </div>
  );
}