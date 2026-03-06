import datetime
import re
from uuid import uuid4
from shortGPT.database.db_document import TINY_MONGO_DATABASE, TinyMongoDocument

from shortGPT.database.content_data_manager import ContentDataManager
class ContentDatabase:
    def __init__(self, ):
        self.content_collection = TINY_MONGO_DATABASE["content_db"]["content_documents"]

    def instanciateContentDataManager(self, id: str, content_type: str, new=False):
        db_doc = TinyMongoDocument("content_db", "content_documents", id)
        return ContentDataManager(db_doc, content_type, new)

    def getContentDataManager(self, id, content_type: str):
        try:
            db_doc = TinyMongoDocument("content_db", "content_documents", id)
            return ContentDataManager(db_doc, content_type, False)
        except:
            return None

    def createContentDataManager(self, content_type: str, descriptive_name: str = None) -> ContentDataManager:
        try:
            now = datetime.datetime.now()
            date_str = now.strftime("%Y%m%d_%H%M%S")
            if descriptive_name:
                safe_name = re.sub(r'[^a-zA-Z0-9_]', '', descriptive_name.replace(' ', '_'))[:30]
                new_short_id = f"{date_str}_{safe_name}"
            else:
                new_short_id = f"{date_str}_{uuid4().hex[:8]}"
            db_doc = TinyMongoDocument("content_db", "content_documents", new_short_id, True)
            return ContentDataManager(db_doc, content_type, True)
        except:
            return None