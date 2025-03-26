#!/bin/bash

echo 'Get token'

token=`curl -X POST "http://127.0.0.1:8000/auth/token" \
  -F "username=testuser" \
  -F "password=test123" | jq -r '.access_token'`

echo $token

echo 'Get clients'
curl -X GET "http://127.0.0.1:8000/clients/" \
  -H "Authorization: Bearer $token"

echo 'Get client'
curl -X GET "http://127.0.0.1:8000/clients/1" \
  -H "Authorization: Bearer $token"

echo 'Get clients by criteria'
curl -X GET "http://127.0.0.1:8000/clients/search/by-criteria?age_min=26" \
  -H "Authorization: Bearer $token"
