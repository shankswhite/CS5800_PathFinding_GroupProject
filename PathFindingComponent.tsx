import { useState, useEffect } from 'react';
import '../../styles/global.scss';
import './PathFindingComponent.module.scss';
import styles from './PathFindingComponent.module.scss';

// import axios from 'axios';
import { pathFindingService } from '../../services/pathFindingService';

const GRID_SIZE = 50;

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
  const [obstacleCount, setObstacleCount] = useState<number>(GRID_SIZE);
  const [visitedCount, setVisitedCount] = useState<number>(0);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  useEffect(() => {
    const initializeGrid = async () => {
      try {
        const { map, pathInformation } = await pathFindingService.generateNewMap(0, GRID_SIZE);
        
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
        setVisitedCount(0);
      } else {
        console.error('Invalid map data received');
      }
    } catch (error) {
      console.error('Failed to regenerate map:', error);
    }
  };

  const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

  const nextStep = async () => {
    if (!pathInfo || currentStep >= pathInfo.length) {
      try {
        // Get new path info using current algorithm when previous steps are exhausted
        const response = await pathFindingService.generateNewMap(algorithm, obstacleCount);
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
          
          setGrid(processedMap);
          setPathInfo(response.pathInformation);
          setCurrentStep(0);
          setVisitedCount(0);
          return;
        }
      } catch (error) {
        console.error('Failed to get new path:', error);
      }
      console.log('No more steps available');
      return;
    }
    
    const currentLevelInfo = pathInfo[currentStep];
    const newGrid = grid.map(row => row.map(cell => ({...cell})));
    let newVisitedCount = visitedCount;
    
    // First check if this step contains the final path
    if (currentLevelInfo.finalPath) {
      currentLevelInfo.finalPath.forEach(([row, col]: number[]) => {
        if (newGrid[row][col].status !== 1 && newGrid[row][col].status !== 2) {
          newGrid[row][col].status = 5; // Final path - will be green
        }
      });
      setGrid(newGrid);
      setCurrentStep(prev => prev + 1);
      return;
    }

    // Change previous "next to visit" nodes (status 4) to visited (status 3)
    newGrid.forEach(row => {
      row.forEach(node => {
        if (node.status === 4) {
          node.status = 3; // Change from blue to orange
          // newVisitedCount++;
        }
      });
    });

    // Process regular step
    Object.entries(currentLevelInfo).forEach(([_, nodeInfo]: [string, any]) => {
      Object.keys(nodeInfo).forEach(coordStr => {
        const [row, col] = coordStr.split(',').map(Number);
        
        if (!isNaN(row) && !isNaN(col) && 
            row >= 0 && row < GRID_SIZE && 
            col >= 0 && col < GRID_SIZE) {
          
          if (newGrid[row][col].status !== 1 && 
              newGrid[row][col].status !== 2 && 
              newGrid[row][col].status !== 6) {
            newGrid[row][col].status = 3; // Visited
            newVisitedCount++;
          }
          
          const neighbors = nodeInfo[coordStr];
          if (Array.isArray(neighbors)) {
            neighbors.forEach(([nextRow, nextCol]) => {
              if (nextRow >= 0 && nextRow < GRID_SIZE && 
                  nextCol >= 0 && nextCol < GRID_SIZE) {
                if (newGrid[nextRow][nextCol].status === 6) {
                  newGrid[nextRow][nextCol].status = 7; // Blocked obstacle - will be red
                } else if (newGrid[nextRow][nextCol].status === 0) {
                  newGrid[nextRow][nextCol].status = 4; // Next to visit
                }
              }
            });
          }
        }
      });
    });
    
    setGrid(newGrid);
    setVisitedCount(newVisitedCount);
    setCurrentStep(prev => prev + 1);
  };

  const goToEnd = async () => {
    if (!pathInfo || pathInfo.length === 0) return;
    setIsProcessing(true);

    const newGrid = grid.map(row => row.map(cell => ({...cell})));
    let newVisitedCount = 0;

    // Faster processing for A*
    if (algorithm === 1) {  // A* algorithm
        // Process visited nodes in chunks for smoother animation
        const chunkSize = 5;  // Process 5 steps at once
        for (let i = 0; i < pathInfo.length; i += chunkSize) {
            const chunk = pathInfo.slice(i, i + chunkSize);
            
            for (const step of chunk) {
                if ('finalPath' in step) continue;
                
                Object.entries(step).forEach(([_, nodeInfo]: [string, any]) => {
                    Object.keys(nodeInfo).forEach(coordStr => {
                        const [row, col] = coordStr.split(',').map(Number);
                        if (newGrid[row][col].status !== 1 && 
                            newGrid[row][col].status !== 2 && 
                            newGrid[row][col].status !== 6) {
                            if (newGrid[row][col].status !== 3) {
                                newGrid[row][col].status = 3;
                                newVisitedCount++;
                            }
                        }
                    });
                });
            }
            
            setGrid([...newGrid]);
            setVisitedCount(newVisitedCount);
            await sleep(20);  // Shorter delay for A*
        }

        // Animate the final path with a moderate speed
        const finalPathStep = pathInfo[pathInfo.length - 1];
        if (finalPathStep && finalPathStep.finalPath) {
            for (const [row, col] of finalPathStep.finalPath) {
                if (newGrid[row][col].status !== 1 && 
                    newGrid[row][col].status !== 2) {
                    newGrid[row][col].status = 5;
                    setGrid([...newGrid]);
                    await sleep(30);  // Moderate delay for path animation
                }
            }
        }
    } else {
        // Original slower animation for Dijkstra
        for (const step of pathInfo) {
            if ('finalPath' in step) continue;

            Object.entries(step).forEach(([_, nodeInfo]: [string, any]) => {
                Object.keys(nodeInfo).forEach(coordStr => {
                    const [row, col] = coordStr.split(',').map(Number);
                    if (newGrid[row][col].status !== 1 && 
                        newGrid[row][col].status !== 2 && 
                        newGrid[row][col].status !== 6) {
                        if (newGrid[row][col].status !== 3) {
                            newGrid[row][col].status = 3;
                            newVisitedCount++;
                        }
                    }
                });
            });
            
            setGrid([...newGrid.map(row => [...row])]);
            setVisitedCount(newVisitedCount);
            await sleep(50);  // Original delay for Dijkstra
        }

        // Animate the path
        const finalPathStep = pathInfo[pathInfo.length - 1];
        if (finalPathStep && finalPathStep.finalPath) {
            for (const [row, col] of finalPathStep.finalPath) {
                if (newGrid[row][col].status !== 1 && 
                    newGrid[row][col].status !== 2) {
                    newGrid[row][col].status = 5;
                    setGrid([...newGrid.map(row => [...row])]);
                    await sleep(50);
                }
            }
        }
    }

    setCurrentStep(pathInfo.length);
    setIsProcessing(false);
  };

  // Add useEffect to watch for state changes
  useEffect(() => {
    if (isProcessing && currentStep < pathInfo?.length) {
      const timer = setTimeout(() => {
        nextStep();
      }, 200);
      return () => clearTimeout(timer);
    }
  }, [isProcessing, currentStep, grid]);

  useEffect(() => {
    return () => {
      setIsProcessing(false);
    };
  }, []);

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

  useEffect(() => {
    regenerateMap();
  }, [algorithm]); // Regenerate map whenever algorithm changes

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.mainContent}>
        <div className={styles['grid-container']}>
          {grid.map((row, rowIndex) => {
            // console.log(`Row ${rowIndex}:`, row.map(node => node.status));
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
          <div className={styles.selectWrapper}>
            <select 
              value={algorithm} 
              onChange={(e) => setAlgorithm(Number(e.target.value))}
            >
              <option value={0}>Dijkstra</option>
              <option value={1}>A*</option>
              <option value={2}>JPS</option>
            </select>
          </div>
          
          <div className={styles.inputGroup}>
            <div className={styles.inputWrapper}>
              <label htmlFor="obstacleCount">Obstacle Num:</label>
              <input
                id="obstacleCount"
                type="number"
                value={obstacleCount}
                onChange={(e) => setObstacleCount(Math.max(20, Math.min(200, parseInt(e.target.value) || 20)))}
                min="20"
                max="200"
              />
            </div>
          </div>

          <button onClick={regenerateMap}>Generate New Map</button>
          <button onClick={nextStep}>Next Step</button>
          <button 
            className={styles.endButton} 
            onClick={goToEnd}
            disabled={isProcessing}
          >
            Go to End
          </button>
          
          <div className={styles.stats}>
            Nodes Traversed: {visitedCount}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PathFindingComponent;