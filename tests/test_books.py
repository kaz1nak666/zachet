from fastapi.testclient import TestClient

def test_create_book(client: TestClient):
    response = client.post(
        "/books/",
        json={"title": "Test Book", "author": "Tester", "year": 2024, "status": "в планах"},
    )
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "Test Book"
    assert data["status"] == "в планах"
    assert "id" in data

def test_read_books(client: TestClient):
    # Создаем книгу
    client.post(
        "/books/",
        json={"title": "Book 1", "author": "Author 1", "year": 2021},
    )
    
    response = client.get("/books/")
    data = response.json()
    assert response.status_code == 200
    assert len(data) >= 1

def test_update_book(client: TestClient):
    # Создаем книгу
    create_resp = client.post(
        "/books/",
        json={"title": "Book Update", "author": "Author", "year": 2022},
    )
    book_id = create_resp.json()["id"]
    
    # Обновляем
    response = client.patch(
        f"/books/{book_id}",
        json={"status": "прочитано", "rating": 5},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "прочитано"
    assert data["rating"] == 5

def test_delete_book(client: TestClient):
    # Создаем книгу
    create_resp = client.post(
        "/books/",
        json={"title": "Book Delete", "author": "Author", "year": 2023},
    )
    book_id = create_resp.json()["id"]
    
    # Удаляем
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204
    
    # Проверяем что удалена
    get_resp = client.get("/books/")
    books = get_resp.json()
    assert not any(b["id"] == book_id for b in books)

def test_update_not_found(client: TestClient):
    response = client.patch("/books/999", json={"rating": 1})
    assert response.status_code == 404
    assert response.json()["detail"] == "Книга не найдена"

def test_create_invalid_rating(client: TestClient):
    # Попытка создать с рейтингом > 5 (через PATCH, т.к. в BookCreate его нет)
    create_resp = client.post(
        "/books/",
        json={"title": "Invalid Rating", "author": "Author", "year": 2023},
    )
    book_id = create_resp.json()["id"]
    
    response = client.patch(f"/books/{book_id}", json={"rating": 10})
    assert response.status_code == 422
