import importlib
import pickle
from pathlib import Path
from typing import Dict, List, Tuple

import faiss
import numpy as np
import numpy.typing as npt

from src.service.models.ranking.interfaces import IRankingModel
from src.service.utils.exceptions import ServiceError
from src.service.utils.logging import ConsoleLogger


class CosineRankingModel(IRankingModel):
    _DATA_PATH = Path(__file__).parent.resolve() / "data"

    def __init__(self, possible_tags: List[str]):
        try:
            self._version = getattr(importlib.import_module(".".join(self.__module__.split(".")[:-1])), "version")
        except AttributeError as e:
            raise ServiceError("Module does not have version.py or it is not in __init__.py") from e
        except ValueError as e:
            raise ServiceError(f"Incorrect path to {self.__module__}") from e

        self._possible_tags = possible_tags
        self._possible_tags.sort()

        self._tg2id: Dict[str, int] = {}
        self._id2tg: Dict[int, str] = {}

        self._storage: List[npt.NDArray[np.float32]] = []
        self._index = faiss.IndexFlatIP(len(self._possible_tags))

        self._logger = ConsoleLogger()

    @property
    def info(self) -> str:
        return f"CosineRankingModel v{self._version}"

    def add_user(self, telegram_id: str, tags: List[str]) -> None:
        if telegram_id in self._tg2id:
            self._logger.debug(f"User {telegram_id} was already added to the ranking model")

        user_vector = self._vectorize(tags, normalize=True)

        self._index.add(user_vector)
        self._storage.append(user_vector)

        self._id2tg[len(self._id2tg)] = telegram_id
        self._tg2id[telegram_id] = len(self._tg2id)

        self._logger.debug(f"User {telegram_id} was added to the ranking model with vector {user_vector}")

    def load_model(self) -> None:
        folder = self._DATA_PATH.as_posix()

        self._index = faiss.read_index(f"{folder}/index.index")
        self._id2tg = pickle.load(open(f"{folder}/id2tg.pickle", "rb"))
        self._tg2id = pickle.load(open(f"{folder}/tg2id.pickle", "rb"))
        self._storage = pickle.load(open(f"{folder}/storage.pickle", "rb"))

    def save_model(self) -> None:
        folder = self._DATA_PATH.as_posix()

        faiss.write_index(self._index, f"{folder}/index.index")
        pickle.dump(self._id2tg, open(f"{folder}/id2tg.pickle", "wb"))
        pickle.dump(self._tg2id, open(f"{folder}/tg2id.pickle", "wb"))
        pickle.dump(self._storage, open(f"{folder}/storage.pickle", "wb"))

    def perform_ranking(self, caller_telegram_id: str, event_user_ids, n: int) -> List[Tuple[str, List[str]]]:
        if caller_telegram_id not in self._tg2id:
            raise ServiceError(f"User {caller_telegram_id} was not found in the ranking model")
        query = self._storage[self._tg2id.get(caller_telegram_id, 0)]
        event_user_ids_set = set(event_user_ids)

        _, ids = self._index.search(query.reshape(1, -1), n)
        caller_id = self._tg2id.get(caller_telegram_id)
        response = []
        for id in ids[0]:
            tg = self._id2tg.get(id, "")
            if id == caller_id:
                continue
            if tg not in event_user_ids_set:
                continue
            tags = self._get_matched_tags(query, self._storage[id])
            response.append((tg, tags))

        return response

    def _get_matched_tags(self, left: npt.NDArray[np.float32], right: npt.NDArray[np.float32]) -> List[str]:
        matched = []
        for tag, l, r in zip(self._possible_tags, left.astype("bool"), right.astype("bool")):
            if l and r:
                matched.append(tag)

        return matched

    def _vectorize(self, tags: List[str], normalize: bool = True) -> npt.NDArray[np.float32]:
        vector = np.zeros(len(self._possible_tags), dtype=np.uint8)

        for idx, tag in enumerate(self._possible_tags):
            if tag in tags:
                vector[idx] = 1.0

        return self._normalize(vector) if normalize else vector  # type: ignore

    @staticmethod
    def _normalize(vector: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
        return vector / np.linalg.norm(vector)
