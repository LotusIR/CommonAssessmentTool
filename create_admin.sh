#!/bin/bash

echo 'Creating admin user'
curl -X POST "http://127.0.0.1:8000/auth/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123",
    "role": "admin"
  }'