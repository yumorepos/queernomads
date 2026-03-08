# 🌍 QueerNomads

A community platform for queer digital nomads to share travel stories, safety tips, and hidden gems from around the globe.

Built as a **CS50 Final Project** — a full-stack Flask web application with user authentication, community storytelling, and search/browse functionality.

## ✨ Features

- **User Authentication** — Register, login, logout with secure password hashing
- **Travel Stories** — Share experiences with title, destination, category, rating, and full story text
- **User Profiles** — Bio, pronouns, home city, and countries visited
- **Browse & Search** — Filter stories by destination or category (nightlife, safety, community, accommodation, general)
- **Community Feed** — See recent stories from the community on the homepage
- **Responsive Design** — Mobile-friendly dark theme with tasteful rainbow accents

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **Database** | SQLite |
| **Frontend** | Jinja2, Bootstrap 5, custom CSS |
| **Auth** | Werkzeug (password hashing), Flask sessions |

## 📸 Screenshots

> *Coming soon — run the app locally to see the UI!*

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yumorepos/queernomads.git
cd queernomads

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app will be available at **http://localhost:5000**

### First Steps

1. Register a new account
2. Edit your profile (add pronouns, bio, countries visited)
3. Share your first travel story
4. Browse stories from the community

## 📁 Project Structure

```
queernomads/
├── app.py              # Main Flask application (routes, logic)
├── helpers.py          # Helper functions (login_required, apology)
├── schema.sql          # Database schema (users, stories)
├── requirements.txt    # Python dependencies
├── templates/
│   ├── layout.html     # Base template with navbar & footer
│   ├── index.html      # Homepage with community feed
│   ├── login.html      # Login form
│   ├── register.html   # Registration form
│   ├── post.html       # Create a new story
│   ├── browse.html     # Search and browse stories
│   ├── story.html      # Full story view
│   ├── profile.html    # User profile page
│   ├── edit_profile.html # Edit profile form
│   └── apology.html    # Error page
└── static/
    └── style.css       # Custom dark theme with rainbow accents
```

## 🎨 Design Philosophy

QueerNomads uses a dark, warm color palette with subtle rainbow accents — celebrating identity without being overwhelming. The UI prioritizes readability and accessibility on both desktop and mobile.

Category badges use distinct colors for quick visual scanning:
- 🟣 **Nightlife** — purple
- 🔴 **Safety** — red
- 🟢 **Community** — green
- 🔵 **Accommodation** — blue
- 🟠 **General** — orange

## 🔒 Security

- Passwords are hashed with Werkzeug's `generate_password_hash` (PBKDF2-SHA256)
- Session-based authentication with Flask's secure session handling
- Input validation on all forms
- SQL injection prevention via parameterized queries
- CSRF protection through Flask's session management

## 📝 License

MIT License — free to use, modify, and distribute.

## 🙏 Acknowledgments

- [CS50](https://cs50.harvard.edu/) — Harvard's Introduction to Computer Science
- [Flask](https://flask.palletsprojects.com/) — Python micro web framework
- [Bootstrap 5](https://getbootstrap.com/) — Responsive CSS framework

---

*Built with ❤️ for the queer travel community.*
