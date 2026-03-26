from pydantic import BaseModel, EmailStr

class PersonalInfo(BaseModel):
    name: str
    email: EmailStr
    phone: str

class Education(BaseModel):
    institution: str
    degree: str
    start_year: int
    end_year: int

class Experience(BaseModel):
    company: str
    title: str
    start_date: str  # Use ISO format: YYYY-MM-DD
    end_date: str  # Use ISO format: YYYY-MM-DD
    description: str

class Skill(BaseModel):
    name: str
    proficiency: str  # e.g., 'beginner', 'intermediate', 'expert'

class Resume(BaseModel):
    personal_info: PersonalInfo
    education: list[Education]
    experience: list[Experience]
    skills: list[Skill]  
