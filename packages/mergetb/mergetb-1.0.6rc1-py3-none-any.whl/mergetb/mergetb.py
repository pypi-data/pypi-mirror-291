import asyncio
import nest_asyncio
nest_asyncio.apply()

from grpclib.exceptions import GRPCError, StreamTerminatedError
from grpclib.client import Channel

from mergetbapi.portal.v1 import *
from .grpc_client import MergeGRPCClient, MergeGRPCError

# initialize a default shared grpc_client for functions in this package
dflt_grpc_client = MergeGRPCClient()

async def _async_get_identities(grpc_client=dflt_grpc_client):
    return await IdentityStub(grpc_client.get_channel()).list_identities(
        ListIdentityRequest(),
        metadata=grpc_client.get_auth_metadata(),
    )

async def _async_get_users(filter=None, grpc_client=dflt_grpc_client):
    return await WorkspaceStub(grpc_client.get_channel()).get_users(
        GetUsersRequest(
            filter=filter
        ),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_get_experiments(filter=None, grpc_client=dflt_grpc_client):
    return await WorkspaceStub(grpc_client.get_channel()).get_experiments(
        GetExperimentsRequest(
            filter=filter,
        ),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_get_projects(filter=None, grpc_client=dflt_grpc_client):
    return await WorkspaceStub(grpc_client.get_channel()).get_projects(
        GetProjectsRequest(
            filter=filter,
        ),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_get_organizations(filter=None, grpc_client=dflt_grpc_client):
    return await WorkspaceStub(grpc_client.get_channel()).get_organizations(
        GetOrganizationsRequest(
            filter=filter,
        ),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_get_realizations(filter=None, grpc_client=dflt_grpc_client):
    return await RealizeStub(grpc_client.get_channel()).get_realizations(
        GetRealizationsRequest(
            filter=filter,
        ),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_get_materializations(filter=None, grpc_client=dflt_grpc_client):
    return await MaterializeStub(grpc_client.get_channel()).get_materializations_v2(
        GetMaterializationsRequestV2(
            filter=filter,
        ),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_get_xdcs(project=None, grpc_client=dflt_grpc_client):
    return await XdcStub(grpc_client.get_channel()).list_xd_cs(
        ListXdCsRequest(
            project=project,
        ),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_get_xdc_jump_hosts(grpc_client=dflt_grpc_client):
    return await XdcStub(grpc_client.get_channel()).get_xdc_jump_hosts(
        GetXdcJumpHostsRequest(),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_get_entity_type_configurations(grpc_client=dflt_grpc_client):
    return await WorkspaceStub(grpc_client.get_channel()).get_entity_type_configurations(
        GetEntityTypeConfigurationsRequest(),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_update_entity_type_configurations(types=None, patch_strategy=None, grpc_client=dflt_grpc_client):
    return await WorkspaceStub(grpc_client.get_channel()).update_entity_type_configurations(
        UpdateEntityTypeConfigurationsRequest(
            types=types,
            patch_strategy=patch_strategy,
        ),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_get_user_configurations(grpc_client=dflt_grpc_client):
    return await WorkspaceStub(grpc_client.get_channel()).get_user_configurations(
        GetUserConfigurationsRequest(),
        metadata=grpc_client.get_auth_metadata()
    )

async def _async_update_user_configurations(institutions=None, categories=None, patch_strategy=None, grpc_client=dflt_grpc_client):
    return await WorkspaceStub(grpc_client.get_channel()).update_user_configurations(
        UpdateUserConfigurationsRequest(
            institutions=institutions,
            categories=categories,
            patch_strategy=patch_strategy,
        ),
        metadata=grpc_client.get_auth_metadata()
    )

def get_identities(grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_identities, grpc_client)

def get_users(filter=None, grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_users, filter, grpc_client)

def get_experiments(filter=None, grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_experiments, filter, grpc_client)

def get_projects(filter=None, grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_projects, filter, grpc_client)

def get_organizations(filter=None, grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_organizations, filter, grpc_client)

def get_realizations(filter=None, grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_realizations, filter, grpc_client)

def get_materializations(filter=None, grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_materializations, filter, grpc_client)

def get_xdcs(project=None, grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_xdcs, project, grpc_client)

def get_xdc_jump_hosts(grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_xdc_jump_hosts, grpc_client)

def get_entity_type_configurations(grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_entity_type_configurations, grpc_client)

def update_entity_type_configurations(types=None, patch_strategy=None, grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_update_entity_type_configurations,
        types, patch_strategy, grpc_client
    )

def get_user_configurations(grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_get_user_configurations, grpc_client)

def update_user_configurations(institutions=None, categories=None, patch_strategy=None, grpc_client=dflt_grpc_client):
    return do_grpc_call(_async_update_entity_type_configurations,
        institutions, categories, patch_strategy, grpc_client
    )

# Synchronously execute an async function
def synced(fn, *args, **kwargs):
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(fn(*args, **kwargs))
    except RuntimeError as e:
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(fn(*args, **kwargs))

# execute an asynchronous MergeTB API call and handle exceptions that can happen
GRPC_CALL_TRIES=5
def do_grpc_call(fn, *args, **kwargs):
    attempt = 1
    while True:
        try:
            return synced(fn, *args, **kwargs)
        except GRPCError as grpc_error:
            raise MergeGRPCError(grpc_error)
        except StreamTerminatedError as e:
            # grpclib does not process GOAWAY frames properly
            # These tend to indicate transient problems, so we can generally
            # retry the call and it will succeed.

            attempt = attempt + 1
            if attempt > GRPC_CALL_TRIES:
                raise e

            print("  [stream_terminated: attempting try %d out of %d]" %
                (attempt, GRPC_CALL_TRIES)
            )
