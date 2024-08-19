
import json
import time

import pymongo.collection

import pymongo as pmon
from typing import Dict, Protocol, List, Iterable
from pydantic import BaseModel, Field
import uuid
from fastapi.encoders import jsonable_encoder
import coopmongo.errors as errors
import logging
from cooptools.decor import timer
from cooptools.protocols import IdentifiableProtocol, JsonableDictProtocol, UniqueIdentifier

logger = logging.getLogger(__name__)

class DocumentFacade(BaseModel):
    obj_data: Dict
    id: str = Field(default_factory=uuid.uuid4, alias='_id')


class DocumentFacadeHandler:

    def __init__(self,
                 obj_type: type,
                 facade_type: type = DocumentFacade,
                 data_field_name: str = 'obj_data'):
        self.facade_type = facade_type
        self.obj_type = obj_type
        self.data_field_name = data_field_name

    def as_BaseModel(self, obj: MongoStorableProtocol) -> BaseModel:
        return self.facade_type(
            id=obj.id,
            obj_data=jsonable_encoder(obj.to_dict())
        )

    def obj_from_doc(self, doc):
        obj_data = doc[self.data_field_name]
        return self.obj_type(**obj_data)

    def resolve_facade_query(self, query: Dict = None):
        if query is not None:
            query = {f"{self.data_field_name}.{k}": v for k, v in query.items()}
        else:
            query = {}

        return query

@timer(logger=logger, log_level=logging.DEBUG)
def _apply_facade(jsonable_objs: Iterable[MongoStorableProtocol],
                  facade_handler: DocumentFacadeHandler = None):
    ready_objs = []
    # tic = time.perf_counter()
    for jsonable_obj in jsonable_objs:
        # try to convert the object using the facade (if exists)
        if facade_handler is not None:
            model = facade_handler.as_BaseModel(jsonable_obj)
            jsonable_obj = jsonable_encoder(model.dict(by_alias=True))
        else:
            jsonable_obj = jsonable_obj.to_jsonable_dict()
        ready_objs.append(jsonable_obj)
    # toc = time.perf_counter()
    # logger.debug(f"Time to apply facade to documents: {toc - tic} sec")
    return ready_objs


@timer(logger=logger, log_level=logging.DEBUG)
def _remove_facade(docs: List[Dict],
                   facade_handler: DocumentFacadeHandler = None):
    # tic = time.perf_counter()

    if facade_handler is not None:
        ret = [facade_handler.obj_from_doc(x) for x in docs]
    else:
        ret = docs

    # toc = time.perf_counter()
    # logger.debug(f"Time to remove facade from documents: {toc - tic} sec")
    return ret


@timer(logger=logger, log_level=logging.DEBUG)
def _convert_to_dataclass(docs: List[Dict],
                          dataclass_model: type) -> List[MongoStorableProtocol]:
    return [dataclass_model(**{k: v for k, v in args.items() if k != '_id'}) for args in docs]

def ready_objects(
        jsonable_objs: Iterable[str | Dict | MongoStorableProtocol]
):
    ready_objs = []
    for obj in jsonable_objs:
        if issubclass(type(obj), MongoStorableProtocol):
            ready_objs.append(obj.to_jsonable_dict())
        elif type(obj) == dict:
            ready_objs.append(obj)
        elif type(obj) == str:
            ready_objs.append(resolve_storable_str(obj))
        else:
            raise TypeError(f"object of type {type(obj)} cannot be stored")

    return ready_objs


@timer(logger=logger, log_level=logging.DEBUG)



