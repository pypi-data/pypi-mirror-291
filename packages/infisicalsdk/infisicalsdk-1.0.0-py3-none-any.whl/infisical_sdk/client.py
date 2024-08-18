from typing import List, Union
import openapi_client 
from openapi_client.models.api_v1_auth_token_auth_identities_identity_id_tokens_post200_response import ApiV1AuthTokenAuthIdentitiesIdentityIdTokensPost200Response
from openapi_client.models.api_v1_auth_universal_auth_login_post_request import ApiV1AuthUniversalAuthLoginPostRequest
from openapi_client.models.api_v3_secrets_raw_get200_response import ApiV3SecretsRawGet200Response
from openapi_client.models.api_v3_secrets_raw_secret_name_patch_request import ApiV3SecretsRawSecretNamePatchRequest
from openapi_client.models.api_v3_secrets_raw_secret_name_post200_response import ApiV3SecretsRawSecretNamePost200Response
from openapi_client.models.api_v3_secrets_raw_secret_name_post_request import ApiV3SecretsRawSecretNamePostRequest

class InfisicalSDK:
    def __init__(self, host: str = "https://api.infisical.com", token: str  = None):
        self.host = host
        self.token_type = None
        self.expires_in = None

        self._api_config = openapi_client.Configuration(host=host, access_token=token)
        self._api_client = openapi_client.ApiClient(self._api_config)
        self._api_instance = openapi_client.DefaultApi(self._api_client)
        self.rest = self._api_instance

        self.auth = Auth(self)
        self.secrets = V3RawSecrets(self)

    def set_token(self, token: str):
        """
        Set the access token for future requests.
        """
        self._api_config.access_token = token

    def get_token(self):
        """
        Set the access token for future requests.
        """
        return self.token


class UniversalAuth:
    def __init__(self, client: InfisicalSDK):
        self.client = client

    def login(self, client_id: str, client_secret: str) -> ApiV1AuthTokenAuthIdentitiesIdentityIdTokensPost200Response:
        """
        Login with Universal Auth.

        Args:
            client_id (str): Your Machine Identity Client ID.
            client_secret (str): Your Machine Identity Client Secret.

        Returns:
            Dict: A dictionary containing the access token and related information.
        """

        response = self.client._api_instance.api_v1_auth_universal_auth_login_post(ApiV1AuthUniversalAuthLoginPostRequest(
            client_id = client_id,
            client_secret = client_secret
        ))

        self.client.set_token(response.access_token)

        return response
    

class AWSAuth:
    def __init__(self, client: InfisicalSDK) -> None:
        self.client = client

    def test(self):
        self.client


class Auth:
    def __init__(self, client):
        self.client = client
        self.awsAuth = AWSAuth(client)
        self.universalAuth = UniversalAuth(client)

class V3RawSecrets:
    def __init__(self, client: InfisicalSDK) -> None:
        self.client = client

    def listSecrets(self, project_id: str, environment_slug: str, secret_path: str, expand_secret_references: bool = True, recursive: bool = False, include_imports : bool = True, tag_filters: List[str] = []) -> ApiV3SecretsRawGet200Response:
        return self.client._api_instance.api_v3_secrets_raw_get(
            workspace_id=project_id, 
            environment=environment_slug, 
            secret_path=secret_path, 
            expand_secret_references=str(expand_secret_references).lower(), 
            recursive=str(recursive).lower(), 
            tag_slugs=",".join(tag_filters), 
            include_imports=str(include_imports).lower())

    def createSecretByName(self, secret_name: str, project_id: str, secret_path: str, environment_slug: str, secret_value: str = None, secret_comment: str = None, skip_multiline_encoding: bool = False, secret_reminder_repeat_days: Union[float, int] = None, secret_reminder_note: str = None) -> ApiV3SecretsRawSecretNamePost200Response:
        secret_request = ApiV3SecretsRawSecretNamePostRequest(
            workspaceId = project_id,
            environment = environment_slug,
            secretPath= secret_path,
            secretValue = secret_value,
            secretComment = secret_comment,
            tagIds = None,
            skipMultilineEncoding = skip_multiline_encoding,
            type = "shared",
            secretReminderRepeatDays = secret_reminder_repeat_days,
            secretReminderNote = secret_reminder_note
        )

        return self.client._api_instance.api_v3_secrets_raw_secret_name_post(secret_name, secret_request)
         

    def updateSecretByName(self, current_secret_name: str, project_id: str, secret_path: str, environment_slug: str, secret_value: str = None, secret_comment: str = None, skip_multiline_encoding: bool = False, secret_reminder_repeat_days: Union[float, int] = None, secret_reminder_note: str = None, new_secret_name: str = None) -> ApiV3SecretsRawSecretNamePost200Response:
        secret_request = ApiV3SecretsRawSecretNamePatchRequest(
            workspaceId = project_id,
            environment = environment_slug,
            secretPath= secret_path,
            secretValue = secret_value,
            secretComment = secret_comment,
            new_secret_name=new_secret_name,
            tagIds = None,
            skipMultilineEncoding = skip_multiline_encoding,
            type = "shared",
            secretReminderRepeatDays = secret_reminder_repeat_days,
            secretReminderNote = secret_reminder_note
        )

        return self.client._api_instance.api_v3_secrets_raw_secret_name_patch(current_secret_name, secret_request) 

    def deleteSecretByName(self):
        pass 

    def getSecretByName(self):
        pass 
