import { useState, useEffect } from 'react';
import '../../styles/global.scss';
import './PathFindingComponent.module.scss';
import styles from './PathFindingComponent.module.scss';

// import axios from 'axios';
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
    const initializeGrid = async () => {
      try {
        const { map, pathInformation } = await pathFindingService.generateNewMap(0, 20);
        
        if (map && map.length > 0) {
          const processedMap = map.map((row: number[], rowIndex: number) =>
            row.map((status: number, colIndex: number) => ({
              row: rowIndex,
              col: colIndex,
              status: status, // Use the number directly as status
              distanceToStart: Infinity,
              distanceToEnd: Infinity
            }))
          );
          
          setGrid(processedMap);
          setPathInfo(pathInformation);
        } else {
          setGrid(createInitialGrid());
        }
        setIsLoading(false);
      } catch (error) {
        console.error('Failed to initialize grid:', error);
        setGrid(createInitialGrid());
        setIsLoading(false);
      }
    };

    initializeGrid();
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
          distanceToStart: Infinity,
          distanceToEnd: Infinity,
        });
      }
      initialGrid.push(currentRow);
    }
    return initialGrid;
  }

  const regenerateMap = async () => {
    try {
      const response = await pathFindingService.generateNewMap(algorithm, obstacleCount);
      console.log('Backend response:', response);
      
      if (response.map && response.map.length > 0) {
        const processedMap = response.map.map((row: number[], rowIndex: number) =>
          row.map((status: number, colIndex: number) => ({
            row: rowIndex,
            col: colIndex,
            status: status,
            distanceToStart: Infinity,
            distanceToEnd: Infinity
          }))
        );
        
        console.log('Processed map:', processedMap);
        setGrid(processedMap);
        setPathInfo(response.pathInformation);
        setCurrentStep(0);
      } else {
        console.error('Invalid map data received');
      }
    } catch (error) {
      console.error('Failed to regenerate map:', error);
    }
  };

  const nextStep = () => {
    if (!pathInfo || currentStep >= pathInfo.length) {
      console.log('No more steps available');
      return;
    }
    
    const currentLevelInfo = pathInfo[currentStep];
    console.log('Processing level info:', currentLevelInfo);
    
    const newGrid = grid.map(row => row.map(cell => ({...cell})));  // Deep copy
    
    // Process each position in the current level
    Object.keys(currentLevelInfo).forEach(pos => {
      const [row, col] = pos.split(',').map(Number);
      
      // Mark the current position as visited
      if (row >= 0 && row < GRID_SIZE && col >= 0 && col < GRID_SIZE) {
        if (newGrid[row][col].status !== 1 && newGrid[row][col].status !== 2) {
          newGrid[row][col].status = 3; // Visited
        }
      }
      
      // Mark the neighbors as next to visit
      const neighbors = currentLevelInfo[pos];
      if (Array.isArray(neighbors)) {
        neighbors.forEach(neighbor => {
          const [nextRow, nextCol] = neighbor;
          if (nextRow >= 0 && nextRow < GRID_SIZE && 
              nextCol >= 0 && nextCol < GRID_SIZE && 
              newGrid[nextRow][nextCol].status === 0) {
            newGrid[nextRow][nextCol].status = 4; // Next to visit
          }
        });
      }
    });
    
    setGrid(newGrid);
    setCurrentStep(prev => prev + 1);
  };

  const getNodeClassName = (node: NodeType) => {
    const baseClass = styles.node;
    
    switch (node.status) {
      case 0:
        return `${baseClass} ${styles.nodeEmpty}`;
      case 1:
        return `${baseClass} ${styles.nodeStart}`;
      case 2:
        return `${baseClass} ${styles.nodeEnd}`;
      case 3:
        return `${baseClass} ${styles.nodeVisited}`;
      case 4:
        return `${baseClass} ${styles.nodeNext}`;
      case 5:
        return `${baseClass} ${styles.nodePath}`;
      case 6:
        return `${baseClass} ${styles.nodeObstacle}`;
      case 7:
        return `${baseClass} ${styles.nodeBlock}`;
      default:
        return `${baseClass} ${styles.nodeEmpty}`;
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.mainContent}>
        <div className={styles['grid-container']}>
          {grid.map((row, rowIndex) => {
            console.log(`Row ${rowIndex}:`, row.map(node => node.status));
            return (
              <div key={rowIndex} className={styles.row}>
                {row.map((node, nodeIndex) => (
                  <div
                    key={`${rowIndex}-${nodeIndex}`}
                    className={getNodeClassName(node)}
                  />
                ))}
              </div>
            );
          })}
        </div>
        
        <div className={styles.controls}>
          <button onClick={regenerateMap}>Generate New Map</button>
          <button onClick={nextStep}>Next Step</button>
          <div className={styles.inputGroup}>
            <div className={styles.inputWrapper}>
              <label htmlFor="obstacleCount">Obstacle Num:</label>
              <input
                id="obstacleCount"
                type="number"
                value={obstacleCount}
                onChange={(e) => setObstacleCount(Math.max(0, Math.min(200, parseInt(e.target.value) || 0)))}
                min="0"
                max="200"
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
    </div>
  );
}

export default PathFindingComponent;