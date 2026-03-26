import React, { useState, useCallback } from 'react';
import ResumeToolbar from './ResumeToolbar';
import ResumeDataPane from './ResumeDataPane';
import ResumePreviewPane from './ResumePreviewPane';
import { ResumeData, ResumeStyle } from '../types/resume';
import styles from '../styles/resume.module.scss';

const defaultResumeData: ResumeData = {
  personalInfo: {
    fullName: '',
    email: '',
    phone: '',
    location: '',
    linkedinUrl: '',
  },
  summary: '',
  workExperience: [],
  education: [],
  skills: [],
  certificates: [],
};

const RESUME_STYLES: Record<string, ResumeStyle> = {
  modern: {
    id: 'modern',
    name: 'Modern',
    description: 'Clean, contemporary design with accent colors',
    cssClass: 'resume-style-modern',
  },
  classic: {
    id: 'classic',
    name: 'Classic',
    description: 'Traditional, professional resume layout',
    cssClass: 'resume-style-classic',
  },
  creative: {
    id: 'creative',
    name: 'Creative',
    description: 'Bold, visually interesting design',
    cssClass: 'resume-style-creative',
  },
};

export default function ResumePage(): JSX.Element {
  const [resumeData, setResumeData] = useState<ResumeData>(defaultResumeData);
  const [selectedStyle, setSelectedStyle] = useState<string>('modern');

  const handleDataChange = useCallback((newData: ResumeData) => {
    setResumeData(newData);
  }, []);

  const handleStyleChange = useCallback((styleId: string) => {
    setSelectedStyle(styleId);
  }, []);

  const handleDownloadPDF = useCallback(() => {
    console.log('Downloading PDF with style:', selectedStyle);
    // PDF generation logic here
  }, [selectedStyle]);

  const handleShare = useCallback(() => {
    console.log('Sharing resume');
    // Share logic here
  }, []);

  return (
    <div className={styles['resume-page']}> 
      <ResumeToolbar
        availableStyles={Object.values(RESUME_STYLES)}
        selectedStyle={selectedStyle}
        onStyleChange={handleStyleChange}
        onDownloadPDF={handleDownloadPDF}
        onShare={handleShare}
      />
      <div className={styles['resume-container']}> 
        <ResumeDataPane
          data={resumeData}
          onChange={handleDataChange}
        />
        <ResumePreviewPane
          data={resumeData}
          style={RESUME_STYLES[selectedStyle]}
        />
      </div>
    </div>
  );
}
