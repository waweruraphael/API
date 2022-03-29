from distutils.sysconfig import customize_compiler
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .import models
from .database import engine,get_db
from .routers import post,user,auth,vote



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def find_post(id):
#     for P in my_Posts:
#         if P['id'] == id:
#             return P

# def find_index_post(id):
#     for i, q in enumerate(my_Posts):
#         if q['id']  == id:
#             return i      


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def read_root():
     return {"message": "Welcome to fast api "}








