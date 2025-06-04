# Beer Dashboard

A simple Flask app where users can sign up, log in, track beers consumed (and money spent), and view a leaderboard of top drinkers. Modern, responsive UI with Docker Compose support.

---

## Requirements

- Docker & Docker Compose installed

---

## Setup & Run

1. **Clone the repo**  
   ```bash
   git clone https://github.com/Eleganton/DISSEMANKOL
   cd beer-dashboard
````

2. **Build and start with Docker Compose**

   ```bash
   docker compose --build
   ```
   Optionally add -d to free terminal

   * This builds the Flask image, creates the database volume, and runs the web service on port 5001.

3. **Access the app**
   Open your browser to [http://localhost:5001](http://localhost:5001).

4. **Stop the services**

   ```bash
   docker compose down
   ```

---

## Usage

* **Sign Up**: Visit `/signup`, choose a username/password/major.
* **Log In**: Visit `/login` and enter your credentials.
* **Dashboard (/profile)**:

  * View your Major, Beers consumed, and Money spent.
  * “Have another beer 🍺” to increment your count.
  * “Delete user 💀” to remove your account.
  * See the Top Beer Drinkers leaderboard.
* **Log Out**: Click “Log out” at the bottom of your profile page.

Flash messages indicate success or errors throughout.

---

## Stack

* Frontend: HTML, CSS
* Backend: Flask, SQLAlchemy, PostgreSQL
* Docker and Docker Compose to tie everything together

---

We use SQLAlchemy, which lets us define Python classes (models) that map directly to database tables. Throughout the app, we treat these models almost like SQL tables—e.g., User.query.filter_by(username=…) translates to a SELECT * FROM users WHERE username=…. When a user “drinks another beer,” we simply increment that model’s beer_count attribute and commit the session, and SQLAlchemy generates the appropriate UPDATE statement under the hood. All create, read, update, and delete operations in the app are performed via SQLAlchemy’s query API rather than writing raw SQL, making our code more concise and easier to maintain
