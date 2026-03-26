import React from 'react';
import { ResumeData, ResumeStyle } from '../types/resume';
import styles from '../styles/resume.module.scss';

interface ResumePreviewPaneProps {
  data: ResumeData;
  style: ResumeStyle;
}

export default function ResumePreviewPane({ data, style, }: ResumePreviewPaneProps): JSX.Element {
  return (
    <div className={`${styles['resume-preview-pane']} ${styles[style.cssClass]}`}> 
      <div className={styles['preview-content']}> 
        <div className={styles['preview-header']}> 
          <h1 className={styles['preview-name']}>{data.personalInfo.fullName || 'Your Name'}</h1> 
          <div className={styles['preview-contact']}> 
            {data.personalInfo.email && <span>{data.personalInfo.email}</span>} 
            {data.personalInfo.phone && <span>{data.personalInfo.phone}</span>} 
            {data.personalInfo.location && <span>{data.personalInfo.location}</span>} 
            {data.personalInfo.linkedinUrl && ( 
              <a href={data.personalInfo.linkedinUrl} target="_blank" rel="noopener noreferrer"> 
                LinkedIn 
              </a> 
            )} 
          </div> 
        </div> 
        {data.summary && ( 
          <div className={styles['preview-section']}> 
            <h2 className={styles['preview-section-title']}>Professional Summary</h2> 
            <p className={styles['preview-text']}>{data.summary}</p> 
          </div> 
        )} 
        {data.workExperience.length > 0 && ( 
          <div className={styles['preview-section']}> 
            <h2 className={styles['preview-section-title']}>Work Experience</h2> 
            {data.workExperience.map((exp) => ( 
              <div key={exp.id} className={styles['preview-entry']}> 
                <div className={styles['entry-header']}> 
                  <h3 className={styles['entry-title']}>{exp.jobTitle || 'Job Title'}</h3> 
                  <span className={styles['entry-company']}>{exp.company || 'Company'}</span> 
                </div> 
                <div className={styles['entry-meta']}> 
                  {exp.location && <span>{exp.location}</span>} 
                  {exp.startDate && <span>{exp.startDate}</span>} 
                  {exp.endDate && <span>to {exp.endDate}</span>} 
                </div> 
                {exp.description && <p className={styles['entry-description']}>{exp.description}</p>} 
              </div> 
            ))} 
          </div> 
        )} 
        {data.education.length > 0 && ( 
          <div className={styles['preview-section']}> 
            <h2 className={styles['preview-section-title']}>Education</h2> 
            {data.education.map((edu) => ( 
              <div key={edu.id} className={styles['preview-entry']}> 
                <div className={styles['entry-header']}> 
                  <h3 className={styles['entry-title']}>{edu.degree || 'Degree'}</h3> 
                  <span className={styles['entry-company']}>{edu.institution || 'Institution'}</span> 
                </div> 
                <div className={styles['entry-meta']}> 
                  {edu.field && <span>{edu.field}</span>} 
                  {edu.graduationDate && <span>{edu.graduationDate}</span>} 
                </div> 
              </div> 
            ))} 
          </div> 
        )} 
        {data.skills.length > 0 && ( 
          <div className={styles['preview-section']}> 
            <h2 className={styles['preview-section-title']}>Skills</h2> 
            <div className={styles['skills-list']}> 
              {data.skills.map((skill) => ( 
                <span key={skill.id} className={styles['skill-tag']}> 
                  {skill.name || 'Skill'} 
                </span> 
              ))} 
            </div> 
          </div> 
        )} 
      </div> 
    </div> 
  ); 
}