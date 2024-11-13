const express = require('express');
const mysql = require('mysql2');
const app = express();

// Configurações do banco de dados MySQL
const db = mysql.createConnection({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'seu_usuario',
    password: process.env.DB_PASSWORD || 'sua_senha',
    database: process.env.DB_NAME || 'aquaponia_db'
});

db.connect((err) => {
    if (err) throw err;
    console.log('Conectado ao banco de dados MySQL!');
});

// Rota para buscar dados de temperatura
app.get('/api/temperature', (req, res) => {
    const { startDate, endDate } = req.query;

    const query = `
        SELECT hour, temperature 
        FROM temperature_readings 
        WHERE timestamp >= ? AND timestamp <= ?
    `;
    db.query(query, [new Date(startDate), new Date(endDate)], (err, results) => {
        if (err) {
            res.status(500).send('Erro ao acessar o banco de dados.');
        } else {
            res.json(results);
        }
    });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});