@timer(logger=logger, log_level=logging.INFO)
def insert_documents(collection: pmon.collection.Collection,
                     jsonable_objs: Iterable[str | Dict | MongoStorableProtocol],
                     facade_handler: DocumentFacadeHandler = None):
    try:
        # handle facade conversion of the documents
        ready_objs = _apply_facade(jsonable_objs, facade_handler=facade_handler)

        for obj in ready_objs:
            if 'id' in obj.keys():
                obj['_id'] = obj['id']
            if 'obj_id' in obj.keys():
                obj['_id'] = obj['obj_id']

        # insert the document(s)
        tic = time.perf_counter()
        if len(jsonable_objs) == 1:
            new_item = collection.insert_one(ready_objs[0])
            created_item = collection.find_one(
                {"_id": new_item.inserted_id}
            )
            created_items = [created_item]
        else:
            new_items = collection.insert_many(ready_objs)
            created_items = list(collection.find(
                {"_id": {'$in': new_items.inserted_ids}}
            ))
        toc = time.perf_counter()
        logger.debug(f"Time to insert docs: {toc - tic} sec")
        logger.info(f"Documents created: [{len(created_items)}]")

        # convert back to object from facade (if exists)
        created_items = _remove_facade(created_items, facade_handler=facade_handler)

        # return
        return created_items

    except pymongo.errors.DuplicateKeyError as e:
        raise errors.DuplicateException() from e
    except Exception as e:
        raise e


@timer(logger=logger, log_level=logging.INFO)
def get_documents(collection: pmon.collection.Collection,
                  facade_handler: DocumentFacadeHandler = None,
                  dataclass_model: type = None,
                  query: Dict = None,
                  ids: List[str] = None,
                  limit: int = 100) -> Dict[UniqueIdentifier, MongoStorableProtocol]:
    # resolve ids
    if ids is not None:
        id_query = {'id': {'$in': ids}}
        query = {**query, **id_query} if query is not None else id_query

    # resolve query
    query = query if facade_handler is None else facade_handler.resolve_facade_query(query)

    # collect items
    tic = time.perf_counter()
    if limit is not None:
        items = list(collection.find(query, limit=limit))
    else:
        items = list(collection.find(query))
    toc = time.perf_counter()
    logger.debug(f"Time to retrieve documents: {toc - tic} sec")

    # remove facade
    if facade_handler is not None:
        items = _remove_facade(items, facade_handler=facade_handler)
    # convert dataclass
    elif dataclass_model is not None:
        items = _convert_to_dataclass(items,
                                      dataclass_model=dataclass_model)

    return {x.id(): x for x in items}


@timer(logger=logger, log_level=logging.INFO)
def get_document(collection: pmon.collection.Collection,
                 id: str,
                 facade_handler: DocumentFacadeHandler = None):
    if facade_handler is None:
        field_name = "_id"
    else:
        field_name = f"{facade_handler.data_field_name}.id"

    item = collection.find_one({field_name: id})
    logger.info(f"Document retrieved: {item}")

    if item is None:
        raise errors.NotFoundException()

    if facade_handler is not None:
        item = facade_handler.obj_from_doc(item)

    return item


@timer(logger=logger, log_level=logging.INFO)
def update_document(collection: pmon.collection.Collection,
                    id: str = None,
                    update_dict: Dict = None,
                    update_obj: MongoStorableProtocol = None,
                    facade_handler: DocumentFacadeHandler = None):
    if update_dict is None and update_obj is None:
        raise ValueError(f"At least one of values or object must be provided")

    if update_dict is not None and id is None:
        raise ValueError(f"Id must be provided if update_dict is being used")

    if update_obj is not None:
        update_dict = jsonable_encoder(update_obj.to_dict())
        id = update_obj.id

    # determine id field to be queried
    if facade_handler is None:
        field_name = "_id"
    else:
        field_name = f"{facade_handler.data_field_name}.id"

    # resolve update dict
    update_dict = update_dict if facade_handler is None else facade_handler.resolve_facade_query(update_dict)

    # update
    update_result = collection.update_one({field_name: id}, {"$set": update_dict})

    # raise if nothing was updated
    if update_result.modified_count == 0:
        raise errors.NotFoundException()

    # retrieve updated doc
    updated_item = get_document(collection=collection, id=id, facade_handler=facade_handler)
    logger.info(f"Document updated: {updated_item}")

    return updated_item

@timer(logger=logger, log_level=logging.INFO)
def delete_document(collection: pmon.collection.Collection,
                    id: str,
                    facade_handler: DocumentFacadeHandler = None):
    if facade_handler is None:
        field_name = "_id"
    else:
        field_name = f"{facade_handler.data_field_name}.id"

    delete_result = collection.delete_one({field_name: id})
    if delete_result.deleted_count == 0:
        raise errors.NotFoundException()

    logger.info(f"Document deleted: {id}")

    return True
