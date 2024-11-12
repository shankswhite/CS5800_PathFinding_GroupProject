import { useState, useEffect } from 'react';
import '../../styles/global.scss';
import './PathFindingComponent.module.scss';
import styles from './PathFindingComponent.module.scss';

import axios from 'axios';
import { pathFindingService } from '../../services/pathFindingService';

const GRID_SIZE = 20;

interface NodeType {
  row: number;
  col: number;
  status: number;
  distanceToStart?: number;
  distanceToEnd?: number;
}

// const STATUS_COLORS = {
//   0: 'white',    // Empty
//   1: 'red',      // Start
//   2: 'green',    // End
//   3: 'orange',   // Visited
//   4: 'blue',     // Next
//   5: 'yellow',   // Final Path
//   6: 'gray',     // Obstacle
//   7: 'black',    // Block
// };

function PathFindingComponent() {
  const [grid, setGrid] = useState(createInitialGrid());
  const [isLoading, setIsLoading] = useState(true);
  const [algorithm, setAlgorithm] = useState<number>(0); // 0: Dijkstra, 1: A*, 2: JPS
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [pathInfo, setPathInfo] = useState<any>(null);
  const [obstacleCount, setObstacleCount] = useState<number>(20);

  useEffect(() => {
    // Fetch initial grid state from backend
    axios.get('https://your-backend-endpoint.com/get-grid').then(response => {
      setGrid(response.data.grid);
      setIsLoading(false);
    }).catch(() => {
      // If there's an error or no response, keep displaying the default grid
      setIsLoading(false);
    });
  }, []);

  function createInitialGrid() {
    const initialGrid: NodeType[][] = [];
    for (let row = 0; row < GRID_SIZE; row++) {
      const currentRow: NodeType[] = [];
      for (let col = 0; col < GRID_SIZE; col++) {
        currentRow.push({
          row,
          col,
          status: (row === 0 && col === 0) ? 1 : // Start
                  (row === GRID_SIZE - 1 && col === GRID_SIZE - 1) ? 2 : // End
                  0, // Empty
        });
      }
      initialGrid.push(currentRow);
    }
    return initialGrid;
  }

  const emptyMap = () => {
    const newGrid = grid.map(row =>
      row.map(node => ({ ...node, status: 0 }))
    );
    setGrid(newGrid);
    setCurrentStep(0);
  };

  const regenerateMap = async () => {
    try {
      const { map, pathInformation } = await pathFindingService.generateNewMap(algorithm, obstacleCount);
      setGrid(map);
      setPathInfo(pathInformation);
      setCurrentStep(0);
    } catch (error) {
      console.error('Failed to regenerate map:', error);
    }
  };

  const nextStep = () => {
    if (!pathInfo || currentStep >= pathInfo.length) return;
    
    const newGrid = [...grid];
    const currentStepInfo = pathInfo[currentStep];
    
    // Update visited and next nodes based on currentStepInfo
    Object.entries(currentStepInfo).forEach(([position, nextNodes]: [string, any]) => {
      const [row, col] = position.split(',').map(Number);
      newGrid[row][col].status = 3; // Mark as visited
      nextNodes.forEach(([nextRow, nextCol]: number[]) => {
        if (newGrid[nextRow][nextCol].status === 0) {
          newGrid[nextRow][nextCol].status = 4; // Mark as next
        }
      });
    });
    
    setGrid(newGrid);
    setCurrentStep(prev => prev + 1);
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles['grid-container']}>
        {grid.length > 0 && grid.map((row, rowIndex) => (
          <div key={rowIndex} className={styles.row}>
            {row.map((node, nodeIndex) => {
              const extraClassName = node.status === 1
                ? 'node-start'
                : node.status === 2
                ? 'node-end'
                : node.status === 3
                ? 'node-visited'
                : node.status === 4
                ? 'node-next'
                : node.status === 6
                ? 'node-obstacle'
                : '';
              return (
                <div
                  key={nodeIndex}
                  className={`${styles.node} ${styles[extraClassName]}`}
                ></div>
              );
            })}
          </div>
        ))}
      </div>
      
      <div className={styles.controls}>
        <button onClick={emptyMap}>Clear Map</button>
        <button onClick={regenerateMap}>Generate New Map</button>
        <button onClick={nextStep}>Next Step</button>
        <div className={styles.inputGroup}>
          <div className={styles.inputWrapper}>
            <label htmlFor="obstacleCount">Obstacle Nums:</label>
            <input
              id="obstacleCount"
              type="number"
              value={obstacleCount}
              onChange={(e) => setObstacleCount(Math.max(0, Math.min(200, parseInt(e.target.value) || 0)))}
              min="0"
              max="200"
              className={styles.obstacleInput}
            />
          </div>
          <select 
            value={algorithm} 
            onChange={(e) => setAlgorithm(Number(e.target.value))}
          >
            <option value={0}>Dijkstra</option>
            <option value={1}>A*</option>
            <option value={2}>JPS</option>
          </select>
        </div>
      </div>
    </div>
  );
}

export default PathFindingComponent;