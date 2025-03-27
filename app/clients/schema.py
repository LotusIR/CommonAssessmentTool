"""
Pydantic models for data validation and serialization.
Defines schemas for client data, predictions, and API responses.
"""

# Standard library imports
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import IntEnum
from app.models import Client


# Enums for validation
class Gender(IntEnum):
    MALE = 1
    FEMALE = 2


class PredictionInput(BaseModel):
    """
    Schema for prediction input data containing all client assessment fields.
    Used for making predictions about client outcomes.
    """

    age: int
    gender: str
    work_experience: int
    canada_workex: int
    dep_num: int
    canada_born: str
    citizen_status: str
    level_of_schooling: str
    fluent_english: str
    reading_english_scale: int
    speaking_english_scale: int
    writing_english_scale: int
    numeracy_scale: int
    computer_scale: int
    transportation_bool: str
    caregiver_bool: str
    housing: str
    income_source: str
    felony_bool: str
    attending_school: str
    currently_employed: str
    substance_use: str
    time_unemployed: int
    need_mental_health_support_bool: str

    @classmethod
    def from_client_response(cls, client):
        def bool_to_str(val: bool) -> str:
            return "1" if val else "0"

        return cls(
            age=client.age,
            gender=bool_to_str(client.gender),
            work_experience=client.work_experience,
            canada_workex=client.canada_workex,
            dep_num=client.dep_num,
            canada_born=bool_to_str(client.canada_born),
            citizen_status=bool_to_str(client.citizen_status),
            level_of_schooling=str(client.level_of_schooling),
            fluent_english=bool_to_str(client.fluent_english),
            reading_english_scale=client.reading_english_scale,
            speaking_english_scale=client.speaking_english_scale,
            writing_english_scale=client.writing_english_scale,
            numeracy_scale=client.numeracy_scale,
            computer_scale=client.computer_scale,
            transportation_bool=bool_to_str(client.transportation_bool),
            caregiver_bool=bool_to_str(client.caregiver_bool),
            housing=str(client.housing),
            income_source=str(client.income_source),
            felony_bool=bool_to_str(client.felony_bool),
            attending_school=bool_to_str(client.attending_school),
            currently_employed=bool_to_str(client.currently_employed),
            substance_use=bool_to_str(client.substance_use),
            time_unemployed=client.time_unemployed,
            need_mental_health_support_bool=bool_to_str(
                client.need_mental_health_support_bool
            ),
        )


class ClientBase(BaseModel):
    age: int = Field(ge=18, description="Age of client, must be 18 or older")
    gender: Gender = Field(description="Gender: 1 for male, 2 for female")
    work_experience: int = Field(ge=0, description="Years of work experience")
    canada_workex: int = Field(ge=0, description="Years of Canadian work experience")
    dep_num: int = Field(ge=0, description="Number of dependents")
    canada_born: bool = Field(description="Whether client was born in Canada")
    citizen_status: bool = Field(description="Client's citizenship status")
    level_of_schooling: int = Field(ge=1, le=14, description="Education level (1-14)")
    fluent_english: bool = Field(description="English fluency status")
    reading_english_scale: int = Field(
        ge=0, le=10, description="English reading level (0-10)"
    )
    speaking_english_scale: int = Field(
        ge=0, le=10, description="English speaking level (0-10)"
    )
    writing_english_scale: int = Field(
        ge=0, le=10, description="English writing level (0-10)"
    )
    numeracy_scale: int = Field(ge=0, le=10, description="Numeracy skill level (0-10)")
    computer_scale: int = Field(ge=0, le=10, description="Computer skill level (0-10)")
    transportation_bool: bool = Field(description="Has transportation")
    caregiver_bool: bool = Field(description="Is a caregiver")
    housing: int = Field(ge=1, le=10, description="Housing situation (1-10)")
    income_source: int = Field(ge=1, le=11, description="Source of income (1-11)")
    felony_bool: bool = Field(description="Has felony record")
    attending_school: bool = Field(description="Currently attending school")
    currently_employed: bool = Field(description="Current employment status")
    substance_use: bool = Field(description="Substance use status")
    time_unemployed: int = Field(ge=0, description="Time unemployed in months")
    need_mental_health_support_bool: bool = Field(
        description="Needs mental health support"
    )
    current_model: str = Field(description="the currently using ML model")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 25,
                "gender": 1,
                "work_experience": 3,
                "canada_workex": 2,
                "dep_num": 1,
                "canada_born": False,
                "citizen_status": True,
                "level_of_schooling": 8,
                "fluent_english": True,
                "reading_english_scale": 8,
                "speaking_english_scale": 7,
                "writing_english_scale": 7,
                "numeracy_scale": 8,
                "computer_scale": 9,
                "transportation_bool": True,
                "caregiver_bool": False,
                "housing": 5,
                "income_source": 3,
                "felony_bool": False,
                "attending_school": False,
                "currently_employed": False,
                "substance_use": False,
                "time_unemployed": 6,
                "need_mental_health_support_bool": False,
                "current_model": "RamdomForest",
            }
        }


