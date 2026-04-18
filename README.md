# Pokédex Backend

A FastAPI backend with PostgreSQL for a Pokédex app featuring user authentication and favorites.
### Framework : FastAPI
### DB : PostgreSQL 
Seeder : [pokemon](https://pokeapi.co/)



# Setup Guide


## Prerequisites

Make sure you have the following installed before starting:

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **PostgreSQL** — [postgresql.org](https://www.postgresql.org/download/)
- **pip** (comes with Python)

---

## Step 1 — Clone the project

```bash
git clone <https://github.com/jam-bri/pokedex_backend>
cd <pokedex_backend>
```

---

## Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3 — Set up PostgreSQL

### 3.1 — Create the database

Open a terminal and connect to PostgreSQL:

```bash
psql -U postgres
```

Then run:

```sql
CREATE DATABASE pokedex_db;
```

Type `\q` to exit.

### 3.2 — Update the database URL

Open `database.py` and update the connection string with your own PostgreSQL credentials:

```python
DATABASE_URL = "postgresql://<username>:<password>@localhost:5432/pokedex_db"
```

Replace `<username>` and `<password>` with your actual PostgreSQL username and password.

> **Never commit this file with real credentials to a public repository.**  

---

## Step 4 — Populate the database with Pokémon data

Run the seeder script to create the tables and import the first 151 Pokémon from [pokeapi.co](https://pokeapi.co):

```bash
python import_pokemon.py
```

> This will take a minute — it fetches each Pokémon one by one with a small delay to avoid overloading the API. You'll see each Pokémon name printed as it's imported.

---

## Step 5 — Run the server

```bash
uvicorn main:app --reload
```

The API will be available at: **http://localhost:8000**

You can explore the interactive API docs at: **http://localhost:8000/docs**

---

## API Overview

### Auth

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/register` | Create a new account | NO |
| POST | `/signin` | Log in and receive a token | NO |
| POST | `/signout` | Log out | YES |

### Pokémon

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/pokemon` | Get all Pokémon | NO |
| GET | `/pokemon/id/{id}` | Get a Pokémon by ID | NO |
| GET | `/pokemon/name/{name}` | Get a Pokémon by name | NO |

### Favorites

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/favorites` | Get your favorites | YES |
| POST | `/favorites` | Add a Pokémon to favorites | YES |
| DELETE | `/favorites/{pokemon_id}` | Remove from favorites | YES |

### How to authenticate

After signing in, you'll receive a `token`. It'll be passed in the `Authorization` header for protected routes:

```
Authorization: Bearer <your_token>
```

---

## Project Structure

```
├── main.py           # API routes and app setup
├── models.py         # Database models (Pokemon, Favorites, User)
├── database.py       # Database connection
├── import_pokemon.py # Script to populate the database
├── requirements.txt  # Python dependencies
├── ai_exchanges.md  # Echanges with AI.
```

---

## Common Issues

**`Connection refused` on PostgreSQL**  
→ Make sure PostgreSQL is running. On most systems: `sudo service postgresql start` (Linux) or start it from the app (macOS/Windows).

**`password authentication failed`**  
→ Double-check the username and password in `DATABASE_URL` in `database.py`.

**`Module not found` errors**  
→ Make sure you ran `pip install -r requirements.txt` and that you're using the right Python environment.

**Seeder script fails mid-way**  
→ It's safe to re-run `import_pokemon.py` — it checks for existing Pokémon before inserting, so no duplicates will be created.

## Ressources 
https://youtu.be/1Nhl4gikGZY?si=QsPb8PNsTsmilJ8l
https://youtu.be/5GxQ1rLTwaU?si=ZTQEp5NmB1vgxvJF
https://youtu.be/QDWdFLOS6OE?si=_Z2hc6Q0roWUKq9r
https://youtu.be/398DuQbQJq0?si=QPXZWi3bCSew7nad
https://youtu.be/HEV1PWycOuQ?si=8jSHfwVm_2TEma6y
https://youtu.be/iWS9ogMPOI0?si=QShnQDzjJaAnOUba