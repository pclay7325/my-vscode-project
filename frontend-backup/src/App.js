import React, { useState, useEffect } from "react";
import { fetchKPIRecords, addKPIRecord } from "./api";
const API_BASE = "http://127.0.0.1:8000/api";

function App() {
  const [records, setRecords] = useState([]);
  const [oeeMin, setOeeMin] = useState(""); // State for minimum OEE filter
  const [newRecord, setNewRecord] = useState({
    file_id: "",
    availability: "",
    performance: "",
    quality: "",
    oee: "",
  });

  // Fetch KPI records on component mount
  useEffect(() => {
    const getRecords = async () => {
      const data = await fetchKPIRecords();
      setRecords(data);
    };
    getRecords();
  }, []);

  // Handle form submission to add a new record
  const handleAddRecord = async (e) => {
    e.preventDefault();
    await addKPIRecord(newRecord);
    const updatedRecords = await fetchKPIRecords();
    setRecords(updatedRecords);
    setNewRecord({ file_id: "", availability: "", performance: "", quality: "", oee: "" });
  };

  // Handle filtering records by minimum OEE
  const handleFilterRecords = async () => {
    try {
      const response = await fetch(`${API_BASE}/kpi_records/filter/?oee_min=${oeeMin}`);
      const data = await response.json();
      setRecords(data);
    } catch (error) {
      console.error("Error filtering records:", error);
    }
  };

  return (
    <div>
      <h1>KPI Records</h1>
      <table border="1" cellPadding="5">
        <thead>
          <tr>
            <th>File ID</th>
            <th>Availability</th>
            <th>Performance</th>
            <th>Quality</th>
            <th>OEE</th>
          </tr>
        </thead>
        <tbody>
          {records.map((record, index) => (
            <tr key={index}>
              <td>{record.file_id}</td>
              <td>{record.availability}</td>
              <td>{record.performance}</td>
              <td>{record.quality}</td>
              <td>{record.oee}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Filter Records</h2>
      <div>
        <label>Minimum OEE:</label>
        <input
          type="number"
          value={oeeMin}
          onChange={(e) => setOeeMin(e.target.value)}
        />
        <button onClick={handleFilterRecords}>Filter</button>
      </div>

      <h2>Add New Record</h2>
      <form onSubmit={handleAddRecord}>
        <div>
          <label>File ID:</label>
          <input
            type="text"
            value={newRecord.file_id}
            onChange={(e) => setNewRecord({ ...newRecord, file_id: e.target.value })}
          />
        </div>
        <div>
          <label>Availability:</label>
          <input
            type="number"
            value={newRecord.availability}
            onChange={(e) => setNewRecord({ ...newRecord, availability: e.target.value })}
          />
        </div>
        <div>
          <label>Performance:</label>
          <input
            type="number"
            value={newRecord.performance}
            onChange={(e) => setNewRecord({ ...newRecord, performance: e.target.value })}
          />
        </div>
        <div>
          <label>Quality:</label>
          <input
            type="number"
            value={newRecord.quality}
            onChange={(e) => setNewRecord({ ...newRecord, quality: e.target.value })}
          />
        </div>
        <div>
          <label>OEE:</label>
          <input
            type="number"
            value={newRecord.oee}
            onChange={(e) => setNewRecord({ ...newRecord, oee: e.target.value })}
          />
        </div>
        <button type="submit">Add Record</button>
      </form>
    </div>
  );
}

export default App;
