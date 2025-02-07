from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from books.schemas import Book
from typing import List



book_router = APIRouter()


@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return books


@book_router.get("/user/{user_uid}", response_model=List[Book], dependencies=[role_checker])
async def get_user_book_submissions():
    books = await book_service.get_user_books(user_uid, session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker],
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(acccess_token_bearer),
) -> dict:
    user_id = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book_data, user_id, session)
    return new_book


@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(acccess_token_bearer),
) -> dict:
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise BookNotFound()


@book_router.patch("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(acccess_token_bearer),
) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None:
        raise BookNotFound()
    else:
        return updated_book


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(acccess_token_bearer),
):
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        raise BookNotFound()
    else:
        return {}
    



@app.put("/posts/{id}")
def update_post(id:int, post:Post)-> dict:    
    cursor.execute("""UPDATE posts SET title = %s, content = %s, publish = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.publish, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    return {"data":updated_post}


@app.get("/get_headers")
async def get_headers(
    accept : str = Header(None), 
    content_type : str = Header(None),
    user_agent : str = Header(None), 
    host : str = Header(None)
    ):

    request_headers = {}
    request_headers["accept"] = accept
    request_headers["content_type"] = content_type
    request_headers["user_agent"] = user_agent
    request_headers["host"] = host
    return request_headers