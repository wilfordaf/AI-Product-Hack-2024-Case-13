import importlib
from pathlib import Path
import numpy as np
import faiss
import numpy.typing as npt
from typing import List, Tuple
import pickle
from src.service.models.ranking.interfaces import IRankingModel
from src.service.utils.exceptions import ServiceError
from src.service.utils.logging import ConsoleLogger


class CosineRankingModel(IRankingModel):
    @staticmethod
    def data_path() -> str:
        return Path(__file__).parent.resolve().joinpath("data")
        

    def __init__(self, possible_tags: List[str]):
        try:
            self._version = getattr(importlib.import_module(".".join(self.__module__.split(".")[:-1])), "version")
        except AttributeError as e:
            raise ServiceError("Module does not have version.py or it is not in __init__.py") from e
        except ValueError as e:
            raise ServiceError(f"Incorrect path to {self.__module__}") from e

        self._possible_tags = possible_tags
        self._possible_tags.sort()

        self._tg2id = {}
        self._id2tg = {}

        self._storage = []
        self._index = faiss.IndexFlatIP(len(self._possible_tags))

        self._logger = ConsoleLogger()

    @property
    def info(self) -> str:
        return f"CosineRankingModel v{self._version}"
    
    @staticmethod
    def __normalize(vector: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
        return  vector / np.linalg.norm(vector)
    
    def __vectorize(self, tags: List[str], normalize: bool = True) -> npt.NDArray[np.float32]:
        vector = np.zeros(len(self._possible_tags), dtype=np.uint8)

        for idx, tag in enumerate(self._possible_tags):
            if tag in tags:
                vector[idx] = 1.
            
        if normalize:
            return self.__normalize(vector)
        return vector

    def add_user(self, telegram_id: str, tags: List[str]) -> None:
        if telegram_id in self._tg2id:
            self._logger.log(f"User {telegram_id} was already added to the ranking model")
        user_vector = self.__vectorize(tags, normalize=True)
        
        self._index.add(user_vector)
        self._storage.append(user_vector)
        
        self._id2tg[len(self._id2tg)] = telegram_id
        self._tg2id[telegram_id] = len(self._tg2id)

        self._logger.log(f"User {telegram_id} was added to the ranking model with vector {user_vector}")


    def load_model(self) -> None:
        folder = self.data_path()

        self._index = faiss.read_index(f"{folder}/index.index")
        self._id2tg = pickle.load(open(f"{folder}/id2tg.pickle", "rb"))
        self._tg2id = pickle.load(open(f"{folder}/tg2id.pickle", "rb"))
        self._storage = pickle.load(open(f"{folder}/storage.pickle", "rb"))
    
    def save_model(self) -> None:
        folder = self.data_path()

        faiss.write_index(self._index, f"{folder}/index.index")
        pickle.dump(self._id2tg, open(f"{folder}/id2tg.pickle", "wb"))
        pickle.dump(self._tg2id, open(f"{folder}/tg2id.pickle", "wb"))
        pickle.dump(self._storage, open(f"{folder}/storage.pickle", "wb"))
    
    def __get_matched_tags(self, left: npt.NDArray[np.float32], right: npt.NDArray[np.float32]) -> List[str]:
        matched = []
        for tag, l, r in zip(self._possible_tags, left.astype("bool"), right.astype("bool")):
            if l and r: matched.append(tag)
        return matched

    def perform_ranking(self, caller_telegram_id: str, n: int) -> List[Tuple[str, List[str]]]:
        if caller_telegram_id not in self._tg2id:
            raise ValueError(f"User {caller_telegram_id} was not found in the ranking model")
        
        query = self._storage[self._tg2id.get(caller_telegram_id)]

        _, ids = self._index.search(query.reshape(1, -1), n)
        caller_id = self._tg2id.get(caller_telegram_id)
        response = []
        for id in ids[0]:
            tg = self._id2tg.get(id)
            if id == caller_id: continue
            tags = self.__get_matched_tags(query, self._storage[id])
            response.append((tg, tags))

        return response
            