class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True


class ClientUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=18)
    gender: Optional[Gender] = None
    work_experience: Optional[int] = Field(None, ge=0)
    canada_workex: Optional[int] = Field(None, ge=0)
    dep_num: Optional[int] = Field(None, ge=0)
    canada_born: Optional[bool] = None
    citizen_status: Optional[bool] = None
    level_of_schooling: Optional[int] = Field(None, ge=1, le=14)
    fluent_english: Optional[bool] = None
    reading_english_scale: Optional[int] = Field(None, ge=0, le=10)
    speaking_english_scale: Optional[int] = Field(None, ge=0, le=10)
    writing_english_scale: Optional[int] = Field(None, ge=0, le=10)
    numeracy_scale: Optional[int] = Field(None, ge=0, le=10)
    computer_scale: Optional[int] = Field(None, ge=0, le=10)
    transportation_bool: Optional[bool] = None
    caregiver_bool: Optional[bool] = None
    housing: Optional[int] = Field(None, ge=1, le=10)
    income_source: Optional[int] = Field(None, ge=1, le=11)
    felony_bool: Optional[bool] = None
    attending_school: Optional[bool] = None
    currently_employed: Optional[bool] = None
    substance_use: Optional[bool] = None
    time_unemployed: Optional[int] = Field(None, ge=0)
    need_mental_health_support_bool: Optional[bool] = None
    current_model: Optional[str] = None


class ModelUpdate(BaseModel):
    new_model: Optional[str] = None


class ClientCreate(BaseModel):
    age: int = Field(None, ge=18)
    gender: Gender = None
    work_experience: int = Field(None, ge=0)
    canada_workex: int = Field(None, ge=0)
    dep_num: int = Field(None, ge=0)
    canada_born: bool = None
    citizen_status: bool = None
    level_of_schooling: int = Field(None, ge=1, le=14)
    fluent_english: bool = None
    reading_english_scale: int = Field(None, ge=0, le=10)
    speaking_english_scale: int = Field(None, ge=0, le=10)
    writing_english_scale: int = Field(None, ge=0, le=10)
    numeracy_scale: int = Field(None, ge=0, le=10)
    computer_scale: int = Field(None, ge=0, le=10)
    transportation_bool: bool = None
    caregiver_bool: bool = None
    housing: int = Field(None, ge=1, le=10)
    income_source: int = Field(None, ge=1, le=11)
    felony_bool: bool = None
    attending_school: bool = None
    currently_employed: bool = None
    substance_use: bool = None
    time_unemployed: int = Field(None, ge=0)
    need_mental_health_support_bool: bool = None


class ServiceResponse(BaseModel):
    client_id: int
    user_id: int
    employment_assistance: bool
    life_stabilization: bool
    retention_services: bool
    specialized_services: bool
    employment_related_financial_supports: bool
    employer_financial_supports: bool
    enhanced_referrals: bool
    success_rate: int = Field(ge=0, le=100)

    class Config:
        from_attributes = True


class ServiceUpdate(BaseModel):
    employment_assistance: Optional[bool] = None
    life_stabilization: Optional[bool] = None
    retention_services: Optional[bool] = None
    specialized_services: Optional[bool] = None
    employment_related_financial_supports: Optional[bool] = None
    employer_financial_supports: Optional[bool] = None
    enhanced_referrals: Optional[bool] = None
    success_rate: Optional[int] = Field(None, ge=0, le=100)


