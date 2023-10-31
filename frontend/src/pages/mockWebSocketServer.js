import { Server } from 'mock-socket';

const mockServer = new Server('ws://localhost:8080');
let messageCount = 0; // Initialize the message count

mockServer.on('connection', (socket) => {
  socket.on('message', (data) => {
    // Handle incoming data (audio chunks) here
    // Send an iterated number with each message
    // messageCount += 1;
    // socket.send(JSON.stringify({ text: `Message ${messageCount}` }));
    // Handle incoming data (audio chunks) here
    // For this example, let's simulate sending the audio chunks back
    const audioChunks = Array.isArray(data) ? data : [data]; // Ensure audioChunks is an array
    audioChunks.forEach((chunk) => {
      // Send each chunk back to the client
      setTimeout(() => {
        socket.send(chunk);
      }, 1000); // Simulate a 1-second delay between chunks
    });
  });
});

export default mockServer;
