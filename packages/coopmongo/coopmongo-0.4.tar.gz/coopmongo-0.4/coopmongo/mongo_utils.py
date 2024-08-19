import pymongo as pmon
from typing import Dict, Protocol, List, Iterable
import uuid
import coopmongo.errors as errors
import logging
from cooptools.decor import timer
from cooptools.protocols import IdentifiableProtocol, JsonableDictProtocol, UniqueIdentifier
from cooptools.dataStore import dataStoreProtocol as dsp


logger = logging.getLogger(__name__)

ORIGINAL_ID_KEY_TXT = 'original_id_key'
DEFAULT_ID_KEY = '_id'

def str_format_lst(
    ids: Iterable[str]
):
    f"\n[\n{',\n\t'.join(str(x) for x in ids)}\n]"


@timer(logger=logger, log_level=logging.DEBUG)
def get_client(uri: str):
    return pmon.MongoClient(uri)


@timer(logger=logger, log_level=logging.DEBUG)
def get_database(db_name: str, client: pmon.MongoClient = None, uri: str = None):
    if client is None:
        client = get_client(uri)

    return client[db_name]


@timer(logger=logger, log_level=logging.DEBUG)
def get_collection(db_name: str, collection_name: str, client: pmon.MongoClient = None, uri: str = None):
    db = get_database(db_name, client=client, uri=uri)
    return db[collection_name]

@timer(logger=logger, log_level=logging.INFO)
def collection_length(collection: pmon.collection.Collection,
                      query: Dict = None):
    filter = {} if query is None else {query, {}}
    return collection.count_documents(filter=filter)

@timer(logger=logger, log_level=logging.INFO)
def create_index(db_name: str, collection_name: str, index_name: pmon.collection._IndexKeyHint,
                 client: pmon.MongoClient = None, uri: str = None):
    collection = get_collection(db_name=db_name, collection_name=collection_name, uri=uri, client=client)
    collection.create_index(index_name)

@timer(logger=logger, log_level=logging.DEBUG)
def get_documents(
        collection: pmon.collection.Collection,
        query: Dict = None,
        ids: Iterable[str] = None,
        limit: int = None,
        id_key: str = DEFAULT_ID_KEY) -> Dict[UniqueIdentifier, Dict]:
    # resolve ids
    if ids is not None:
        id_query = {DEFAULT_ID_KEY: {'$in': ids}}
        query = {**query, **id_query} if query is not None else id_query

    # collect items
    if limit is not None:
        items = list(collection.find(query, limit=limit))
    else:
        items = list(collection.find(query))

    # replace ids
    ret = {x[DEFAULT_ID_KEY]: x for x in items}
    for k, v in ret.items():
        v[v[ORIGINAL_ID_KEY_TXT]] = v[DEFAULT_ID_KEY]
        del v[DEFAULT_ID_KEY]
        del v[ORIGINAL_ID_KEY_TXT]

    logger.info(f"Document(s) retrieved: {str_format_lst(ret.keys())}")
    return ret

@timer(logger=logger, log_level=logging.DEBUG)
def check_for_keys(
        collection: pmon.collection.Collection,
        ids: Iterable[str]
) -> Dict[str, bool]:
    results = get_documents(
        collection=collection,
        ids=ids
    )

    return {
        id: id in results.keys() for id in ids
    }

@timer(logger=logger, log_level=logging.DEBUG)
def insert_documents(
        collection: pmon.collection.Collection,
        objs: Iterable[dict],
        id_key: str = DEFAULT_ID_KEY
) -> Dict[IdentifiableProtocol, Dict]:
    objs = list(objs)
    for obj in objs:
        if DEFAULT_ID_KEY in obj.keys() and DEFAULT_ID_KEY != id_key:
            raise ValueError(f"invalid id_key: {id_key} when \'{DEFAULT_ID_KEY}\' already in dict")
        obj[ORIGINAL_ID_KEY_TXT] = id_key
        obj[DEFAULT_ID_KEY] = str(obj[id_key])
        del obj[id_key]

    if len(objs) == 1:
        inserted_result = collection.insert_one(objs[0])
        created_ids = [inserted_result.inserted_id]
    else:
        inserted_result = collection.insert_many(objs)
        created_ids = inserted_result.inserted_ids

    inserted = get_documents(
        collection=collection,
        ids=created_ids,
        id_key=id_key
    )

    logger.info(f"Document(s) inserted: {[x for x in inserted.keys()]}")
    return inserted


@timer(logger=logger, log_level=logging.INFO)
def update_document(collection: pmon.collection.Collection,
                    id: str,
                    updates: Dict[str, Dict]):
    # update
    update_result = collection.update_one({DEFAULT_ID_KEY: id}, {"$set": updates})


    # raise if nothing was updated
    if update_result.modified_count == 0:
        raise errors.NotFoundException()

    # retrieve updated doc
    updated_item = get_documents(
        collection=collection,
        ids=[id],
    )
    logger.info(f"Document updated: {updated_item}")
    return updated_item


@timer(logger=logger, log_level=logging.INFO)
def delete_documents(collection: pmon.collection.Collection,
                     ids: Iterable[str]):

    key_check = check_for_keys(
        collection=collection,
        ids=ids
    )

    if any([v is False for k, v in key_check.items()]):
        raise dsp.IdsNotInStoreException(ids=[k for k, v in key_check.items() if v is False])

    delete_result = collection.delete_many({DEFAULT_ID_KEY: {'$in': ids}})

    if delete_result.deleted_count != len(list(ids)):
        key_check = check_for_keys(
            collection=collection,
            ids=ids
        )
        raise Exception(f"Well well well... for some reason, not all the records were deleted. Keys {str_format_lst([k for k, v in key_check.items() if v])} remain")

    logger.info(f"Document(s) deleted: {str_format_lst(ids)}")

    return True

def clear_collection(collection: pmon.collection.Collection):
    delete_result = collection.delete_many({})
    return True

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
        return args.connection_string()


    def test_collection():
        return get_collection(
            db_name='test_db',
            collection_name='test_collection',
            client=get_client(uri=test_mongo_connection_args()))


    def test_insert_001():
        c = test_collection()
        inserted = insert_documents(
            collection=c,
            objs=[{
                'id': str(uuid.uuid4()),
                'name': 'Tj',
                'occupation': "engineer"
            }],
            id_key='id'
        )
        pprint(inserted)


    test_insert_001()
