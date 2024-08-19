import uuid

import pymongo
import pymongo as pmon
import coopmongo.mongo_utils as utils
from typing import List, Dict, Generic, TypeVar, Callable, Iterable, Tuple, Any, Protocol
from cooptools.protocols import IdentifiableProtocol, JsonableDictProtocol, UniqueIdentifier
from cooptools.dataStore.dataStoreProtocol import DataStoreProtocol, SUPPORTED_DICT_IDENTIFIERS
from cooptools.dataStore.dbConnectionURI import MongoDBConnectionArgs
import json
from cooptools.dataStore import dataStoreProtocol as dsp

class MongoStorableProtocol(IdentifiableProtocol, JsonableDictProtocol):
    pass


SupportedMongoStorable = MongoStorableProtocol | dict | str


def _resolve_dict(dic: Dict):
    id_key = next(x for x in SUPPORTED_DICT_IDENTIFIERS if x in dic.keys())
    if id_key is None:
        raise ValueError(
            f"The objects dict does not conform to supported keys: [{','.join(SUPPORTED_DICT_IDENTIFIERS)}]")
    return (dic, id_key)

def ready_objects(
        objs: Iterable[SupportedMongoStorable]
) -> Dict[UniqueIdentifier, Tuple[Dict, str]]:
    ready_objs = {}
    for obj in objs:
        if issubclass(type(obj), MongoStorableProtocol):
            ready_objs[obj.get_id] = (obj.to_jsonable_dict(), 'id')
        elif type(obj) == dict:
            dic, id_key = _resolve_dict(obj)
            ready_objs[dic[id_key]] = (dic, id_key)
        elif type(obj) == str:
            try:
                content=json.loads(obj)
                dic, id_key = _resolve_dict(content)
                ready_objs[dic[id_key]] = (dic, id_key)
            except:
                obj={
                    'id': uuid.uuid4(),
                    'content': obj
                }
                dic, id_key = _resolve_dict(obj)
                ready_objs[dic[id_key]] = (dic, id_key)
        else:
            raise TypeError(f"object of type {type(obj)} cannot be stored")

    return ready_objs

class ObjectDictFacadeProtocol(Protocol):
    def obj_to_dict_translator(self, x: Any) -> Dict:
        pass

    def dict_to_obj_translator(self, x: Dict) -> Any:
        pass

class MongoCollectionDataStore(DataStoreProtocol):

    def __init__(self,
                 db_name: str,
                 collection_name: str,
                 connection_args: MongoDBConnectionArgs,
                 facade: ObjectDictFacadeProtocol = None
                 # obj_id_key: str
                 ):
        self.db_name = db_name
        self.collection_name = collection_name
        self.connection_args = connection_args
        self._facade = facade
        self.tracked_time = {}


    def _apply_facade(self,
                      items: Iterable[SupportedMongoStorable]):
        if self._facade is not None:
            items = [self._facade.obj_to_dict_translator(x) for x in items]

        return items

    def _remove_facade(self, items: Iterable[Dict] | Dict[UniqueIdentifier, Dict]):
        if self._facade is None:
            return items

        if type(items) == dict:
            items = {k: self._facade.dict_to_obj_translator(v) for k,v in items.items()}
        else:
            items = [self._facade.dict_to_obj_translator(x) for x in items]

        return items

    @property
    def Client(self) -> pymongo.MongoClient:
        return utils.get_client(uri=self.connection_args.connection_string())

    @property
    def Collection(self):
        return utils.get_collection(db_name=self.db_name,
                                    collection_name=self.collection_name,
                                    client=self.Client)

    @property
    def CollectionSize(self):
        return self.Collection.count_documents({})

    @property
    def CollectionSizeEstimated(self):
        return self.Collection.estimated_document_count({})

    def add(self,
            items: Iterable[SupportedMongoStorable]) -> Dict[UniqueIdentifier, SupportedMongoStorable]:

        items = self._apply_facade(items)

        ready = ready_objects(items)

        organized = {}
        for id, val in ready.items():
            data, id_key = val
            organized.setdefault(id_key, []).append(data)

        ret = {}
        for id_key, sub_items in organized.items():
            sub = utils.insert_documents(
                collection=self.Collection,
                objs=sub_items,
                id_key=id_key
            )
            ret.update(sub)

        return self

    def get(self,
            cursor_range: Tuple[int, int] = None,
            ids: Iterable[UniqueIdentifier] = None,
            limit: int = None,
            query: Dict = None) -> Dict[UniqueIdentifier, SupportedMongoStorable]:
        retrieved = utils.get_documents(self.Collection,
                                        query=query,
                                        ids=ids,
                                        limit=limit)

        retrieved = self._remove_facade(retrieved)

        return retrieved

    # def update(self,
    #            items: Iterable[SupportedMongoStorable] = None,
    #            ) -> Dict[UniqueIdentifier, Dict]:
    #     updated = {}
    #     for item in items:
    #         updated[item.id()] = utils.update_document(collection=self.Collection,
    #                                                    id=id,
    #                                                    updates=
    #                                                    )
    #     return updated

    def remove(self,
               items: Iterable[dsp.StorableData] = None,
               cursor_range: Tuple[int, int] = None,
               ids: Iterable[UniqueIdentifier] = None) -> Dict[UniqueIdentifier, dsp.StorableData]:
        items = self._apply_facade(items)

        if items is not None:
            ids = [dsp.get_identifier(item for item in items)]

        ret = utils.delete_documents(
            self.Collection,
            ids=ids
        )

        return self

    def clear(self):
        utils.clear_collection(self.Collection)
        return self

if __name__ == "__main__":
    from cooptools.dataStore import dbConnectionURI as dburi
    from cooptools.cnxn_info import Creds
    from pprint import pprint

    def test_mongo_connection_args():
        args = dburi.MongoDBConnectionArgs(
            db_type=dburi.DataBaseType.MONGODB,
            db_connector=dburi.DataBaseConnector.SRV,
            server_name='cluster0.bfcjjod.mongodb.net',
            creds=Creds(
                user="tylertjburns",
                pw="Chick3nCoopDissonanc3!"
            )
        )
        return args

    def test_mongo_collection_data_store():
        mcds = MongoCollectionDataStore(
            db_name='test_db',
            collection_name='test_collection2',
            connection_args=test_mongo_connection_args()
        )
        return mcds

    def test_mcds_add():
        mcds = test_mongo_collection_data_store()
        ids=[str(uuid.uuid4()) for ii in range(10)]
        added = mcds.add(
            items=[{
                'id': x,
                'name': 'tj',
                'occupation': 'engineer'
            } for x in ids]
        ).get(ids)

        pprint(added)

    def test_mcds_remove():
        mcds = test_mongo_collection_data_store()
        options = list(mcds.get().values())
        ret = mcds.remove(ids=[options[0]['id']]).get()
        pprint(ret)

    def test_mcds_clear():
        mcds = test_mongo_collection_data_store()
        ret = mcds.clear()
        pprint(ret)


    test_mcds_clear()
    test_mcds_add()
    test_mcds_remove()
