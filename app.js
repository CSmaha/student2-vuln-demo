const express = require('express');
const app = express();

app.get('/user', (req, res) => {
    const userInput = req.query.name;

    // ❌ XSS
    res.send("<h1>Hello " + userInput + "</h1>");
});

app.get('/eval', (req, res) => {
    const code = req.query.code;

    // ❌ Code Injection
    eval(code);

    res.send("Executed");
});

// ❌ Hardcoded secret
const password = "123456";

app.listen(3000, () => {
    console.log("App running on port 3000");
});
