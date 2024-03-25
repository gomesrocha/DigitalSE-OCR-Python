from motor.motor_asyncio import AsyncIOMotorClient
from infra.config import settings


mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
db = mongo_client[settings.MONGODB_DB]
collection = db[settings.MONGODB_COLLECTION]


async def index_document(document_id, tokens):
    for token in tokens:
        await collection.update_one(
            {"_id": token},
            {"$addToSet": {"documents": document_id}},
            upsert=True
        )


async def search_documents(keyword):
    result = await collection.find_one({"_id": keyword})
    if result:
        return result.get("documents", [])
    else:
        return []
