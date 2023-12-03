from litestar.contrib.sqlalchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session, Query
from app.models import Author, Book


class AuthorRepository(SQLAlchemySyncRepository[Author]):
    model_type = Author

async def provide_authors_repo(db_session: Session):
    return AuthorRepository(session=db_session, auto_commit=True)


class BookRepository(SQLAlchemySyncRepository[Book]):
    model_type = Book

    def search_by_title(self, title: str) -> list[Book]:
        query: Query[Book] = self.session.query(Book).filter(Book.title.istartswith(title))
        return query.all()
    
async def provide_books_repo(db_session: Session):
    return BookRepository(session=db_session, auto_commit=True)