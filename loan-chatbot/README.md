# Loan Chatbot

A simple chatbot application that helps users with loan-related queries. The chatbot provides information about loan types, interest rates, application requirements, and more.

## Features

- Real-time chat interface
- Responsive design
- Basic loan-related information
- Easy to extend with more features

## Prerequisites

- Node.js (v12 or higher)
- npm (Node Package Manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd loan-chatbot
```

2. Install dependencies:
```bash
npm install
```

## Usage

1. Start the server:
```bash
node app.js
```

2. Open your browser and navigate to:
```
http://localhost:3000
```

## Project Structure

```
loan-chatbot/
├── views/                   # EJS templates
│   ├── index.ejs           # Main chat interface
│   └── partials/           # Reusable components
│       ├── header.ejs
│       └── footer.ejs
├── public/                 # Static files
│   ├── styles/
│   │   └── style.css      # Custom CSS
│   └── scripts/
│       └── script.js      # Client-side JavaScript
├── app.js                 # Main server file
├── package.json          # Project dependencies
└── README.md            # Project documentation
```

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the ISC License. 