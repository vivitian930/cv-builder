import json
from pydantic import BaseModel
from typing import List, Optional


class PersonalInfo(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]

class Education(BaseModel):
    degree: Optional[str]
    university: Optional[str]
    graduation_date: Optional[str]

class WorkExperience(BaseModel):
    company: Optional[str]
    position: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    summary: Optional[str]
    bullet_points: Optional[List[str]]

class ResearchExperience(BaseModel):
    organization: Optional[str]
    position: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    summary: Optional[str]
    bullet_points: Optional[List[str]]

class ProjectExperience(BaseModel):
    name: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    summary: Optional[str]
    bullet_points: Optional[List[str]]

class Resume(BaseModel):
    personal_info: Optional[PersonalInfo]
    education: Optional[List[Education]]
    work_experience: Optional[List[WorkExperience]]
    research_experience: Optional[List[ResearchExperience]]
    project_experience: Optional[List[ProjectExperience]]
    personal_statement: Optional[str]

