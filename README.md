# 1 - RUN 
`docker-compose up --build -d`

# 2 - TEST
in Terminal :
`curl -d "isin=2jdkertitrew&limit_price=0.1&side=sell&valid_until=1622401835&quantity=1622401835" -X POST http://localhost:8080/orders`

Feel free to change the request parameters to trigger the validation method.