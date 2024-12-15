import React from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import ChartjsParetoChart from './ChartjsParetoChart';
import BarChartComponent from './BarChartComponent';
import PieChartComponent from './PieChartComponent';
import LineChartComponent from './LineChartComponent';

function ChartGrid({ paretoData, filteredData, chartOrder, setChartOrder }) {
  const handleDragEnd = (result) => {
    const { source, destination } = result;

    if (!destination) return;

    const reordered = [...chartOrder];
    const [removed] = reordered.splice(source.index, 1);
    reordered.splice(destination.index, 0, removed);

    setChartOrder(reordered);
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <Droppable droppableId="charts">
        {(provided) => (
          <div
            {...provided.droppableProps}
            ref={provided.innerRef}
            style={{ display: 'grid', gap: '20px', gridTemplateColumns: '1fr' }}
          >
            {chartOrder.map((chart, index) => (
              <Draggable key={chart} draggableId={chart} index={index}>
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                    style={{
                      ...provided.draggableProps.style,
                      padding: '20px',
                      border: '1px solid #ccc',
                      borderRadius: '5px',
                      backgroundColor: '#fff',
                      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                    }}
                  >
                    <h3>{chart}</h3>
                    {chart === 'Pareto Chart' && <ChartjsParetoChart data={paretoData} />}
                    {chart === 'Bar Chart' && <BarChartComponent data={filteredData} />}
                    {chart === 'Pie Chart' && <PieChartComponent data={filteredData} />}
                    {chart === 'Line Chart' && <LineChartComponent data={filteredData} />}
                  </div>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
}

export default ChartGrid;
