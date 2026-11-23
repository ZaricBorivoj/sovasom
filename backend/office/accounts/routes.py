import hashlib
import secrets
from datetime import timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from office.accounts.models import Account, Grant, LoginSession, Membership

router = APIRouter(prefix="/api")
SESSION_COOKIE = "__Host-office_session"
CSRF_COOKIE = "__Host-office_csrf"
LIFETIME = timedelta(days=30)
passwords = PasswordHasher()
# Equal-cost verification for unknown email addresses; no usable account credential.
dummy_hash = passwords.hash(secrets.token_urlsafe(32))


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def database(request: Request):
    with request.app.state.sessions() as db:
        yield db


def current_session(request: Request, db: Session = Depends(database)) -> LoginSession:
    token = request.cookies.get(SESSION_COOKIE, "")
    session = db.get(LoginSession, digest(token)) if token else None
    if not session or session.revoked_at or session.expires_at <= request.app.state.now():
        raise HTTPException(401, "Please sign in again.")
    account = db.get(Account, session.account_id)
    if not account or not account.enabled:
        raise HTTPException(401, "Please sign in again.")
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        if not secrets.compare_digest(
            session.csrf_hash, digest(request.cookies.get(CSRF_COOKIE, ""))
        ):
            raise HTTPException(403, "Refresh the page and try again.")
    return session


def office_member(
    session: LoginSession = Depends(current_session), db: Session = Depends(database)
) -> Account:
    membership = db.get(Membership, session.account_id)
    if not membership or not membership.active:
        raise HTTPException(403, "Your office access is no longer available.")
    return db.get(Account, session.account_id)


def profile(account: Account, csrf: str, db: Session) -> dict:
    roles = set(db.scalars(select(Grant.role).where(Grant.account_id == account.id)))
    return {
        "account": {
            "id": str(account.id),
            "email": account.email,
            "display_name": account.display_name,
            "is_administrator": "administrator" in roles,
            "is_menu_maintainer": "menu_maintainer" in roles,
        },
        "csrf_token": csrf,
    }


def cookie(response: Response, name: str, value: str, max_age: int):
    response.set_cookie(
        name, value, max_age=max_age, secure=True, httponly=True, samesite="strict", path="/"
    )


def session_csrf(request: Request, response: Response, session: LoginSession, db: Session) -> str:
    token = request.cookies.get(CSRF_COOKIE, "")
    if not secrets.compare_digest(session.csrf_hash, digest(token)):
        # A cross-site top-level CSRF navigation can replace the Strict cookie
        # while omitting the session. Repair its binding on authenticated return.
        token = secrets.token_urlsafe(32)
        session.csrf_hash = digest(token)
        db.commit()
        remaining = int((session.expires_at - request.app.state.now()).total_seconds())
        cookie(response, CSRF_COOKIE, token, max(0, remaining))
    return token


@router.get("/auth/csrf")
def csrf(request: Request, response: Response, db: Session = Depends(database)):
    session = db.get(LoginSession, digest(request.cookies.get(SESSION_COOKIE, "")))
    if session and not session.revoked_at and session.expires_at > request.app.state.now():
        return {"csrf_token": session_csrf(request, response, session, db)}
    token = secrets.token_urlsafe(32)
    cookie(response, CSRF_COOKIE, token, 3600)
    return {"csrf_token": token}


class Credentials(BaseModel):
    email: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=1, max_length=1024, repr=False)


@router.post("/auth/login")
def login(
    credentials: Credentials, request: Request, response: Response, db: Session = Depends(database)
):
    account = db.scalar(
        select(Account).where(Account.email == credentials.email.strip().casefold())
    )
    try:
        passwords.verify(account.password_hash if account else dummy_hash, credentials.password)
    except VerificationError:
        raise HTTPException(401, "Email or password is incorrect.") from None
    if not account or not account.enabled:
        raise HTTPException(401, "Email or password is incorrect.")
    membership = db.get(Membership, account.id)
    if not membership or not membership.active:
        raise HTTPException(403, "Your office access is no longer available.")
    now = request.app.state.now()
    if old_token := request.cookies.get(SESSION_COOKIE):
        if old_session := db.get(LoginSession, digest(old_token)):
            old_session.revoked_at = now
    token, csrf_token = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
    db.add(
        LoginSession(
            token_hash=digest(token),
            account_id=account.id,
            csrf_hash=digest(csrf_token),
            created_at=now,
            expires_at=now + LIFETIME,
        )
    )
    db.commit()
    cookie(response, SESSION_COOKIE, token, int(LIFETIME.total_seconds()))
    cookie(response, CSRF_COOKIE, csrf_token, int(LIFETIME.total_seconds()))
    return profile(account, csrf_token, db)


@router.get("/auth/session")
def session_info(
    request: Request,
    response: Response,
    account: Account = Depends(office_member),
    session: LoginSession = Depends(current_session),
    db: Session = Depends(database),
):
    return profile(account, session_csrf(request, response, session, db), db)


@router.post("/auth/logout", status_code=204)
def logout(
    request: Request,
    response: Response,
    session: LoginSession = Depends(current_session),
    db: Session = Depends(database),
):
    session.revoked_at = request.app.state.now()
    db.commit()
    for name in [SESSION_COOKIE, CSRF_COOKIE]:
        cookie(response, name, "", 0)


@router.get("/office/home")
def home(account: Account = Depends(office_member)):
    return {"active_run": None, "history": []}
