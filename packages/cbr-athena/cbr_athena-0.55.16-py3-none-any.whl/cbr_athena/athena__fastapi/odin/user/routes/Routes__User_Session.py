from fastapi                            import Security, Request, Depends
from fastapi.security                   import APIKeyHeader
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

from cbr_athena.odin.Odin__CBR__User_Session import Odin__CBR__User_Session
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Objects import obj_data

ROUTE_PATH__USER_SESSION        = 'user-session'
EXPECTED_ROUTES__USER_SESSION   = ['/session-details']

api_key_header   = APIKeyHeader(name="Authorization", auto_error=False)

class CBR__Session_Auth(Type_Safe):
    odin_cbr_user_session : Odin__CBR__User_Session

    def session_data(self, request: Request, session_id: str = Security(api_key_header)):
        if session_id is None:
            if 'CBR_TOKEN' in request.cookies:
                session_id = request.cookies.get('CBR_TOKEN')
                if '|' in session_id:                                   # for the cases where the admin is impersonating a session ID
                    session_id = session_id.split('|')[1]
        session_data = self.odin_cbr_user_session.user_session_data(session_id)
        return session_data

    def session_id_to_session_data(self,  request: Request, session_id: str = Security(api_key_header)):
        return self.session_data(request, session_id)

    def admins_only(self,request: Request, session_id: str = Security(api_key_header)):
        session_data = self.session_data(request, session_id)
        if session_data.get('data').get('user_access').get('is_admin'):
            return session_data
        else:
            return { 'error': 'only admins can access this route'}





cbr_session_auth = CBR__Session_Auth()

class Routes__User_Session(Fast_API_Routes):

    tag : str = ROUTE_PATH__USER_SESSION

    def session_data(self, session_data: str = Depends(cbr_session_auth.session_id_to_session_data)):
        return session_data

    def only_admins(self, session_data: str = Depends(cbr_session_auth.admins_only)):
        from cbr_athena.llms.storage.CBR__Chats_Storage__S3 import CBR__Chats_Storage__S3
        chats_storage_s3 = CBR__Chats_Storage__S3()
        result = {'s3_bucket': chats_storage_s3.s3_db_base.s3_bucket()}
        return {'result': result}


    def chat_debug(self):
        from cbr_athena.config.CBR__Config__Athena import cbr_config_athena
        return {'aws_disabled': cbr_config_athena.aws_disabled()}

    def setup_routes(self):
        self.add_route_get(self.session_data)
        self.add_route_get(self.only_admins )
        self.add_route_get(self.chat_debug)