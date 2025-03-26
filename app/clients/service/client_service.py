"""
Client service module handling all database operations for clients.
Provides CRUD operations and business logic for client management.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
from app.models import Client, ClientCase, User
from app.clients.schema import ClientUpdate, ServiceUpdate, ServiceResponse, ModelUpdate


class ClientService:
    @staticmethod
    def get_client(db: Session, client_id: int):
        """Get a specific client by ID"""
        return ClientService.get_client_or_404nf(db, client_id)

    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 50):
        """
        Get clients with optional pagination.
        Default shows first 50 clients, which means you'd need 3 pages for 150 records.
        """
        ClientService.validate_pagination(skip, limit)
        return {
            "clients": db.query(Client).offset(skip).limit(limit).all(),
            "total": db.query(Client).count()
        }

    @staticmethod
    def get_clients_by_criteria(
        db: Session,
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
        filters = locals().copy()
        filters.pop("db")

        ClientService.validate_criteria(filters)
        """Get clients filtered by any combination of criteria"""
        query = db.query(Client)

        try:
            query = ClientService.filter_clients_by_criteria(query, **filters)
            return query.all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving clients: {str(e)}",
            )

    @staticmethod
    def get_clients_by_services(db: Session, **service_filters: Optional[bool]):
        """
        Get clients filtered by multiple service statuses.
        """
        query = db.query(Client).join(ClientCase)
        try:
            for service_name, status in service_filters.items():
                if status is not None:
                    query = query.filter(getattr(ClientCase, service_name) == status)
            return query.all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving clients: {str(e)}",
            )

    @staticmethod
    def get_client_services(db: Session, client_id: int):
        client_cases = db.query(ClientCase).filter(ClientCase.client_id == client_id).all()
        """Get all services for a specific client with case worker info"""
        if not client_cases:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No services found for client with id {client_id}",
            )
        return client_cases

    @staticmethod
    def get_clients_by_success_rate(db: Session, min_rate: int = 70):
        """Get clients with success rate at or above the specified percentage"""
        if not (0 <= min_rate <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Success rate must be between 0 and 100",
            )
        return (
            db.query(Client)
            .join(ClientCase)
            .filter(ClientCase.success_rate >= min_rate)
            .all()
        )

    @staticmethod
    def get_clients_by_case_worker(db: Session, case_worker_id: int):
        """Get all clients assigned to a specific case worker"""
        ClientService.get_caseworker_or_404nf(db, case_worker_id)
        return (
            db.query(Client)
            .join(ClientCase)
            .filter(ClientCase.user_id == case_worker_id)
            .all()
        )

    @staticmethod
    def update_client(db: Session, client_id: int, client_update: ClientUpdate):
        """Update a client's information"""
        client = ClientService.get_client_or_404nf(db, client_id)
        ClientService.update_model_instance(client, client_update.dict(exclude_unset=True))
        try:
            db.commit(); db.refresh(client)
            return client
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client: {str(e)}",
            )

    @staticmethod
    def update_client_services(db: Session, client_id: int, user_id: int, service_update: ServiceUpdate):
        """Update a client's services and outcomes for a specific case worker"""
        client_case = ClientService.get_case_or_404nf(db, client_id, user_id)
        ClientService.update_model_instance(client_case, service_update.dict(exclude_unset=True))
        try:
            db.commit()
            db.refresh(client_case)
            return client_case
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client services: {str(e)}",
            )

    @staticmethod
    def create_case_assignment(db: Session, client_id: int, case_worker_id: int):
        """Create a new case assignment"""
        client = ClientService.get_client_or_404nf(db, client_id)
        case_worker = ClientService.get_caseworker_or_404nf(db, case_worker_id)
        existing = db.query(ClientCase).filter_by(client_id=client_id, user_id=case_worker_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client {client_id} already has a case assigned to case worker {case_worker_id}",
            )

        # Create new case assignment with default service values
        new_case = ClientCase(
            client_id=client_id,
            user_id=case_worker_id,
            employment_assistance=False,
            life_stabilization=False,
            retention_services=False,
            specialized_services=False,
            employment_related_financial_supports=False,
            employer_financial_supports=False,
            enhanced_referrals=False,
            success_rate=0,
        )
        try:
            db.add(new_case); 
            db.commit(); 
            db.refresh(new_case)
            return new_case
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create case assignment: {str(e)}",
            )

    @staticmethod
    def delete_client(db: Session, client_id: int):
        """Delete a client and their associated records"""
        client = ClientService.get_client_or_404nf(db, client_id)
        try:
            db.query(ClientCase).filter_by(client_id=client_id).delete()
            db.delete(client); db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete client: {str(e)}",
            )

    @staticmethod
    def get_current_model(db: Session, client_id: int):
        client = ClientService.get_client_or_404nf(db, client_id)
        return {"current_model": client.current_model}

    @staticmethod
    def set_model(db: Session, client_id: int, data: ModelUpdate):
        client = ClientService.get_client_or_404nf(db, client_id)
        try:
            client.current_model = data.new_model
            db.commit()
            return {
                "message": "Model updated", 
                "client_id": client_id, 
                "current_model": client.current_model,
                }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client services: {str(e)}",
            )
 
    """
    Hepler methods for public API methods
    """
    @staticmethod
    def get_client_or_404nf(db: Session, client_id: int) -> Client:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found",
            )
        return client

    @staticmethod
    def get_caseworker_or_404nf(db: Session, user_id: int) -> User:
        caseworker = db.query(User).filter(User.id == caseworker_id).first()
        if not caseworker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case worker with id {case_worker_id} not found",
            )
        return caseworker

    @staticmethod
    def get_case_or_404nf(db: Session, client_id: int, user_id: int) -> ClientCase:
        case = db.query(ClientCase).filter_by(client_id=client_id, user_id=user_id).first()
        if not case:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, 
                detail=f"No case for client {client_id} with worker {user_id}. "
                f"Cannot update services for a non-existent case assignment.",
                )
        return case

    @staticmethod
    def update_model_instance(instance, update_data: dict):
        for field, value in update_data.items():
            setattr(instance, field, value)

    @staticmethod
    def validate_pagination(skip: int, limit: int):
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip value cannot be negative",
            )
        if limit < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be greater than 0",
            )

    @staticmethod
    def validate_criteria(filters: dict):
        if (level := filters.get("education_level")) is not None and not (1 <= level <= 14):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Education level must be between 1 and 14",
            )
        if (age := filters.get("age_min")) is not None and age < 18:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum age must be at least 18",
            )
        if (gender := filters.get("gender")) is not None and gender not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gender must be 1 or 2",
            )

    @staticmethod
    def filter_clients_by_criteria(query, **filters):
        field_map = {
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

        for key, column in field_map.items():
            if (val := filters.get(key)) is not None:
                if callable(column):
                    query = query.filter(column(val))
                else:
                    query = query.filter(column == val)

        return query