class ClientListResponse(BaseModel):
    clients: List[ClientResponse]
    total: int


class ClientFilters:
    def __init__(
        self,
        employment_status: Optional[bool] = None,
        education_level: Optional[int] = None,
        age_min: Optional[int] = None,
        gender: Optional[int] = None,
        work_experience: Optional[int] = None,
        canada_workex: Optional[int] = None,
        dep_num: Optional[int] = None,
        canada_born: Optional[bool] = None,
        citizen_status: Optional[bool] = None,
        fluent_english: Optional[bool] = None,
        reading_english_scale: Optional[int] = None,
        speaking_english_scale: Optional[int] = None,
        writing_english_scale: Optional[int] = None,
        numeracy_scale: Optional[int] = None,
        computer_scale: Optional[int] = None,
        transportation_bool: Optional[bool] = None,
        caregiver_bool: Optional[bool] = None,
        housing: Optional[int] = None,
        income_source: Optional[int] = None,
        felony_bool: Optional[bool] = None,
        attending_school: Optional[bool] = None,
        substance_use: Optional[bool] = None,
        time_unemployed: Optional[int] = None,
        need_mental_health_support_bool: Optional[bool] = None,
        current_model: Optional[str] = None,
    ):
        self.field_map = {
            "employment_status": Client.currently_employed,
            "age_min": lambda v: Client.age >= v,
            "gender": Client.gender,
            "education_level": Client.level_of_schooling,
            "work_experience": Client.work_experience,
            "canada_workex": Client.canada_workex,
            "dep_num": Client.dep_num,
            "canada_born": Client.canada_born,
            "citizen_status": Client.citizen_status,
            "fluent_english": Client.fluent_english,
            "reading_english_scale": Client.reading_english_scale,
            "speaking_english_scale": Client.speaking_english_scale,
            "writing_english_scale": Client.writing_english_scale,
            "numeracy_scale": Client.numeracy_scale,
            "computer_scale": Client.computer_scale,
            "transportation_bool": Client.transportation_bool,
            "caregiver_bool": Client.caregiver_bool,
            "housing": Client.housing,
            "income_source": Client.income_source,
            "felony_bool": Client.felony_bool,
            "attending_school": Client.attending_school,
            "substance_use": Client.substance_use,
            "time_unemployed": Client.time_unemployed,
            "need_mental_health_support_bool": Client.need_mental_health_support_bool,
            "current_model": Client.current_model,
        }
        self.employment_status: Optional[bool] = employment_status
        self.education_level: Optional[int] = education_level
        self.age_min: Optional[int] = age_min
        self.gender: Optional[int] = gender
        self.work_experience: Optional[int] = work_experience
        self.canada_workex: Optional[int] = canada_workex
        self.dep_num: Optional[int] = dep_num
        self.canada_born: Optional[bool] = canada_born
        self.citizen_status: Optional[bool] = citizen_status
        self.fluent_english: Optional[bool] = fluent_english
        self.reading_english_scale: Optional[int] = reading_english_scale
        self.speaking_english_scale: Optional[int] = speaking_english_scale
        self.writing_english_scale: Optional[int] = writing_english_scale
        self.numeracy_scale: Optional[int] = numeracy_scale
        self.computer_scale: Optional[int] = computer_scale
        self.transportation_bool: Optional[bool] = transportation_bool
        self.caregiver_bool: Optional[bool] = caregiver_bool
        self.housing: Optional[int] = housing
        self.income_source: Optional[int] = income_source
        self.felony_bool: Optional[bool] = felony_bool
        self.attending_school: Optional[bool] = attending_school
        self.substance_use: Optional[bool] = substance_use
        self.time_unemployed: Optional[int] = time_unemployed
        self.need_mental_health_support_bool: Optional[bool] = (
            need_mental_health_support_bool
        )
        self.current_model: Optional[str] = current_model

    def build_filter(self):
        filter = []
        for key, value in self.field_map.items():
            if not hasattr(self, key) or getattr(self, key) is None:
                continue
            if callable(value):
                filter.append(value(getattr(self, key)))
            else:
                filter.append(value == getattr(self, key))
        return filter
