from litestar import Controller, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from advanced_alchemy.exceptions import NotFoundError 
from app.dtos import (
    AuthorReadDTO,
    AuthorReadFullDTO,
    AuthorUpdateDTO,
    AuthorWriteDTO,
    BookReadDTO,
    BookReadFullDTO,
    BookWriteDTO,
    BookUpdateDTO,
)
from app.models import Author, Book
from app.repositories import (
    AuthorRepository,
    BookRepository,
    provide_authors_repo,
    provide_books_repo,
)
from sqlalchemy.orm import Session


class AuthorController(Controller):
    path = "/authors"
    tags = ["authors"]
    return_dto = AuthorReadDTO
    dependencies = {"authors_repo": Provide(provide_authors_repo)}

    @get()
    async def list_authors(self, authors_repo: AuthorRepository) -> list[Author]:
        return authors_repo.list()

    @post("/", dto=AuthorWriteDTO)
    async def create_author(self, data: Author, authors_repo: AuthorRepository) -> Author:
        return authors_repo.add(data)

    @get("/{author_id:int}", return_dto=AuthorReadFullDTO)
    async def get_author(self, author_id: int, authors_repo: AuthorRepository) -> Author:
        try:
            author = authors_repo.get(author_id)
            if not author:
                raise ValueError("El autor no existe")
            return author
        except NotFoundError:
            raise HTTPException(status_code=404, detail="El autor no existe")
            

    @patch("/{author_id:int}", dto=AuthorUpdateDTO)
    async def update_author(
        self, author_id: int, data: DTOData[Author], authors_repo: AuthorRepository
    ) -> Author:  
        try:
            author = authors_repo.get(author_id)
            if not author:
                raise ValueError("El autor no existe")
            author = data.update_instance(author)
            authors_repo.add(author)
            return author
        except NotFoundError:
            raise HTTPException(status_code=404, detail="El autor no existe")


class BookController(Controller):
    path = "/books"
    tags = ["books"]
    return_dto = BookReadDTO
    dependencies = {"books_repo": Provide(provide_books_repo)}
    # En resumen, esta línea establece que el controlador 
    # BookController depende de un repositorio de libros 
    # (books_repo) que será proporcionado por la función 
    # provide_books_repo. Este enfoque facilita la inyección 
    # de dependencias y hace que el controlador sea más modular 
    # y fácil de probar.
    @get()
    async def list_books(self, books_repo: BookRepository) -> list[Book]:
        return books_repo.list()

    @post(dto=BookWriteDTO)
    async def create_book(self, data: Book, books_repo: BookRepository) -> Book:
        return books_repo.add(data)
    
    @get("/{book_id:int}", return_dto=BookReadFullDTO)
    async def get_book(self, book_id: int, books_repo: BookRepository) -> Book:
        try:
            book = books_repo.get(book_id)
            if not book:
                raise ValueError("El libro no existe")
            return book
        except NotFoundError:
            raise HTTPException(status_code=404, detail="El libro no existe")
    
    @patch("/{book_id:int}", dto=BookUpdateDTO)
    async def update_book(
        self, book_id: int, data: DTOData[Book], books_repo: BookRepository
    ) -> Book:
        try:
            book = books_repo.get(book_id)
            if not book:
                raise ValueError("El libro no existe")
            book = data.update_instance(book)
            return book
        except NotFoundError:
            raise HTTPException(status_code=404, detail="El libro no existe")


    @get("/search", return_dto=BookReadFullDTO)
    async def get_book_by_title(
        self, title: str, books_repo: BookRepository
        ) -> list[Book]:
        try:
            books = books_repo.search_by_title(title)
            if not books:
                raise NotFoundError("Libro no encontrado")
            return books
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

