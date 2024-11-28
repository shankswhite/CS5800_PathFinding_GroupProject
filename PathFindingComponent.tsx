import { useState, useEffect, useRef } from 'react';
import '../../styles/global.scss';
import './PathFindingComponent.module.scss';
import styles from './PathFindingComponent.module.scss';
import GlowingButton from '../common/GlowingButton';

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

// Add this function before the PathFindingComponent
function convertToOrthogonalPath(path: number[][]): number[][] {
  if (!path || path.length === 0) return [];
  return path;
}

function PathFindingComponent() {
  const [grid, setGrid] = useState(createInitialGrid());
  const [isLoading, setIsLoading] = useState(true);
  const [algorithm, setAlgorithm] = useState<number>(0); // 0: Dijkstra, 1: A*, 2: JPS
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [pathInfo, setPathInfo] = useState<any>(null);
  const [obstacleCount, setObstacleCount] = useState<number>(GRID_SIZE);
  const [visitedCount, setVisitedCount] = useState<number>(0);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [isMuted, setIsMuted] = useState(true);  // Start muted by default
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Update the useEffect for audio
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = 0.3;
      audioRef.current.loop = true;
      // Don't autoplay
      audioRef.current.pause();
    }
  }, []); // Empty dependency array means this runs once on mount

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
      console.log('PathInfo received:', response.pathInformation);
      
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
        
        console.log('Initial map status counts:', 
          processedMap.flat().reduce((acc: Record<number, number>, node: NodeType) => {
            acc[node.status] = (acc[node.status] || 0) + 1;
            return acc;
          }, {})
        );
        
        setGrid(processedMap);
        setPathInfo(response.pathInformation);
        setCurrentStep(0);
        setVisitedCount(0);
      }
    } catch (error) {
      console.error('Failed to regenerate map:', error);
    }
  };

  const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

  const nextStep = async () => {
    if (!pathInfo || currentStep >= pathInfo.length) {
      return;
    }
    
    const currentLevelInfo = pathInfo[currentStep];
    const newGrid = grid.map(row => row.map(cell => ({...cell})));
    let newVisitedCount = visitedCount;

    // First check if this step contains the final path
    if (currentLevelInfo.finalPath) {
      // ... existing finalPath code ...
      return;
    }

    // Process regular step
    Object.entries(currentLevelInfo).forEach(([_, nodeInfo]: [string, any]) => {
      Object.keys(nodeInfo).forEach(coordStr => {
        const [row, col] = coordStr.split(',').map(Number);
        
        if (!isNaN(row) && !isNaN(col) && 
            row >= 0 && row < GRID_SIZE && 
            col >= 0 && col < GRID_SIZE) {
          
          // First mark current node as visited
          if (newGrid[row][col].status !== 1 && 
              newGrid[row][col].status !== 2 && 
              newGrid[row][col].status !== 6) {
            if (newGrid[row][col].status === 4) {
              newGrid[row][col].status = 3;
              newVisitedCount++;  // Increment count when converting from next to visited
            } else if (newGrid[row][col].status === 0) {
              newGrid[row][col].status = 3;
              newVisitedCount++;  // Increment count for newly visited nodes
            }
          }
          
          // Then process its neighbors
          const neighbors = nodeInfo[coordStr];
          if (Array.isArray(neighbors)) {
            neighbors.forEach(([nextRow, nextCol]) => {
              if (nextRow >= 0 && nextRow < GRID_SIZE && 
                  nextCol >= 0 && nextCol < GRID_SIZE) {
                if (newGrid[nextRow][nextCol].status === 6) {
                  newGrid[nextRow][nextCol].status = 7;
                } else if (newGrid[nextRow][nextCol].status === 0) {
                  newGrid[nextRow][nextCol].status = 4;  // Set next nodes
                }
              }
            });
          }
        }
      });
    });
    
    setGrid(newGrid);
    setVisitedCount(newVisitedCount);  // Update the visited count
    setCurrentStep(prev => prev + 1);
  };

  const goToEnd = async () => {
    if (!pathInfo || pathInfo.length === 0) return;
    setIsProcessing(true);
  
    const newGrid = grid.map(row => row.map(cell => ({ ...cell })));
    let newVisitedCount = visitedCount;
    const animationDelay = algorithm === 1 ? 2 : 50;
  
    // Process steps except the last one
    for (let step = currentStep; step < pathInfo.length - 1; step++) {
      const currentLevelInfo = pathInfo[step];
      Object.entries(currentLevelInfo).forEach(([_, nodeInfo]: [string, any]) => {
        Object.keys(nodeInfo).forEach(coordStr => {
          const [row, col] = coordStr.split(',').map(Number);
  
          if (
            !isNaN(row) &&
            !isNaN(col) &&
            row >= 0 &&
            row < GRID_SIZE &&
            col >= 0 &&
            col < GRID_SIZE
          ) {
            if (
              newGrid[row][col].status !== 1 &&
              newGrid[row][col].status !== 2 &&
              newGrid[row][col].status !== 6
            ) {
              if (newGrid[row][col].status === 4) {
                newGrid[row][col].status = 3;
                newVisitedCount++;
              } else if (newGrid[row][col].status === 0) {
                newGrid[row][col].status = 3;
                newVisitedCount++;
              }
            }
  
            const neighbors = nodeInfo[coordStr];
            if (Array.isArray(neighbors)) {
              neighbors.forEach(([nextRow, nextCol]) => {
                if (
                  nextRow >= 0 &&
                  nextRow < GRID_SIZE &&
                  nextCol >= 0 &&
                  nextCol < GRID_SIZE
                ) {
                  if (newGrid[nextRow][nextCol].status === 6) {
                    newGrid[nextRow][nextCol].status = 7;
                  } else if (newGrid[nextRow][nextCol].status === 0) {
                    newGrid[nextRow][nextCol].status = 4;
                  }
                }
              });
            }
          }
        });
      });
  
      setGrid([...newGrid.map(row => [...row])]);
      setVisitedCount(newVisitedCount);
      await sleep(animationDelay);
    }
  
    // Animate the final path
    const finalPathStep = pathInfo[pathInfo.length - 1];
    if (finalPathStep && finalPathStep.finalPath) {
      // Clear previous 'next' nodes
      newGrid.forEach(row => {
        row.forEach(node => {
          if (node.status === 4) {
            node.status = 3;
          }
        });
      });

      const optimizedPath = convertToOrthogonalPath(finalPathStep.finalPath);
      
      for (const [row, col] of optimizedPath) {
        // Only draw path on valid cells (not obstacles or blocks)
        if (newGrid[row][col].status !== 6 && 
            newGrid[row][col].status !== 7 && 
            newGrid[row][col].status !== 1 && 
            newGrid[row][col].status !== 2) {
          newGrid[row][col].status = 5;
          setGrid([...newGrid.map(row => [...row])]);
          await sleep(animationDelay);
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

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = 0.3;
      audioRef.current.loop = true;
      // Don't autoplay
      audioRef.current.pause();
    }
  }, []);

  const toggleMusic = () => {
    if (audioRef.current) {
      if (isMuted) {
        audioRef.current.play().catch(error => {
          console.log('Audio playback failed:', error);
        });
      } else {
        audioRef.current.pause();
      }
      setIsMuted(!isMuted);
    }
  };

  useEffect(() => {
    console.log('PathInfo updated:', pathInfo);
  }, [pathInfo]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.container}>
      <audio 
        ref={audioRef} 
        src="/audio/algorithm-music.mp3" 
        preload="auto"  // Preload the audio
        loop  // Add loop attribute
      />
      
      <div className={styles.mainContent}>
        <div className={styles['grid-container']}>
          {grid.map((row, rowIndex) => {
            // console.log(`Row ${rowIndex}:`, row.map(node => node.status));
            return (
              <div key={rowIndex} className={styles.row}>
                {row.map((node, nodeIndex) => {
                  // Add inline styles for status 4 nodes
                  const inlineStyle = node.status === 4 ? {
                    backgroundColor: '#00f',
                    border: '2px solid yellow',
                    zIndex: 10,
                    position: 'relative' as const,
                    boxShadow: '0 0 10px blue'
                  } : undefined;

                  return (
                    <div
                      key={`${rowIndex}-${nodeIndex}`}
                      className={getNodeClassName(node)}
                      style={inlineStyle}
                      onClick={() => console.log(`Clicked node at [${rowIndex},${nodeIndex}] with status: ${node.status}`)}
                    />
                  );
                })}
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
              <button 
                className={styles.musicToggle}
                onClick={toggleMusic}
                aria-label="Toggle music"
              >
                {isMuted ? '🔇' : '🔊'}
              </button>
            </div>
          </div>

          <GlowingButton 
            color="#ff6b6b"  // Matching your original red color
            onClick={regenerateMap}
          >
            Generate New Map
          </GlowingButton>

          <GlowingButton 
            color="#2ecc71"  // Matching your original green color
            onClick={() => {
              console.log('Next Step button clicked');
              console.log('Current step:', currentStep);
              console.log('PathInfo:', pathInfo);
              nextStep();
            }}
          >
            Next Step
          </GlowingButton>

          <GlowingButton 
            color="#9c27b0"  // Matching your original purple color
            onClick={goToEnd}
            disabled={isProcessing}
          >
            Go to End
          </GlowingButton>
          
          <div className={styles.stats}>
            Nodes Traversed: {visitedCount}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PathFindingComponent;