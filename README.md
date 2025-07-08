### patreon-payment-api

This project provides a Python API for interacting with Patreon. Below are instructions for setting up and running the API, as well as details on the available endpoints.

![license](https://img.shields.io/badge/license-MIT-red)


## Table of Contents
- [Installation](#installation)
- [Setup](#setup)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/exrod/patreon-payment-api.git
   cd patreon-payment-api
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Obtain a Patreon API access token and set it as an environment variable:
   ```bash
   export ACCESS_TOKEN=your_access_token
   ```
   OR
2. Update the `.env` file with your configurations.

## Running the API

1. Start the Flask server:
   ```bash
   python main.py
   ```

2. The API will be accessible at `http://localhost:6969`.

## API Endpoints

### Get Non Paid Members Info

- **Endpoint**: `/patreon/non_active`
- **Method**: `GET`
- **Description**: Retrieves detailed information about Non Paid Members.
- **Example Request**:
  ```bash
  curl -X GET "http://localhost:6969/patreon/non_active"
  ```

### Get Paid Members Info

- **Endpoint**: `/patreon/active`
- **Method**: `GET`
- **Description**: Retrieves detailed information about Non Paid Members.
- **Example Request**:
  ```bash
  curl -X GET "http://localhost:6969/patreon/active"
  ```

### Get All Members Info

- **Endpoint**: `/patreon`
- **Method**: `GET`
- **Description**: Retrieves detailed information about Members.
- **Example Request**:
  ```bash
  curl -X GET "http://localhost:6969/patreon/active"
  ```

## Usage

After starting the server, use the API endpoints to interact with the Patreon API. You can use tools like `curl` or Postman to test the endpoints.

## Contributing

We welcome contributions! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

Github Username Changed to - @inlovewithgo
