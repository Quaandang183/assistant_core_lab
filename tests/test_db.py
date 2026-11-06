from datetime import datetime, timedelta, timezone

import httpx
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from assistant_api.db import ChatSession, Feedback, Interaction, Repository, hash_session, init_db, make_engine
from assistant_api.main import create_app
from assistant_api.weather import WeatherClient


def make_repo():
    engine = make_engine("sqlite://")
    init_db(engine)
    return Repository(engine, "salt"), engine


def test_session_id_is_hashed():
    repo, engine = make_repo()
    repo.record_interaction("student-42", "r1", "fee", None, True, False, 3.0)
    with Session(engine) as db:
        s = db.exec(select(ChatSession)).one()
    assert s.id == hash_session("student-42", "salt") and "student-42" not in s.id


def test_one_session_many_interactions():
    repo, engine = make_repo()
    for i in range(3):
        repo.record_interaction("s", f"r{i}", "rule", "H26-5.3", True, False, 10.0)
    with Session(engine) as db:
        assert len(db.exec(select(ChatSession)).all()) == 1
        assert len(db.exec(select(Interaction)).all()) == 3


def test_feedback_requires_existing_interaction():
    repo, _ = make_repo()
    assert repo.add_feedback("missing", 1, None) is None
    repo.record_interaction("s", "r1", "fee", None, True, False, 1.0)
    assert repo.add_feedback("r1", -1, "wrong fee").id == 1


# ---- R2: list_feedback ----
def test_list_feedback_newest_first_and_limit():
    repo, engine = make_repo()
    repo.record_interaction("s", "r1", "fee", None, True, False, 1.0)
    base = datetime(2026, 11, 1, tzinfo=timezone.utc)
    with Session(engine) as db:  # fixed timestamps, so the order does not depend on the clock
        for i, comment in enumerate(["oldest", "middle", "newest"]):
            db.add(Feedback(request_id="r1", rating=1, comment=comment, created_at=base + timedelta(minutes=i)))
        db.commit()
    assert [f.comment for f in repo.list_feedback()] == ["newest", "middle", "oldest"]
    assert [f.comment for f in repo.list_feedback(limit=2)] == ["newest", "middle"]


def test_list_feedback_empty():
    repo, _ = make_repo()
    assert repo.list_feedback() == []


def test_intent_stats():
    repo, _ = make_repo()
    repo.record_interaction("s", "r1", "fee", None, True, False, 10.0)
    repo.record_interaction("s", "r2", "fee", None, True, False, 20.0)
    repo.record_interaction("s", "r3", "unknown", None, False, False, 5.0)
    stats = repo.intent_stats()
    assert stats[0] == {"intent": "fee", "requests": 2, "avg_latency_ms": 15.0, "unresolved": 0}
    assert stats[1]["intent"] == "unknown" and stats[1]["unresolved"] == 1


# ---- the data survives a restart ----
def test_feedback_survives_restart(tmp_path):
    url = f"sqlite:///{tmp_path / 'assistant.db'}"

    first = Repository(make_engine(url), "salt")
    init_db(first.engine)
    first.record_interaction("s", "r1", "fee", None, True, False, 1.0)
    first.add_feedback("r1", 1, "thanks")
    first.engine.dispose()  # "stop the server"

    second = Repository(make_engine(url), "salt")  # "start it again"
    init_db(second.engine)
    assert [(f.request_id, f.rating, f.comment) for f in second.list_feedback()] == [("r1", 1, "thanks")]


def test_api_feedback_survives_restart(tmp_path, settings, service):
    url = f"sqlite:///{tmp_path / 'assistant.db'}"
    settings = settings.model_copy(update={"api_admin_key": "secret-admin", "database_url": url, "session_salt": "x"})
    down = WeatherClient(
        "https://example.test", 10.76, 106.68, retries=1, transport=httpx.MockTransport(lambda r: httpx.Response(500))
    )

    first = TestClient(create_app(settings, service, down))
    rid = first.post("/v1/chat", json={"message": "hi"}).json()["request_id"]
    assert first.post("/v1/feedback", json={"request_id": rid, "rating": 1}).status_code == 201

    second = TestClient(create_app(settings, service, down))  # a new app on the same database file
    listed = second.get("/v1/feedback", headers={"X-API-Key": "secret-admin"}).json()
    assert [f["request_id"] for f in listed] == [rid]


# ---- privacy by design ----
def test_raw_message_is_never_stored(tmp_path, settings, service):
    url = f"sqlite:///{tmp_path / 'assistant.db'}"
    settings = settings.model_copy(update={"database_url": url})
    down = WeatherClient(
        "https://example.test", 10.76, 106.68, retries=1, transport=httpx.MockTransport(lambda r: httpx.Response(500))
    )
    secret = "my phone is 0901234567"
    TestClient(create_app(settings, service, down)).post(
        "/v1/chat", json={"message": secret, "session_id": "student-7"}
    )

    import sqlite3

    con = sqlite3.connect(tmp_path / "assistant.db")
    dump = "\n".join(con.iterdump())
    con.close()
    assert "0901234567" not in dump and "student-7" not in dump


def test_secrets_are_not_in_settings_repr(settings):
    assert "dev-salt" not in repr(settings.model_copy(update={"session_salt": "dev-salt"}))
