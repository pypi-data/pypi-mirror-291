import uuid

from globus_cli.login_manager import LoginManager
from globus_cli.parsing import command, endpoint_id_arg
from globus_cli.termio import display


@command("deactivate", deprecated=True, hidden=True)
@endpoint_id_arg
@LoginManager.requires_login("transfer")
def endpoint_deactivate(login_manager: LoginManager, *, endpoint_id: uuid.UUID) -> None:
    """
    Remove the credential previously assigned to an endpoint via
    'globus endpoint activate' or any other form of endpoint activation
    """
    transfer_client = login_manager.get_transfer_client()
    res = transfer_client.endpoint_deactivate(endpoint_id)
    display(res, text_mode=display.RAW, response_key="message")
