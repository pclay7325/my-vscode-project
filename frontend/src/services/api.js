import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api";

// Fetch all KPI records
export const fetchKPIRecords = async () => {
  try {
    const response = await axios.get(`${API_BASE}/kpi_records/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching KPI records:", error);
    throw error;
  }
};

// Add a new KPI record
export const addKPIRecord = async (record) => {
  try {
    const response = await axios.post(`${API_BASE}/kpi_records/`, record);
    return response.data;
  } catch (error) {
    console.error("Error adding KPI record:", error);
    throw error;
  }
};
