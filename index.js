const express = require('express');
const cors = require('cors');

const app = express();

// Render par CORS ekdum badiya kaam kare isliye setup
app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json());

// Check karne ke liye home route
app.get('/', (req, res) => {
    res.send("Render Backend is Live and Connected to Agent Router!");
});

// Aapka sahi API URL aur API Key direct code me
const AGENT_ROUTER_BASE_URL = "https://agentrouter.org/v1/chat/completions";
const MY_SECRET_API_KEY = "Sk-7eeoGOHiiviyMTB6Rxe87lOnB7rGgto8FR8JKmDztKpmriZX"; 

app.post('/api/chat', async (req, res) => {
    try {
        const { prompt } = req.body;
        if (!prompt) return res.status(400).json({ error: "Prompt is required" });

        console.log("Sending request to Agent Router for:", prompt);

        const response = await fetch(AGENT_ROUTER_BASE_URL, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${MY_SECRET_API_KEY}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "claude-3-5-sonnet",
                messages: [{ role: "user", content: prompt }]
            })
        });

        const data = await response.json();
        res.json(data);

    } catch (error) {
        console.error("Render Backend Error:", error);
        res.status(500).json({ error: "Server Error", details: error.message });
    }
});

// Render dynamic port use karta hai
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on port ${PORT}`);
});
