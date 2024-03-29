from atom_bk_frame.auth.controllers.queries.sign_in_query_enum import SignInQueryEnum
from atom_bk_frame.auth.encrypt_maneger import EncryptManeger
from atom_bk_frame.auth.entities.auth_user_entity import AuthUserEntity
from atom_bk_frame.auth.session_maneger import SessionManeger
from atom_bk_frame.controller.controller import Controller
from atom_bk_frame.db.db_accesors.select_db_accesor import SelectDbAccesor
from atom_bk_frame.http.request import Request
from atom_bk_frame.http.response.http_error_response import Response401, Response404
from atom_bk_frame.http.response.response import Response
from atom_bk_frame.util.class_loader_util import get_module_by_full_route
from atom_bk_frame.util.settings_util import get_member_by_settings


class SignInController(Controller):
    """ユーザ認証コントローラ

    Args:
        Controller (_type_): コントローラ基底クラス
    """

    def post(self, request: Request, **kwargs) -> Response:
        body = request.json
        if body.get("identifier") is None or body.get("password") is None:
            return Response404()

        identifier = body.get("identifier")
        password = EncryptManeger.get_hash(body.get("password"))

        user_entity_module = get_module_by_full_route(get_member_by_settings("AUTH_USER_ENTITY"))
        select_db_accesor = SelectDbAccesor(user_entity_module)

        entities = select_db_accesor.select(self._get_query(), param={
            "user_name": identifier,
            "email": identifier,
            "password": password
        })

        if len(entities) <= 0:
            return Response401()

        user_entity: AuthUserEntity = entities[0]
        session_maneger = SessionManeger()
        session_code = session_maneger.generete_session(user_entity.user_id.value)

        response = Response(status="200", body=session_code)
        response.set_cookie(session_maneger.generate_set_cookie_syntax(session_code))

        return response

    def _get_query(self) -> str:
        db_type: str = get_member_by_settings("DB_TYPE")

        return SignInQueryEnum.get_value(db_type.upper())
