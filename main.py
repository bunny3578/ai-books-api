from fastapi import FastAPI, HTTPException, Body
import database
import models

app = FastAPI(
    title="博客來 AI 書籍管理 API",
    description="第3次小考",
    version="1.0.0",
)


@app.get("/")
def root():
    """回傳 API 歡迎訊息"""
    return {"message": "AI Books API"}


@app.get("/books", response_model=list[models.BookResponse])
def get_books(skip: int = 0, limit: int = 10):
    """分頁取得書籍（skip, limit）"""
    books = database.get_all_books(skip=skip, limit=limit)
    return books


@app.get("/books/{book_id}", response_model=models.BookResponse)
def get_book(book_id: int):
    """取得單一書籍"""
    book = database.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", status_code=201, response_model=models.BookResponse)
def create_book(book: models.BookCreate = Body(...)):
    """新增一本書"""
    new_id = database.create_book(
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        price=book.price,
        publish_date=book.publish_date,
        isbn=book.isbn,
        cover_url=book.cover_url,
    )
    new_book = database.get_book_by_id(new_id)
    return new_book


@app.put("/books/{book_id}", response_model=models.BookResponse)
def update_book(book_id: int, book: models.BookCreate = Body(...)):
    """完整更新一本書"""
    updated = database.update_book(
        book_id=book_id,
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        price=book.price,
        publish_date=book.publish_date,
        isbn=book.isbn,
        cover_url=book.cover_url,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return database.get_book_by_id(book_id)


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    """刪除一本書"""
    deleted = database.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return
