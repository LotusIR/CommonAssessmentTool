import pytest
from fastapi import status

# Test GET Operations
def test_get_clients_unauthorized(client):
    """Test that unauthorized access is prevented"""
    response = client.get("/clients/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_clients_as_admin(client, admin_headers):
    """Test getting all clients as admin"""
    response = client.get("/clients/", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "clients" in data
    assert "total" in data
    assert len(data["clients"]) > 0

def test_get_client_by_id(client, admin_headers):
    """Test getting specific client"""
    # Test existing client
    response = client.get("/clients/1", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1
    
    # Test non-existent client
    response = client.get("/clients/999", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_clients_by_criteria(client, admin_headers):
    """Test searching clients by various criteria"""
    # Test single criterion
    response = client.get(
        "/clients/search/by-criteria",
        params={"age_min": 25},
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

    # Test multiple criteria
    response = client.get(
        "/clients/search/by-criteria",
        params={
            "age_min": 25,
            "currently_employed": True,
            "gender": 2
        },
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK

    # Test invalid criteria
    response = client.get(
        "/clients/search/by-criteria",
        params={"age_min": 15},  # Below minimum age
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Changed from 400

def test_get_clients_by_services(client, admin_headers):
    """Test getting clients by service status"""
    response = client.get(
        "/clients/search/by-services",
        params={
            "employment_assistance": True,
            "life_stabilization": True
        },
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

def test_get_client_services(client, admin_headers):
    """Test getting services for a specific client"""
    response = client.get("/clients/1/services", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    services = response.json()
    assert isinstance(services, list)
    assert len(services) > 0
    assert "employment_assistance" in services[0]
    assert "success_rate" in services[0]

def test_get_clients_by_success_rate(client, admin_headers):
    """Test getting clients by success rate threshold"""
    response = client.get(
        "/clients/search/success-rate",
        params={"min_rate": 70},
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

def test_get_clients_by_case_worker(client, admin_headers, case_worker_headers):
    """Test getting clients assigned to a case worker"""
    # Test as admin
    response = client.get("/clients/case-worker/2", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    
    # Test as case worker
    response = client.get("/clients/case-worker/2", headers=case_worker_headers)
    assert response.status_code == status.HTTP_200_OK

# Test UPDATE Operations
def test_update_client(client, admin_headers):
    """Test updating client information"""
    update_data = {
        "age": 26,
        "currently_employed": True,
        "time_unemployed": 0
    }
    response = client.put(
        "/clients/1",
        json=update_data,
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK
    updated_client = response.json()
    assert updated_client["age"] == 26
    assert updated_client["currently_employed"] == True
    assert updated_client["time_unemployed"] == 0

# Test Create Case Assignment
def test_create_case_assignment(client, admin_headers):
    """Test creating new case assignment"""
    response = client.post(
        "/clients/1/case-assignment",
        params={"case_worker_id": 2},
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK

    # Test duplicate assignment
    response = client.post(
        "/clients/1/case-assignment",
        params={"case_worker_id": 2},
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# Test DELETE Operation
def test_delete_client(client, admin_headers):
    """Test deleting a client"""
    # Test successful deletion
    response = client.delete("/clients/2", headers=admin_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify client is deleted
    response = client.get("/clients/2", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test deleting non-existent client
    response = client.delete("/clients/999", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Test model operation
def test_get_current_model(client, admin_headers):
    """Test get current model"""
    response = client.get("/clients/1/model", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert "current_model" in response.json()


def test_set_current_model(client, admin_headers):
    """Test set model for a client"""
    new_model_payload = {"new_model": "RandomForest"}

    response = client.put(
        "/clients/1/model",
        headers=admin_headers,
        json=new_model_payload
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["current_model"] == "RandomForest"
    assert data["client_id"] == 1
    assert "message" in data and "updated" in data["message"].lower()

    # verify it updated by calling GET again
    response_check = client.get("/clients/1/model", headers=admin_headers)
    assert response_check.status_code == status.HTTP_200_OK
    assert response_check.json()["current_model"] == "RandomForest"
