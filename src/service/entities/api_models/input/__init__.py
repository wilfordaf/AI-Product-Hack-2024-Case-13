from .add_tags_by_cv_user_request_body import AddTagsByCVUserRequestBody
from .add_tags_by_dialogue_user_request_body import AddTagsByDialogueUserRequestBody
from .add_tags_by_link_user_request_body import AddTagsByLinkUserRequestBody
from .add_tags_by_text_user_request_body import AddTagsByTextUserRequestBody
from .add_user_request_body import AddUserRequestBody
from .get_is_admin_request_body import GetIsAdminRequestBody
from .get_ranking_user_request_body import GetRankingUserRequestBody

__all__ = [
    "AddTagsByCVUserRequestBody",
    "AddTagsByTextUserRequestBody",
    "AddTagsByDialogueUserRequestBody",
    "AddTagsByLinkUserRequestBody",
    "AddUserRequestBody",
    "GetIsAdminRequestBody",
    "GetRankingUserRequestBody",
]
