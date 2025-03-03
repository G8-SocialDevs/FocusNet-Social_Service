from fastapi import FastAPI
from app.api import publication
from app.api import comment
from app.api import reaction

app = FastAPI()

app.include_router(publication.router, prefix="/publication", tags=["publication"])
app.include_router(comment.router, prefix="/comment", tags=["comment"])
app.include_router(reaction.router, prefix="/reaction", tags=["reaction"])