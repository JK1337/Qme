import React, { useCallback } from 'react';
import { ResumeData } from '../types/resume';
import styles from '../styles/resume.module.scss';

interface ResumDataPaneProps {
  data: ResumeData;
  onChange: (data: ResumeData) => void;
}

export default function ResumeDataPane({
  data,
  onChange,
}: ResumDataPaneProps): JSX.Element {
  const handlePersonalInfoChange = useCallback(
    (field: string, value: string) => {
      onChange({
        ...data,
        personalInfo: {
          ...data.personalInfo,
          [field]: value,
        },
      });
    },
    [data, onChange]
  );

  const handleSummaryChange = useCallback(
    (value: string) => {
      onChange({ ...data, summary: value });
    },
    [data, onChange]
  );

  const handleAddWorkExperience = useCallback(() => {
    onChange({
      ...data,
      workExperience: [
        ...data.workExperience,
        {
          id: Date.now().toString(),
          company: '',
          position: '',
          startDate: '',
          endDate: '',
          description: '',
          current: false,
        },
      ],
    });
  }, [data, onChange]);

  const handleAddEducation = useCallback(() => {
    onChange({
      ...data,
      education: [
        ...data.education,
        {
          id: Date.now().toString(),
          school: '',
          degree: '',
          field: '',
          graduationDate: '',
        },
      ],
    });
  }, [data, onChange]);

  const handleAddSkill = useCallback(() => {
    onChange({
      ...data,
      skills: [...data.skills, { id: Date.now().toString(), name: '', level: 'intermediate' }],
    });
  }, [data, onChange]);

  return (
    <div className={styles['resume-data-pane']}>  
      <div className={styles['form-section']}>  
        <h3>Personal Information</h3>  
        <input  
          type="text"  
          placeholder="Full Name"  
          value={data.personalInfo.fullName}  
          onChange={(e) => handlePersonalInfoChange('fullName', e.target.value)}  
          className={styles['form-input']}  
        />  
        <input  
          type="email"  
          placeholder="Email"  
          value={data.personalInfo.email}  
          onChange={(e) => handlePersonalInfoChange('email', e.target.value)}  
          className={styles['form-input']}  
        />
        <input  
          type="tel"  
          placeholder="Phone"  
          value={data.personalInfo.phone}  
          onChange={(e) => handlePersonalInfoChange('phone', e.target.value)}  
          className={styles['form-input']}  
        />  
        <input  
          type="text"  
          placeholder="Location"  
          value={data.personalInfo.location}  
          onChange={(e) => handlePersonalInfoChange('location', e.target.value)}  
          className={styles['form-input']}  
        />  
        <input  
          type="url"  
          placeholder="LinkedIn URL"  
          value={data.personalInfo.linkedinUrl}  
          onChange={(e) => handlePersonalInfoChange('linkedinUrl', e.target.value)}  
          className={styles['form-input']}  
        />  
      </div>  

      <div className={styles['form-section']}>  
        <h3>Professional Summary</h3>  
        <textarea  
          placeholder="Write a brief summary of your professional background..."  
          value={data.summary}  
          onChange={(e) => handleSummaryChange(e.target.value)}  
          className={styles['form-textarea']}  
          rows={4}  
        />  
      </div>  

      <div className={styles['form-section']}>  
        <h3>Work Experience</h3>  
        {data.workExperience.map((job, index) => (  
          <div key={job.id} className={styles['subsection']}>  
            <input  
              type="text"  
              placeholder="Company"  
              value={job.company}  
              className={styles['form-input']}  
            />  
            <input  
              type="text"  
              placeholder="Position"  
              value={job.position}  
              className={styles['form-input']}  
            />  
            <textarea  
              placeholder="Description"  
              value={job.description}  
              className={styles['form-textarea']}  
              rows={3}  
            />  
          </div>  
        ))}  
        <button onClick={handleAddWorkExperience} className={styles['add-button']}>  
          + Add Work Experience  
        </button>  
      </div>  

      <div className={styles['form-section']}>  
        <h3>Education</h3>  
        {data.education.map((edu) => (  
          <div key={edu.id} className={styles['subsection']}>  
            <input  
              type="text"  
              placeholder="School/University"  
              value={edu.school}  
              className={styles['form-input']}  
            />  
            <input  
              type="text"  
              placeholder="Degree"  
              value={edu.degree}  
              className={styles['form-input']}  
            />  
            <input  
              type="text"  
              placeholder="Field of Study"  
              value={edu.field}  
              className={styles['form-input']}  
            />  
          </div>  
        ))}  
        <button onClick={handleAddEducation} className={styles['add-button']}>  
          + Add Education  
        </button>  
      </div>  

      <div className={styles['form-section']}>  
        <h3>Skills</h3>  
        {data.skills.map((skill) => (  
          <div key={skill.id} className={styles['skill-entry']}>  
            <input  
              type="text"  
              placeholder="Skill name"  
              value={skill.name}  
              className={styles['form-input']}  
            />  
          </div>  
        ))}  
        <button onClick={handleAddSkill} className={styles['add-button']}>  
          + Add Skill  
        </button>  
      </div>  
    </div>
  );
}