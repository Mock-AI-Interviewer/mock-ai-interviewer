export const config = {
    backendApiUrl: process.env.REACT_APP_BASE_API_ENDPOINT || "http://localhost:8000",
    backendApiWebsocketUrl: process.env.REACT_APP_WEBSOCKET_ENDPOINT || "ws://localhost:8000",
}