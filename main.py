from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from graphql.schema import schema
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from redis import Redis
from elasticsearch import AsyncElasticsearch
import beanie
from api.endpoints import router as api_router

app = FastAPI(title=settings.PROJECT_NAME)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# REST API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# GraphQL route
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Database connection
@app.on_event("startup")
async def startup_event():
    # MongoDB connection
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await beanie.init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            "models.animal.Animal",
            "models.employee.Employee",
            "models.habitat.Habitat",
            "models.note.Note"
        ]
    )
    
    # Redis connection
    app.state.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    # Elasticsearch connection
    app.state.es = AsyncElasticsearch(
        hosts=[settings.ELASTICSEARCH_URL]
    )
    
    # Create Elasticsearch indices if they don't exist
    indices = [
        f"{settings.ELASTICSEARCH_INDEX_PREFIX}_animals",
        f"{settings.ELASTICSEARCH_INDEX_PREFIX}_habitats",
        f"{settings.ELASTICSEARCH_INDEX_PREFIX}_notes"
    ]
    
    for index in indices:
        if not await app.state.es.indices.exists(index=index):
            await app.state.es.indices.create(index=index)

@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.es.close()