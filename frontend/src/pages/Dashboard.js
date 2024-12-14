import React, { useEffect, useState } from 'react';
import BarChart from '../components/BarChart';
import LineChart from '../components/LineChart';
import { getKpiSummary, getKpiHistory } from '../services/api';

const Dashboard = () => {
    const [kpiData, setKpiData] = useState(null);
    const [timestamps, setTimestamps] = useState([]);
    const [oeeValues, setOeeValues] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isFetching, setIsFetching] = useState(false); // Singleton state flag

    useEffect(() => {
        const fetchData = async () => {
            if (!isFetching) {
                setIsFetching(true); // Set flag to true to prevent re-fetching
                try {
                    // Fetch KPI summary for the bar chart
                    const summary = await getKpiSummary();
                    console.log('KPI Summary Data:', summary); // Log fetched summary data
                    setKpiData([
                        summary.average_oee,
                        summary.average_downtime_percentage,
                        summary.average_utilization_percentage,
                        summary.average_yield_percentage,
                        summary.average_throughput,
                    ]);

                    // Fetch historical OEE data for the line chart
                    const history = await getKpiHistory();
                    console.log('Historical Data for Line Chart:', history); // Log fetched history data
                    setTimestamps(history.timestamps);
                    setOeeValues(history.values);

                    setLoading(false);
                } catch (error) {
                    console.error('Error fetching data:', error);
                    setLoading(false);
                }
            }
        };

        fetchData();
    }, [isFetching]); // Use the singleton flag to control fetching

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!kpiData || kpiData.length === 0) {
        return <div>No KPI data available. Please upload a file.</div>;
    }

    return (
        <div>
            <h1>Dashboard</h1>
            <h2>Bar Chart</h2>
            <BarChart data={kpiData} />
            <h2>Line Chart</h2>
            <LineChart timestamps={timestamps} values={oeeValues} />
        </div>
    );
};

export default Dashboard;
