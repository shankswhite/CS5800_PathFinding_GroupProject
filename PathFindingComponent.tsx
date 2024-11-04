import React, { useState, useEffect } from 'react';
import '../../styles/global.scss';
import './PathFindingComponent.module.scss';
import styles from './PathFindingComponent.module.scss';

import axios from 'axios'; // Assuming you are using axios for API requests

const GRID_SIZE = 20;

function PathFindingComponent() {
  const [grid, setGrid] = useState(createInitialGrid());
  const [isLoading, setIsLoading] = useState(true);

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
    const initialGrid = [];
    for (let row = 0; row < GRID_SIZE; row++) {
      const currentRow = [];
      for (let col = 0; col < GRID_SIZE; col++) {
        currentRow.push({
          row,
          col,
          isStart: row === 0 && col === 0,
          isEnd: row === GRID_SIZE - 1 && col === GRID_SIZE - 1,
          isObstacle: false,
          isVisited: false,
          isNext: false,
          currentPosition: false,
        });
      }
      initialGrid.push(currentRow);
    }
    return initialGrid;
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles['grid-container']}>
      {grid.length > 0 && grid.map((row, rowIndex) => (
        <div key={rowIndex} className={styles.row}>
          {row.map((node, nodeIndex) => {
            const { isStart, isEnd, isObstacle, isVisited, isNext, currentPosition } = node;
            const extraClassName = isStart
              ? 'node-start'
              : isEnd
              ? 'node-end'
              : isObstacle
              ? 'node-obstacle'
              : isVisited
              ? 'node-visited'
              : isNext
              ? 'node-next'
              : currentPosition
              ? 'node-current'
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
  );
}

export default PathFindingComponent;