from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from . database import engine
from . routers import users, posts, auth, votes
from . config import settings

#
# if you have alembic then this create is not required.
# This is required only incase of sqlalchemy without alembic.
#
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://www.google.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get('/')
async def root():
    return {"message": "Hello World!!!!! This is my first Fast API app"}


##############################################################################################################
##
## Any code within this block is kept for reference purpose 
##
## In-Memory (based on global variable) solution.
## Copied this code before converting into DB specific
##
##

# my_posts = [{"id": 1, "title": "first post", "content": "first post content", "published": True, "rating":2},
#            {"id": 2, "title": "second post", "content": "second post content", "published": True, "rating":3}]

# @app.get('/posts')
# async def get_posts():
#     return {"data": my_posts}

# @app.get('/posts/latest')
# async def get_latest_post(response: Response):
#     if len(my_posts) == 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts were found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"data": f"post with id:{id} is not found"}
#     return {"data": my_posts[len(my_posts)-1]}

# @app.get('/posts/{id}')
# async def get_post(id: int, response: Response):
#     data = [x for x in my_posts if x['id'] == id]
#     if len(data) == 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} is not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"data": f"post with id:{id} is not found"}
#     return {"data": data.pop()}

# @app.get('/posts/{id}')
# async def get_post(id: int, response: Response):
#     cur.execute(f"""SELECT * FROM posts WHERE id = {id}""")
#     record = cur.fetchone()
#     if record is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} is not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"data": f"post with id:{id} is not found"}
#     return {"data": record}

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_posts(payload: Post):
#     print(payload.dict())
#     my_post = payload.dict()
#     my_post['id'] = randrange(0, 100000)
#     my_posts.append(my_post)
#     return {"data" : my_post}

# @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_posts(id: int):
#     data = [x for x in my_posts if x['id'] == id]
#     if len(data) > 0:
#         my_posts.remove(data[0])
#         return Response(status_code=status.HTTP_204_NO_CONTENT)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

# @app.put('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def update_posts(id: int, payload: Post):
#     data = [x for x in my_posts if x['id'] == id]
#     if len(data) > 0:
#         req_data = payload.dict()
#         req_data['id'] = id
#         index = my_posts.index(data[0])
#         my_posts.pop(index)
#         my_posts.insert(index, req_data)
#         return Response(status_code=status.HTTP_204_NO_CONTENT)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

##############################################################################################################


##############################################################################################################
##
## Any code within this block is kept for reference purpose 
##
## Direct Postgres SQL talk with psycopg DB driver.
## Copied this code before converting into DB ORM specific
##
##

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     rating: Optional[int] = None


# while True:
#     try:
#         conn = psycopg.connect("host= 127.0.0.1 dbname=fastapi user=postgres")
#         cur = conn.cursor(row_factory=psycopg.rows.dict_row)
#         break
#     except Exception as ex:
#         print(ex)
#         time.sleep(1)

# @app.get('/')
# async def root():
#     return {"message": "Hello World!!! This is my first Fast API app"}

# @app.get('/posts')
# async def get_posts():
#     cur.execute("SELECT * FROM posts")
#     my_posts = cur.fetchall()
#     if len(my_posts) == 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts were found")    
        
#     return {"data": my_posts}

# @app.get('/posts/latest')
# async def get_latest_post(response: Response):
#     cur.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
#     record = cur.fetchone()
#     if record is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts were found")
#     return {"data": record}

# @app.get('/posts/{id}')
# async def get_post(id: int, response: Response):
#     cur.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
#     record = cur.fetchone()
#     if record is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} is not found")
#     return {"data": record}

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_posts(payload: Post):
#     print(payload.dict())
#     my_post = payload.dict()
#     cur.execute("""INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING *""",
#                         (payload.title, payload.content, payload.published, payload.rating))
#     conn.commit()
#     record = cur.fetchone()
#     if record is None:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"post with id:{id} is not found")    
#     return {"data" : record}


# @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_posts(id: int):
#     cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     deleted_post = cur.fetchone()

#     if deleted_post is not None:
#         conn.commit()
#         return Response(status_code=status.HTTP_204_NO_CONTENT)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

# @app.put('/posts/{id}', status_code=status.HTTP_200_OK)
# def update_posts(id: int, payload: Post):
#     cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING *""",
#                     (payload.title, payload.content, payload.published, payload.rating, str(id)))
#     updated_post = cur.fetchone()

#     if updated_post is not None:
#         conn.commit()
#         return Response(status_code=status.HTTP_200_OK)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

##############################################################################################################