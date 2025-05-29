const express = require('express');
const axios = require('axios');
const Redis = require('ioredis');

const app = express();
app.use(express.json());

const redis = new Redis({ host: process.env.REDIS_HOST || 'localhost' });
const PY_API = process.env.PYTHON_API_URL || 'http://localhost:5000/event';

function generateData() {
  return {
    temperature: (20 + Math.random() * 15).toFixed(2),
    pressure: (100 + Math.random() * 50).toFixed(2),
    timestamp: Date.now()
  };
}

app.get('/sensor-data', async (req, res) => {
  const cache = await redis.get('sensor:data');
  if (cache) return res.json(JSON.parse(cache));

  const data = generateData();
  await redis.setex('sensor:data', 10, JSON.stringify(data));
  res.json(data);
});

app.post('/alert', async (req, res) => {
  const alert = req.body;
  try {
    await axios.post(PY_API, alert);
    res.status(200).json({ status: 'alert sent' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Sensor API rodando na porta ${PORT}`));
