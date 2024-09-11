from .add_event_request_body import AddEventRequestBody
from .add_tags_by_cv_user_request_body import AddTagsByCVUserRequestBody
from .add_tags_by_dialogue_user_request_body import AddTagsByDialogueUserRequestBody
from .add_tags_by_link_user_request_body import AddTagsByLinkUserRequestBody
from .add_tags_by_text_user_request_body import AddTagsByTextUserRequestBody
from .add_user_request_body import AddUserRequestBody
from .add_user_to_event_request_body import AddUserToEventRequestBody
from .get_is_admin_request_body import GetIsAdminRequestBody
from .get_ranking_user_request_body import GetRankingUserRequestBody
from .get_tags_by_user_request_body import GetTagsByUserRequestBody
from .get_users_by_event_request_body import GetUsersByEventRequestBody

__all__ = [
    "AddTagsByCVUserRequestBody",
    "AddTagsByTextUserRequestBody",
    "AddTagsByDialogueUserRequestBody",
    "AddTagsByLinkUserRequestBody",
    "AddUserRequestBody",
    "GetIsAdminRequestBody",
    "GetRankingUserRequestBody",
    "GetUsersByEventRequestBody",
    "GetTagsByUserRequestBody",
    "AddEventRequestBody",
    "AddUserToEventRequestBody",
]
