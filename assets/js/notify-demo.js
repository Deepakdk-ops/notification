const wsLog = document.getElementById("wsLog");

let ws = null;

function connectWS(userId) {
    if (ws) ws.close();

    ws = new WebSocket(`wss://YOUR_RENDER_DOMAIN/ws/notifications/${userId}/`);

    ws.onopen = () => log("WebSocket connected");

    ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        log("Received: " + JSON.stringify(data));
    };

    ws.onclose = () => log("WebSocket disconnected");
}

function sendNotification() {
    const userId = document.getElementById("userId").value;
    const message = document.getElementById("message").value;

    if (!ws || ws.readyState !== 1) connectWS(userId);

    fetch("https://YOUR_RENDER_DOMAIN/api/notify/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, message: message })
    })
    .then(r => r.json())
    .then(res => log("API: " + JSON.stringify(res)));
}

function log(msg) {
    wsLog.innerHTML += msg + "<br>";
}