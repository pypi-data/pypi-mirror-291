from enum import StrEnum
from pydantic import BaseModel, Field
from sqlalchemy import select, func, Select
from sqlalchemy.orm import Session

class PaginationManagerExceptionErrors(StrEnum):
    VERY_LARGE_PAGE_SIZE = "Page size exceeds the maximum configured limit of {}."
    PAGE_SIZE_NOT_ALLOWED = "The page size must be greater than zero or has an illegal value."

class PaginationParameters(BaseModel):
    """Descripcion
    :param page:int         : Page number.
    :param page_size:int    : Page size.
    """
    page:int = Field(default=1)
    page_size:int = Field(default=50)

class Page(BaseModel):
    """Descripcion
    :param items:list           : Query results list.
    :param page_size:int        : Number of page records.
    :param page:int             : Current page.
    :param total_pages:int      : Number of pages.
    :param total_records:int    : Number of records.
    """
    items:list= Field(default=[])
    page_size:int= Field(default=50)
    page:int= Field(default=1)
    total_pages:int= Field(default=1)
    total_records:int= Field(default=0)
    def __init__(self, kwargs:dict=None):
        if kwargs is not None:
            super().__init__(**kwargs)

class PaginationManager:
    def __init__(self,page_size_limit:int=50) -> None:
        """Description
        :param page_size_limit(int): Used to not allow pages that are too large. Default 50."""
        self.page_size_limit=page_size_limit

    def query_pagination(self,query:Select, connection_session:Session, params:PaginationParameters=PaginationParameters(),return_dict:bool=True,page_size_limit:int=None,count_records:bool=True)->Page|dict:
            """Description
            If there are too many records, it is recommended that the frontend the first time when creating the grid request page 1 with count_records=True to capture total_pages and total_records; The following page views with count_records=False.
            
            :param: query(str)                      : Complete database query submitted by user.
            :param: connection_session(Session)     : SQLAlchemy session connection.
            :param: params(PaginationParameters)    : These are the pagination parameters to be used or are assigned by default.
            :param: return_dict(bool)               : If it is true, a standard dictionary will be returned or if it is false, the Page and SQLAlchemy type information will be left as it is in the query.
            :param: page_size_limit (int)           : Policy for the number of records per page, if None, the global variable self.page_size_limit will be used.
            :param: count_records(bool)             : If true, the records will be counted. If false, the counting information will be -1 and no counting will be done.

            ### Example
            ```Python
            from fastapi import APIRouter, Depends
            from fastapi.encoders import jsonable_encoder
            from fastapi.responses import JSONResponse
            from sqlalchemy import select

            router = APIRouter(prefix="/api/v1/pagination", tags={"Pagination"})

            @router.get("/id/")
            def get_data_by_id(id:int=0,params:PaginationParameters = Depends(), connection_session: Session = Depends(get_db)):
                query = select(Pagination).order_by(Pagination.id)
                page=query_pagination(query,connection_session,params)
                return JSONResponse(content=jsonable_encoder(page))
            ```
            """
            # Page size policy validation
            if params.page_size <=0: raise ValueError(PaginationManagerExceptionErrors.PAGE_SIZE_NOT_ALLOWED)
            if page_size_limit is None:
                if params.page_size > self.page_size_limit:
                    raise ValueError(PaginationManagerExceptionErrors.VERY_LARGE_PAGE_SIZE.format(self.page_size_limit))
            else:
                if params.page_size > page_size_limit:
                    raise ValueError(PaginationManagerExceptionErrors.VERY_LARGE_PAGE_SIZE.format(page_size_limit))
            
            # Count
            if count_records:
                query_for_count_registries = select(func.count()).select_from(query.subquery())
                total_records = connection_session.execute(query_for_count_registries).scalar()
                total_pages = (total_records + params.page_size - 1) // params.page_size
            else:
                total_records=-1
                total_pages=-1
            # Paginate query
            offset = (params.page - 1) * params.page_size
            paginate_query = query.offset(offset).limit(params.page_size)
            item_dict = {}
            items = []
            is_dict=False
            columns = [col.key for col in query.columns]            
            for row in connection_session.execute(paginate_query).all():
                column_i=0
                for value in row:
                    if hasattr(value, '_sa_instance_state'):
                        data = value.__dict__
                        del data["_sa_instance_state"]
                        items.append(data)
                    else:
                        item_dict[columns[column_i]]=value
                        column_i=column_i+1
                        is_dict=True
                if is_dict:
                    items.append(item_dict)
                    item_dict = {}
            page_dictionary={
                "items": items,
                "page_size": params.page_size,
                "page": params.page,
                "total_pages": total_pages,
                "total_records": total_records,
            }
            if return_dict:
                return page_dictionary
            else:
                return Page(page_dictionary)
