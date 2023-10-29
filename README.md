# API for shop with admin panel
## Installation without docker
1. Create and activate virtual environment, install dependencies
```
make install
```
2. Create and fill in the `.env` file similar to `.env.example`
3. Apply migrations
```
make migrate
```
4. Apply migrations
```
make migrate
```
5. Create fake data (optional)
```
make fake_data
```
The service will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

Documentation for the service will be available at [http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)

## Installation with docker
1. Create and fill in the `.env` file similar to `.env.example`
2. If you want to use PostgreSQL, set `USE_POSTGRES=True`
3. Run the command
```
make run_docker
```
The service will be available at [http://127.0.0.1:80](http://127.0.0.1:80)

Documentation for the service will be available at [http://127.0.0.1:80/api/v1/docs](http://127.0.0.1:80/api/v1/docs)

## Useful development commands when running without docker
```
make superuser   # Creating a superuser
make flash       # Database cleanup
make test        # Running tests
make format      # Running linter
make fake_data   # Add fake data to db
```
## Database schema
![Schema](./imgs/models.png)
```
make db_image
```