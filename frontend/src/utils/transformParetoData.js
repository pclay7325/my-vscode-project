export function transformParetoData(data, metric) {
  if (!data || data.length === 0) {
    console.warn('No data provided for transformation.');
    return [];
  }

  console.log('Raw Data:', data);
  console.log('Metric:', metric);

  // Filter out rows where the metric or file_id is missing
  const validData = data.filter(
    (item) => item[metric] !== undefined && item[metric] !== null && item.file_id
  );

  if (validData.length === 0) {
    console.warn(`No valid rows found for metric "${metric}".`);
    return [];
  }

  const sortedData = validData.sort((a, b) => b[metric] - a[metric]);

  const totalMetricValue = sortedData.reduce((sum, item) => sum + item[metric], 0);
  let cumulativeSum = 0;

  const transformedData = sortedData.map((item) => {
    cumulativeSum += item[metric];
    return {
      file_id: item.file_id,
      value: item[metric],
      cumulativePercent: (cumulativeSum / totalMetricValue) * 100,
    };
  });

  console.log('Transformed Pareto Data:', transformedData);
  return transformedData;
}
