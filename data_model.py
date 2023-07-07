import json
from pydantic import BaseModel
from typing import List, Optional

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str

class Education(BaseModel):
    degree: str
    university: str
    graduation_date: str

class WorkExperience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: str
    summary: str
    bullet_points: List[str]

class ResearchExperience(BaseModel):
    organization: str
    position: str
    start_date: str
    end_date: str
    summary: str
    bullet_points: List[str]

class ProjectExperience(BaseModel):
    name: str
    start_date: str
    end_date: str
    summary: str
    bullet_points: List[str]

class Resume(BaseModel):
    personal_info: Optional[PersonalInfo]
    education: Optional[List[Education]]
    work_experience: Optional[List[WorkExperience]]
    research_experience: Optional[List[ResearchExperience]]
    project_experience: Optional[List[ProjectExperience]]
    personal_statement: Optional[str]

