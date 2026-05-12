def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_get_one_task(client):
    r = client.post("/api/tasks", json={"title": "Task 1"})
    assert r.status_code == 201

    r = client.get("/api/tasks/one")
    assert r.status_code == 200

    body = r.get_json()
    assert body["title"] == "Task 1"
    assert body["done"] is False
    assert "id" in body

def test_tasks_crud(client):
    r = client.get("/api/tasks")
    assert r.status_code == 200
    assert r.get_json() == []

    r = client.post("/api/tasks", json={"title": "  Kup mleko  "})
    assert r.status_code == 201
    body = r.get_json()
    assert body["title"] == "Kup mleko"
    assert body["done"] is False
    tid = body["id"]

    r = client.patch(f"/api/tasks/{tid}", json={"done": True})
    assert r.status_code == 200
    assert r.get_json()["done"] is True

    r = client.get("/api/tasks")
    assert len(r.get_json()) == 1


def test_create_task_validation(client):
    r = client.post("/api/tasks", json={})
    assert r.status_code == 400
