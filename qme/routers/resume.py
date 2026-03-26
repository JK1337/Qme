from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from .database import get_db, Resume as ResumeModel

app = FastAPI()

class Resume(BaseModel):
    id: Optional[int]
    name: str
    content: str

@app.get("/resumes", response_model=List[Resume])
def read_resumes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    resumes = db.query(ResumeModel).offset(skip).limit(limit).all()
    return resumes

@app.post("/resumes", response_model=Resume)
def create_resume(resume: Resume, db: Session = Depends(get_db)):
    db_resume = ResumeModel(**resume.dict())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

@app.get("/resumes/{resume_id}", response_model=Resume)
def read_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(ResumeModel).filter(ResumeModel.id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@app.put("/resumes/{resume_id}", response_model=Resume)
def update_resume(resume_id: int, resume: Resume, db: Session = Depends(get_db)):
    db_resume = db.query(ResumeModel).filter(ResumeModel.id == resume_id)
    if db_resume.first() is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    db_resume.update(resume.dict())
    db.commit()
    return db_resume.first()

@app.delete("/resumes/{resume_id}")
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    db_resume = db.query(ResumeModel).filter(ResumeModel.id == resume_id)
    if db_resume.first() is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    db_resume.delete()
    db.commit()
    return {"detail": "Resume deleted"}

@app.post("/resumes/{resume_id}/pdf")
def generate_pdf(resume_id: int, db: Session = Depends(get_db)):
    # Logic to generate PDF
    return {"detail": "PDF generated"}

@app.post("/resumes/{resume_id}/share")
def create_share_link(resume_id: int, db: Session = Depends(get_db)):
    # Logic to create share link
    return {"detail": "Share link created"}

@app.post("/resumes/{resume_id}/rewrite")
def ai_rewrite(resume_id: int, db: Session = Depends(get_db)):
    # Logic to rewrite resume using AI
    return {"detail": "Resume rewritten"}
