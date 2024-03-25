import re

from motor.motor_asyncio import AsyncIOMotorClient

mongo_client = AsyncIOMotorClient("mongodb://mongo:27017/")
db = mongo_client["document_db"]
collection = db["documents"]


def clean_and_tokenize(text):
    # Remover espaços e símbolos indesejados usando expressão regular
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    # Dividir o texto em tokens usando espaços como delimitador
    tokens = cleaned_text.split()
    return tokens


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
