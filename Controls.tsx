// import React from 'react';
import styles from './Controls.module.scss';

function Controls({ 
  onEmpty,
  onRegenerate,
  onNextStep,
  algorithm,
  setAlgorithm
}: {
  onEmpty: () => void;
  onRegenerate: () => void;
  onNextStep: () => void;
  algorithm: number;
  setAlgorithm: (value: number) => void;
}) {
  return (
    <div className={styles.controls}>
      <button onClick={onEmpty}>Empty Map</button>
      <button onClick={onRegenerate}>Regenerate Map</button>
      <button onClick={onNextStep}>Next Step</button>
      <select value={algorithm} onChange={(e) => setAlgorithm(Number(e.target.value))}>
        <option value={0}>Dijkstra</option>
        <option value={1}>A*</option>
        <option value={2}>Jump Point Search</option>
      </select>
    </div>
  );
}

export default Controls; 