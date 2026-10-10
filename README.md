# ecovento-baconst express = require('express');
const cors = require('cors');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Serve o painel visual HTML
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Rotas da API
app.get('/api/status', (req, res) => {
  res.json({
    empresa: "EcoVento Energias Renováveis, S.A.",
    estado: "Operacional",
    parquesEolicos: 4,
    capacidadeTotalMW: 120.5,
    geracaoAtualMW: 98.2,
    eficienciaGlobal: "81.5%"
  });
});

app.get('/api/parques', (req, res) => {
  res.json([
    { id: 1, nome: "Parque Eólico do Marão", potenciaMW: 45.0, estado: "Normal", turbinas: 15 },
    { id: 2, nome: "Parque Eólico da Serra do Caramulo", potenciaMW: 30.5, estado: "Normal", turbinas: 10 },
    { id: 3, nome: "Parque Eólico de Alvão", potenciaMW: 25.0, estado: "Manutenção", turbinas: 8 },
    { id: 4, nome: "Parque Eólico de Montemuro", potenciaMW: 20.0, estado: "Normal", turbinas: 6 }
  ]);
});

app.listen(port, () => {
  console.log(`Servidor da EcoVento a correr na porta ${port}`);
});
ckend
