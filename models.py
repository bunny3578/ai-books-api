from pydantic import BaseModel
from datetime import datetime


class BookCreate(BaseModel):
    """
    用於接收前端建立或更新書籍的資料模型
    """

    title: str
    author: str
    publisher: str | None = None
    price: int
    publish_date: str | None = None
    isbn: str | None = None
    cover_url: str | None = None


class BookResponse(BookCreate):
    """
    用於回應給前端的完整書籍資料模型 (包含 id 與 created_at)
    """

    id: int
    created_at: datetime
