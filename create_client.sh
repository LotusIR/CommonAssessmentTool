#!/bin/bash

echo 'Getting token'
token=`curl -X POST "http://127.0.0.1:8000/auth/token" \
  -F "username=testuser" \
  -F "password=test123" | jq -r '.access_token'`

echo 'Creating client'
curl -X POST "http://127.0.0.1:8000/clients/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $token" \
  -d '{
    "age": 25,
    "gender": 1,
    "work_experience": 3,
    "canada_workex": 2,
    "dep_num": 1,
    "canada_born": false,
    "citizen_status": true,
    "level_of_schooling": 8,
    "fluent_english": true,
    "reading_english_scale": 8,
    "speaking_english_scale": 7,
    "writing_english_scale": 7,
    "numeracy_scale": 8,
    "computer_scale": 9,
    "transportation_bool": true,
    "caregiver_bool": false,
    "housing": 5,
    "income_source": 3,
    "felony_bool": false,
    "attending_school": false,
    "currently_employed": false,
    "substance_use": false,
    "time_unemployed": 6,
    "need_mental_health_support_bool": false,
    "current_model": "RamdomForest"
  }'
