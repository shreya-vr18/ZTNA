# ZTNA — Zero Trust Network Access

A Zero Trust Network Access (ZTNA) system that replaces implicit "inside the network = trusted" access with per-request, identity- and context-based verification. Every access request is evaluated individually using dynamic trust scoring, rather than relying on a one-time login.

## Problem Statement

Traditional VPN-based access grants broad network access after a single authentication step — if credentials are compromised, an attacker can move laterally across the entire network. ZTNA enforces "never trust, always verify," continuously evaluating risk based on identity, device, location, and behavior before granting access to any resource.

## Features

- **JWT-based Authentication** — stateless, signature-verified access tokens with refresh token rotation
- **Role-Based Access Control (RBAC)** — permissions scoped precisely to each user's role
- **Dynamic Trust Scoring** — per-session risk evaluation based on:
  - Identity & credential strength
  - Device fingerprint
  - Login location
  - Login time patterns
  - Behavioral/usage patterns
- **Micro-segmentation** — access scoped tightly to only the resources a user needs, not the whole network
- **Session Logging** — all access attempts logged via SQLite for auditability

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Authentication | JWT |
| Database | SQLite |
| Language | Python |

## Team

| Member | Area |
|---|---|
| Shreya V R | Identity & Credential Risk Scoring |
| Vaishnavi R D | Device & Location Risk Scoring |
| Akash P Bhat | Behavioral Risk & Trust Score Aggregation |

## Project Structure

```text
ztna-project/
├── README.md
├── .gitignore
├── requirements.txt
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── auth.py              # Login endpoint, JWT creation, refresh logic
│   ├── models.py            # Pydantic models + DB schema
│   ├── database.py          # SQLite connection setup
│   └── risk/
│       ├── identity_risk.py     # Shreya V R — identity/credential scoring
│       ├── device_risk.py       # Vaishnavi R D — device & location scoring
│       └── risk_engine.py       # Akash P Bhat — aggregation & final decision
│
├── database/
│   └── ztna.db               # SQLite database file (auto-created on first run)
│
└── frontend/
    └── (teammate's frontend files, if part of this repo)
```
## Setup

```bash
# Clone the repository
git clone https://github.com/<owner>/<repo-name>.git
cd <repo-name>

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

Server runs at `http://127.0.0.1:8000` — interactive API docs available at `http://127.0.0.1:8000/docs`.

## How It Works

1. User authenticates → server verifies credentials + evaluates initial trust score
2. On success, server issues a short-lived **access token** and a longer-lived **refresh token**
3. Every subsequent request includes the access token in the `Authorization` header
4. Server verifies the token signature and checks the role/permission (RBAC) for the requested resource
5. Access token expires periodically; client uses the refresh token to obtain a new one without re-login
6. All access attempts are logged for audit purposes

## Future Scope

- AI-based dynamic risk analysis for adaptive trust scoring
- Blockchain-based audit trail for tamper-proof session logs

## License

MIT
