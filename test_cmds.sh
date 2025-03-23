echo 'Creating admin user'
curl -X POST "http://127.0.0.1:8000/auth/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123",
    "role": "user"
  }'

echo 'Getting token'
token=`curl -X POST "http://127.0.0.1:8000/auth/token" \
  -F "username=testuser" \
  -F "password=test123" | jq -r '.access_token'`

echo 'Creating client'
curl -X POST "http://127.0.0.1:8000/clients/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $token" \
  -d '{
    "age": 18,
    "gender": 1,
    "work_experience": 5
  }'
