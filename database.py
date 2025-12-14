import sqlite3


def get_db_connection() -> sqlite3.Connection:
    """建立資料庫連線並設定 row_factory"""
    conn = sqlite3.connect("bokelai.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_all_books(skip: int = 0, limit: int = 100) -> list[dict]:
    """取得所有書籍 (分頁)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?", (limit, skip))
    books = cursor.fetchall()
    conn.close()
    return [dict(book) for book in books]


def get_book_by_id(book_id: int) -> dict | None:
    """根據 ID 取得單一書籍"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    if book:
        return dict(book)
    return None


def create_book(
    title: str,
    author: str,
    publisher: str | None,
    price: int,
    publish_date: str | None,
    isbn: str | None,
    cover_url: str | None,
) -> int:
    """新增一本書，回傳新書籍的 ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO books (title, author, publisher, price, publish_date, isbn, cover_url)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (title, author, publisher, price, publish_date, isbn, cover_url),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_book(
    book_id: int,
    title: str,
    author: str,
    publisher: str | None,
    price: int,
    publish_date: str | None,
    isbn: str | None,
    cover_url: str | None,
) -> bool:
    """更新書籍資訊，回傳是否更新成功"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE books
           SET title=?, author=?, publisher=?, price=?, publish_date=?, isbn=?, cover_url=?
           WHERE id=?""",
        (title, author, publisher, price, publish_date, isbn, cover_url, book_id),
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0


def delete_book(book_id: int) -> bool:
    """刪除書籍，回傳是否刪除成功"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0
