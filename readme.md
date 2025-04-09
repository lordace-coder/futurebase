# FutureBase

FutureBase is a **Backend-as-a-Service (BaaS)** platform designed to simplify the development of data-driven applications. It provides developers with tools to manage projects, collections, and data fields seamlessly, enabling rapid application development without worrying about backend complexities.

## Features

- **Project Management**: Create and manage multiple projects.
- **Dynamic Collections**: Define collections with customizable fields.
- **Field Types**: Support for various data types, including:
  - Text
  - URL
  - Number
  - Decimal
  - Select
  - JSON
  - Boolean
- **Data Operations**: Perform CRUD operations on collections.
- **User Authentication**: Secure access to projects and collections.
- **REST API**: Expose data and operations via a RESTful API.

## Tech Stack

- **Backend**: Django (Python)
- **Database**: MongoDB (via PyMongo)
- **API Framework**: Django REST Framework
- **Frontend**: Bootstrap (for admin templates)
- **Containerization**: Docker

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/futurebase.git
   cd futurebase
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up MongoDB:
   - Ensure MongoDB is running locally or update the connection string in `collections_manager/database.py`.

4. Run migrations:
   ```bash
   python futurebase/manage.py migrate
   ```

5. Start the development server:
   ```bash
   python futurebase/manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000`.

## API Endpoints

### Authentication
- **Login**: `/api/token/`
- **Refresh Token**: `/api/token/refresh/`

### Collections
- **List Collections**: `GET /api/collections/<email>/<password>/<project_id>`
- **Collection Data**: `GET /api/collection-data/<email>/<password>/<id>`

### Projects
- **List Projects**: `GET /dashboard/`
- **Create Project**: `POST /create-project/`

## Development

### Running with Docker
1. Build the Docker image:
   ```bash
   docker build -t futurebase .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 futurebase
   ```

### Running Tests
Run the Django test suite:
```bash
python futurebase/manage.py test
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
