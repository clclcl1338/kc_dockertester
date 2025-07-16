# Dockerized API Tester for Keycloak

This is a Dockerized API tester that validates login credentials and checks for a valid bearer token using a remote Keycloak instance.

## Features

*   Validates login credentials via the `/auth` endpoint and returns a bearer token.
*   Responds with "hello valid user" when calling the `/check` endpoint with a valid token, or "unauthorize" otherwise.
*   Connects to a remote Keycloak instance (public or private IP, any port).
*   Configuration is managed through a `.env` file.

## Prerequisites

*   Docker
*   Docker Compose

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Configure the `.env` file:**

    Create a `.env` file in the root of the project and add the following environment variables:

    ```
    KEYCLOAK_URL=http://localhost:8080
    CLIENT_ID=my-client
    USERNAME=my-user
    PASSWORD=my-password
    REALM_NAME=my-realm
    ```

    **Note:** If your Keycloak instance is running in Docker, you might need to use the Docker host IP address instead of `localhost`. On most systems, you can use `host.docker.internal` for the `KEYCLOAK_URL`. For example:

    ```
    KEYCLOAK_URL=http://host.docker.internal:8080
    ```

## Running the API Tester

1.  **Build and run the Docker container:**

    ```bash
    docker-compose up --build
    ```

    The API tester will be available at `http://localhost:5000`.

## Testing with Keycloak 25.0.1 in Docker

This section provides a guide on how to test the API tester with a Keycloak 25.0.1 instance running in Docker.

1.  **Run Keycloak in Docker:**

    ```bash
    docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:25.0.1 start-dev
    ```

2.  **Create a new realm in Keycloak:**

    *   Go to `http://localhost:8080` and log in to the Keycloak admin console with the credentials `admin`/`admin`.
    *   Click on "Create Realm".
    *   Enter a name for your realm (e.g., `my-realm`) and click "Create".

3.  **Create a new client:**

    *   In your new realm, go to "Clients" and click "Create client".
    *   Set the "Client ID" to `my-client`.
    *   Click "Next".
    *   Enable "Client authentication" and "Authorization".
    *   Click "Next".
    *   Add `http://localhost:5000/*` to the "Valid redirect URIs".
    *   Click "Save".

4.  **Create a new user:**

    *   Go to "Users" and click "Add user".
    *   Enter a username (e.g., `my-user`).
    *   Click "Create".
    *   Go to the "Credentials" tab and set a password for the user (e.g., `my-password`).

5.  **Update the `.env` file:**

    Update your `.env` file with the values you used to configure Keycloak:

    ```
    KEYCLOAK_URL=http://localhost:8080
    CLIENT_ID=my-client
    USERNAME=my-user
    PASSWORD=my-password
    REALM_NAME=my-realm
    ```

    **Note:** If you are running the API tester on the same machine as the Keycloak Docker container, you might need to use `host.docker.internal` for the `KEYCLOAK_URL` in your `.env` file.

6.  **Run the API tester:**

    ```bash
    docker-compose up --build
    ```

## API Endpoints

### `/auth`

*   **Method:** `POST`
*   **Description:** Authenticates with Keycloak and returns a bearer token.
*   **Success Response:**

    ```json
    {
        "token": "your-bearer-token"
    }
    ```

*   **Error Response:**

    ```json
    {
        "error": "Authentication failed"
    }
    ```

### `/check`

*   **Method:** `GET`
*   **Description:** Checks if the provided bearer token is valid.
*   **Headers:**

    *   `Authorization: Bearer your-bearer-token`

*   **Success Response:**

    ```json
    {
        "message": "hello valid user"
    }
    ```

*   **Error Response:**

    ```json
    {
        "error": "unauthorize"
    }
    ```

## Running the Tests

To run the tests, run the following command:

```bash
python3 -m unittest tests/test_app.py
```
