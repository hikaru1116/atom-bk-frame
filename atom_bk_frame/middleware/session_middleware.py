from typing import Dict, List, Tuple
from atom_bk_frame.auth.entities.auth_user_entity import AuthUserEntity
from atom_bk_frame.auth.entities.session_entitiy import SessionEntity
from atom_bk_frame.auth.session_maneger import SessionManeger
from atom_bk_frame.db.db_accesors.db_accesor import DbAccesor
from atom_bk_frame.http.request import Request
from atom_bk_frame.http.response.response import Response
from atom_bk_frame.core.middleware import Middleware
from atom_bk_frame.util.class_loader_util import get_module_by_full_route
from atom_bk_frame.util.settings_util import get_member_by_settings


class SessionMiddleware(Middleware):
    """セッション管理ミドルウェア
    アプリケーションのセッション情報の取得、判別処理を行います

    Args:
        Middleware (_type_): ミドルウェア基底クラス
    """

    def request_process(self,
                        response: Response,
                        request: Request,
                        **kwargs) -> Tuple[bool, Response, Request, Dict]:

        cookie = request.cookie
        if not cookie:
            return True, response, request, kwargs

        session = request.cookie.get("session")
        if not session:
            return True, response, request, kwargs

        session_db_accesor = DbAccesor(SessionEntity)
        session_entities: List[SessionEntity] = session_db_accesor.select_by_param(param={
            "session": session[0]
        })

        if len(session_entities) <= 0:
            return True, response, request, kwargs

        session_entitiy = session_entities[0]

        if not SessionManeger.check_epired(session_entitiy.expired_at.value):
            return True, response, request, kwargs

        user_entity_module = get_module_by_full_route(get_member_by_settings("AUTH_USER_ENTITY"))
        user_db_accesor = DbAccesor(user_entity_module)
        user_entity: AuthUserEntity = user_db_accesor.select_by_id(session_entities[0].user_id.value)

        kwargs['user'] = user_entity

        return True, response, request, kwargs

    def response_process(self,
                         response: Response) -> Tuple[bool, Response]:
        return True, response
