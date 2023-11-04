from fastapi import APIRouter
from fastapi.responses import HTMLResponse

html_templates = APIRouter()

html = """
<!DOCTYPE html>
<html>
<head>
<title>Test WebSocket</title>
</head>
<body>
<h1>WebSocket Test</h1>
<button onclick="startWebSocket()">Start WebSocket</button>
<button onclick="stopWebSocket()">Stop WebSocket</button>
<script>
var socket = null;
function startWebSocket() {
  socket = new WebSocket("ws://localhost:8000/ws/audio");
  socket.binaryType = 'arraybuffer'; // set binary type to arraybuffer
  socket.onmessage = function(event) {
    console.log("Received data", event.data);
    // handle received audio data here
  }
}
function stopWebSocket() {
  if (socket) {
    socket.close();
    socket = null;
  }
}
</script>
</body>
</html>
"""

@html_templates.get("/")
async def get():
    return HTMLResponse(html)