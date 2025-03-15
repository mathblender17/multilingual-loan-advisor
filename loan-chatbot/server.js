// Add this after your login post route
app.get('/chat', (req, res) => {
    // Check if user is logged in
    if (!req.session.user) {
        return res.redirect('/login');
    }
    res.render('chat');
});

// Modify your login POST route to redirect to chat
app.post('/login', (req, res) => {
    const { email, password } = req.body;
    
    // Find user
    const user = users.find(u => u.email === email);
    
    if (!user || user.password !== password) {
        return res.render('login', { error: 'Invalid email or password' });
    }
    
    // Set user session
    req.session.user = user;
    
    // Redirect to chat instead of home
    res.redirect('/chat');
}); 