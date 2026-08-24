from typing import List, Optional

from pydantic import BaseModel, Field


class Requirement(BaseModel):
    id: str
    description: str
    priority: str = "Medium"
    category: str = "Functional"


class RequirementAnalysis(BaseModel):
    project_summary: str
    requirements: List[Requirement] = Field(default_factory=list)

    user_roles: List[str] = Field(default_factory=list)

    integrations: List[str] = Field(default_factory=list)

    security_requirements: List[str] = Field(default_factory=list)

    data_requirements: List[str] = Field(default_factory=list)

    non_functional_requirements: List[str] = Field(
        default_factory=list
    )

    assumptions: List[str] = Field(default_factory=list)

    open_questions: List[str] = Field(default_factory=list)


class ArchitectureComponent(BaseModel):
    name: str

    technology: str

    responsibility: str

    alternatives: List[str] = Field(
        default_factory=list
    )

    rationale: str


class Architecture(BaseModel):
    project_summary: str

    architecture_style: str

    components: List[ArchitectureComponent] = Field(
        default_factory=list
    )

    data_flow: List[str] = Field(
        default_factory=list
    )

    integrations: List[str] = Field(
        default_factory=list
    )

    security_considerations: List[str] = Field(
        default_factory=list
    )

    scalability_considerations: List[str] = Field(
        default_factory=list
    )

    assumptions: List[str] = Field(
        default_factory=list
    )

    open_questions: List[str] = Field(
        default_factory=list
    )


class TechnologyRecommendation(BaseModel):
    category: str

    technology: str

    description: str

    alternatives: List[str] = Field(
        default_factory=list
    )

    rationale: str

    risks: List[str] = Field(
        default_factory=list
    )


class TechnologyStack(BaseModel):
    recommendations: List[
        TechnologyRecommendation
    ] = Field(default_factory=list)


class ValidationResult(BaseModel):
    overall_status: str

    strengths: List[str] = Field(
        default_factory=list
    )

    issues: List[str] = Field(
        default_factory=list
    )

    missing_requirements: List[str] = Field(
        default_factory=list
    )

    risks: List[str] = Field(
        default_factory=list
    )

    recommendations: List[str] = Field(
        default_factory=list
    )


class FinalArchitecture(BaseModel):
    project_summary: str

    architecture: Architecture

    technology_stack: TechnologyStack

    validation: ValidationResult

    developer_feedback: Optional[str] = None

    change_summary: List[str] = Field(
        default_factory=list
    )
