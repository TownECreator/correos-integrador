import os
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

DB_PATH = "users.db"
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "cambia-esta-clave-en-produccion-demo")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Auth Service - Correos Internos")


def hash_password(password: str) -> str:
    raw = password.encode("utf-8")[:72]
    return bcrypt.hashpw(raw, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    raw = password.encode("utf-8")[:72]
    return bcrypt.checkpw(raw, password_hash.encode("utf-8"))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL DEFAULT 'Empleado',
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: Optional[str] = "Empleado"


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}


@app.post("/register", status_code=201)
def register(data: RegisterRequest):
    role = data.role if data.role in ("Empleado", "Admin") else "Empleado"
    password_hash = hash_password(data.password)
    created_at = datetime.now(timezone.utc).isoformat()

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, role, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (data.username, role, password_hash, created_at),
        )
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    conn.close()

    return {
        "message": "Usuario registrado correctamente",
        "user_id": user_id,
        "username": data.username,
        "role": role,
    }


@app.post("/login")
def login(data: LoginRequest):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, role, password_hash FROM users WHERE username = ?",
        (data.username,),
    )
    user = cur.fetchone()
    conn.close()

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    exp = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user["id"]),
        "username": user["username"],
        "role": user["role"],
        "exp": exp,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in_minutes": TOKEN_EXPIRE_MINUTES,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
        },
    }


@app.get("/verify")
def verify_token(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token faltante o mal formado")

    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "valid": True,
            "user_id": payload.get("sub"),
            "username": payload.get("username"),
            "role": payload.get("role"),
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
