FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files (pyproject.toml and poetry.lock)
COPY pyproject.toml poetry.lock ./

# Set the Python version for Poetry
RUN poetry env use /usr/local/bin/python3.12

# Install ODBC dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc \
    unixodbc-dev

# Download și instalează driverul ODBC pentru SQL Server 17
RUN apt-get update
RUN echo "deb [signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list
RUN wget -qO - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/keyrings/microsoft.gpg
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
    msodbcsql17

# Install project dependencies using Poetry
RUN poetry install --no-root

# Copy the src directory containing your application code
COPY static /app/static
COPY src /app/src

# Set the user to run the application (optional, for security)
# USER nonroot

# Define the command to run your application
CMD ["poetry", "run", "python", "src/app.py"]