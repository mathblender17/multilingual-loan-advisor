const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const session = require('express-session');

const app = express();
const port = 3001;

// Simple in-memory storage for demo
const users = new Map();

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
    secret: 'demo-secret-key',
    resave: false,
    saveUninitialized: false,
    cookie: {
        maxAge: 1000 * 60 * 60 * 24 // 1 day
    }
}));

// Set EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Authentication Middleware
const isAuthenticated = (req, res, next) => {
    if (req.session.userId) {
        next();
    } else {
        res.redirect('/login');
    }
};

// Routes
app.get('/', isAuthenticated, (req, res) => {
    res.render('index');
});

app.get('/login', (req, res) => {
    res.render('login', { error: null });
});

app.get('/signup', (req, res) => {
    res.render('signup', { error: null });
});

app.post('/signup', (req, res) => {
    const { username, email, password, confirmPassword } = req.body;

    if (password !== confirmPassword) {
        return res.render('signup', { error: 'Passwords do not match' });
    }

    if (users.has(email)) {
        return res.render('signup', { error: 'Email already exists' });
    }

    // Store user in memory
    users.set(email, { username, email, password });
    req.session.userId = email;
    res.redirect('/');
});

app.post('/login', (req, res) => {
    const { email, password } = req.body;
    const user = users.get(email);

    if (!user || user.password !== password) {
        return res.render('login', { error: 'Invalid email or password' });
    }

    req.session.userId = email;
    res.redirect('/');
});

app.get('/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/login');
});

// Chat endpoint
app.post('/chat', isAuthenticated, (req, res) => {
    const userMessage = req.body.message;
    let botResponse = '';

    // Simple loan-related responses
    if (userMessage.toLowerCase().includes('loan')) {
        botResponse = 'I can help you with various types of loans. What specific information are you looking for?';
    } else if (userMessage.toLowerCase().includes('interest')) {
        botResponse = 'Our current interest rates range from 3.5% to 12% depending on the loan type and your credit score.';
    } else if (userMessage.toLowerCase().includes('apply')) {
        botResponse = 'To apply for a loan, you\'ll need: \n1. Valid ID\n2. Proof of income\n3. Bank statements\n4. Credit history';
    } else {
        botResponse = 'How can I assist you with your loan-related questions?';
    }

    res.json({ response: botResponse });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
}); 