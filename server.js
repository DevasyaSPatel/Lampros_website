const express = require('express');
const cors = require('cors');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// API Endpoint to proxy CoinGecko (avoids CORS issues on the frontend)
app.get('/api/prices', async (req, res) => {
    try {
        const CG_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum,bitcoin,solana,matic-network&vs_currencies=usd&include_24hr_change=true';
        const response = await axios.get(CG_URL);
        res.json(response.data);
    } catch (error) {
        console.error("Error fetching crypto prices:", error.message);
        res.status(500).json({ error: "Failed to fetch top crypto prices" });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
    console.log(`- WebApp UI: http://localhost:${PORT}/index.html`);
    console.log(`- API Endpoint: http://localhost:${PORT}/api/prices`);
});
