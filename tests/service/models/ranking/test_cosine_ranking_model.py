from src.service.models.ranking.cosine_ranking_model import CosineRankingModel


def test_correct_get_info():
    c = CosineRankingModel([])
    assert c.info == "CosineRankingModel v0.0.1_beta"

def test_correct_vectorize():
    import numpy as np

    c = CosineRankingModel(["tag1", "tag2", "tag3"])

    vector = c._vectorize(["tag1", "tag2", "tag3"])
    assert vector == np.array([1.0, 1.0, 1.0]).astype(np.float32)

    vector = c._vectorize(["tag1", "tag3"])
    assert vector == np.array([1.0, 0.0, 1.0]).astype(np.float32)

def test_correct_add_user():
    import numpy as np
    
    c = CosineRankingModel(["tag1", "tag2", "tag3"])

    c.add_user("tg1", ["tag1"])
    c.add_user("tg2", ["tag2"])
    c.add_user("tg3", ["tag3"])
    
    assert c._id2tg == {0: "tg1", 1: "tg2", 2: "tg3"}
    assert c._tg2id == {"tg1": 0, "tg2": 1, "tg3": 2}

    assert c._storage == [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0])]

    assert c._index.ntotal == 3


def test_correct_get_matched_tags():
    import numpy as np

    c = CosineRankingModel(["tag1", "tag2", "tag3"])

    vector = c._vectorize(["tag1", "tag2", "tag3"])
    assert c._get_matched_tags(vector, vector) == ["tag1", "tag2", "tag3"]

def test_correct_perform_ranking():
    import numpy as np

    c = CosineRankingModel(["tag1", "tag2", "tag3"])

    c.add_user("tg1", ["tag1"])
    c.add_user("tg2", ["tag2"])
    c.add_user("tg3", ["tag3"])

    assert set([("tg2", ["tag2"]), ("tg3", ["tag3"])]) == set(c.perform_ranking("tg1", ["tg1", "tg2", "tg3"], 3))







