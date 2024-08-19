import pymongo as pmon
import coopmongo.mongo_utils as utils
from typing import List, Dict, Generic, TypeVar, Callable, Iterable, Tuple
from cooptools.protocols import UniqueIdentifier, IdentifiableProtocol
from cooptools.dataStoreProtocol import DataStoreProtocol


class MongoCollectionHandler(DataStoreProtocol):

    def __init__(self,
                 db_name: str,
                 collection_name: str,
                 client: pmon.MongoClient = None,
                 uri: str = None,
                 facade_handler: utils.DocumentFacadeHandler = None,
                 dataclass_model: type = None,
                 sample_doc_gen: Callable[[...], utils.MongoStorableProtocol] = None
                 ):
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = client if client is not None else utils.get_client(uri)
        self.facade_handler = facade_handler
        self.dataclass_model = dataclass_model
        self.sample_doc_gen = sample_doc_gen
        self.tracked_time = {}

    @property
    def Collection(self):
        return utils.get_collection(db_name=self.db_name,
                                    collection_name=self.collection_name,
                                    client=self.client)

    @property
    def CollectionSize(self):
        return self.Collection.count_documents({})

    @property
    def CollectionSizeEstimated(self):
        return self.Collection.estimated_document_count({})

    def add(self,
            items: Iterable[utils.MongoStorableProtocol]) -> Dict[UniqueIdentifier, utils.MongoStorableProtocol]:
        ret = utils.insert_documents(collection=self.Collection,
                                     jsonable_objs=items,
                                     facade_handler=self.facade_handler)
        return ret

    def get(self,
            ids: Iterable[UniqueIdentifier] = None,
            query: Dict = None,
            limit: int = None) -> Dict[UniqueIdentifier, utils.MongoStorableProtocol]:
        retrieved = utils.get_documents(self.Collection,
                                        facade_handler=self.facade_handler,
                                        dataclass_model=self.dataclass_model,
                                        query=query,
                                        ids=ids,
                                        limit=limit)
        return retrieved

    def find(self,
             id: UniqueIdentifier) -> utils.MongoStorableProtocol:
        retrieved = utils.get_document(collection=self.Collection,
                                       facade_handler=self.facade_handler,
                                       id=id)
        return retrieved

    def update(self,
               items: Iterable[utils.MongoStorableProtocol] = None,
               ) -> Dict[UniqueIdentifier, utils.MongoStorableProtocol]:
        updated = {}
        for item in items:
            updated[item.id()] = utils.update_document(collection=self.Collection,
                                                       id=id,
                                                       update_obj=item,
                                                       facade_handler=self.facade_handler)
        return updated

    def remove(self,
               items: Iterable[IdentifiableProtocol] = None,
               cursor_range: Tuple[int, int] = None,
               ids: Iterable[UniqueIdentifier] = None) -> Dict[UniqueIdentifier, IdentifiableProtocol]:
        deleted = {}
        for item in items:
            utils.delete_document(
                self.Collection,
                id=item.id(),
                facade_handler=self.facade_handler)
            deleted[item.id()] = item
        return deleted
