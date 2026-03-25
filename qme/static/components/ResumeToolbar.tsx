import React, { useMemo } from 'react';
import { ResumeStyle } from '../types/resume';
import styles from '../styles/resume.module.scss';

interface ResumeToolbarProps {
  availableStyles: ResumeStyle[];
  selectedStyle: string;
  onStyleChange: (styleId: string) => void;
  onDownloadPDF: () => void;
  onShare: () => void;
}

export default function ResumeToolbar({
  availableStyles,
  selectedStyle,
  onStyleChange,
  onDownloadPDF,
  onShare,
}: ResumeToolbarProps): JSX.Element {
  const selectedStyleObj = useMemo(
    () => availableStyles.find((s) => s.id === selectedStyle),
    [availableStyles, selectedStyle]
  );

  return (
    <div className={styles['resume-toolbar']}> 
      <div className={styles['toolbar-section']}> 
        <label htmlFor="style-select" className={styles['style-label']}> 
          Template Style:
        </label>
        <select
          id="style-select"
          value={selectedStyle}
          onChange={(e) => onStyleChange(e.target.value)}
          className={styles['style-dropdown']}
          aria-label="Select resume style template"
        >
          {availableStyles.map((style) => (
            <option key={style.id} value={style.id}>
              {style.name} - {style.description}
            </option>
          ))}
        </select>
      </div>

      <div className={styles['toolbar-section']}> 
        <button
          onClick={onDownloadPDF}
          className={`${styles['toolbar-button']} ${styles['button-primary']}`}
          aria-label="Download resume as PDF"
        >
          📥 Download PDF
        </button>
        <button
          onClick={onShare}
          className={`${styles['toolbar-button']} ${styles['button-secondary']}`}
          aria-label="Share resume"
        >
          🔗 Share
        </button>
      </div>
    </div>
  );
}