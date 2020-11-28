#curl --request get 'http://localhost:5000/api/v1/login?username=jc&password=password'


#curl -d '{boxer.json}' -H  'Content-Type: application/json' 'http://localhost:5000/api/v1/adduser'

curl --request postcurl --location --request POST 'http://localhost:5000/api/v1/adduser' \
--header 'Content-Type: application/json' \
--data-raw '{
        "perm": "usr",
        "firstname": "Gene",
        "lastname": "Fullmer",
        "username": "Cyclone",
        "email": "cyclone@n2n",
        "password": "password"
}'
