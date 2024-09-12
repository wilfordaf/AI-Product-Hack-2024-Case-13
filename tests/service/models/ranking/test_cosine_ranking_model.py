from src.service.models.ranking.cosine_ranking_model import CosineRankingModel


def test_correct_get_info():
    c = CosineRankingModel([])
    assert c.info == "CosineRankingModel v0.0.1_beta"
