# Restaurant Finder - Test Task Challenge

## Introduction
This project is a test task challenge to develop an MVP within 24 hours. The application allows users to search for restaurants based on specific criteria using a Telegram bot and displays the results on a React web interface with an interactive map.

## Features
- **Telegram Bot**: Interact with users and process their restaurant search requests.
- **React Web Interface**: Display restaurant search results dynamically.
- **AI Integration**: Use OpenAI to interpret natural language queries.
- **Restaurant Search API**: Retrieve restaurant data using Yelp.
- **Interactive Map**: Visualize restaurant locations using OpenStreetMap.

## Usage

### End User
1. Visit the website and click the button to go to the Telegram bot. (Or go to the bot directly)
2. Start a conversation with the bot by clicking the `/start` command.
3. Send a message with your restaurant search criteria (e.g., "Looking for an Italian restaurant near Times Square").
4. The bot will respond with a list of relevant restaurants and a link to view them on the web interface.
5. Click the "Show on map" button to see the restaurant locations on the interactive map.

### Developer

#### Prerequisites
- Docker
- Docker Compose

#### Deployment

1. **Clone the repository**:
    ```bash
    git clone https://github.com/maskyy/restaurant-finder.git
    cd restaurant-finder
    ```

2. **Build and run the Docker containers**:
    ```bash
    docker-compose up --build
    ```

3. **Environment Variables**:
    Copy `.env.example` and set the following important variables:
    ```env
        BOT_TOKEN=bot_token
        WEBHOOK_URL=https://example.com  # backend
        SERVER_URL=https://example.org  # frontend
        OPENAI_API_KEY=secret_key
        YELP_API_KEY=yelp_api_key
        OPENCAGE_API_KEY=opencage_api_key
    ```
    Copy `client/config.js.example` and set the BASE_URL to WEBHOOK_URL.

4. **Access the application**:
    - **Web Interface**: Open your browser and go to `http://localhost:5173`.
    - **Telegram Bot**: Start a conversation with your bot on Telegram.

#### Project Structure
- **client**: Contains the React web interface.
- **server**: Contains the FastAPI backend and Telegram bot handlers.
- **Dockerfile**: Docker configuration for building the project.
- **docker-compose.yml**: Docker Compose configuration for running the project.

#### Development
1. **Frontend**:
    ```bash
    cd client
    npm install
    npm start
    ```

2. **Backend**:
    ```bash
    poetry install --only main --no-root
    python -m restaurant-finder.main
    ```
