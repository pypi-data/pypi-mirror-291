import io
import os
import time
from pathlib import Path
from typing import IO

import pytest

import artifactory as art
import artifactory.units as units
import artifactory.models.requests as req
import artifactory.models.resources as res
from artifactory.shortcuts import upload_resource, download_resource

import utils


TEST_SERVER_HOST=os.getenv('TEST_SERVER_HOST')
TEST_SERVER_PORT=os.getenv('TEST_SERVER_PORT')
TEST_FILES=Path(__file__).parent / 'files'
assert utils.all_not_None(TEST_SERVER_HOST, TEST_SERVER_PORT, TEST_FILES)


@pytest.fixture(name='client')
def init_art_client():
    config = art.ClientConfig(
        artifactory_endpoint = f'http://{TEST_SERVER_HOST}:{TEST_SERVER_PORT}',
        upload_chunk_size = 5 * units.B,
        upload_retries = 0,
    )
    return art.Client(config)


def test_resource_upload_simple(
    client: art.Client,
):
    r_id = upload_resource(
        client,
        'Hello, World!',
        file_name='hello_world.txt',
        hard_ttl_s=3600,
    )
    assert r_id is not None
    
    meta = client.get_resource_meta(r_id)
    assert meta.resource_id == r_id
    assert meta.file_name == 'hello_world.txt'
    assert meta.byte_size == len(b'Hello, World!')
    assert meta.hard_ttl_s == 3600

    assert meta.checksum_md5 is None
    assert meta.context is None
    assert meta.has_ownership is True
    assert meta.draft_creation_ts is not None
    assert meta.draft_creation_ts <= int(time.time())
    assert meta.creation_ts is not None
    assert meta.creation_ts <= int(time.time())
    assert meta.last_access_ts is not None
    assert meta.last_access_ts <= int(time.time())
    assert meta.soft_ttl_s is None
    assert meta.is_removed is False

    content_it = client.download_resource(r_id)
    assert b''.join(c for c in content_it) == b'Hello, World!'

    content = download_resource(client, r_id)
    assert content == b'Hello, World!'

    r_id_copy = client.copy_resource(r_id, hard_ttl_s=1)
    assert r_id_copy is not None
    assert r_id_copy != r_id

    content_copy = download_resource(client, r_id_copy)
    assert content_copy == b'Hello, World!'


def test_resource_upload_through_api(
    client: art.Client,
):
    request = req.V1ResourcesDraftsPOSTRequest(
        body=res.NewResourceDraftMeta(),
    )
    response = client.api.v1_resources_drafts_POST(request)
    resource_id = response.resource_id
    upload_url = response.upload_url
    
    content = b'Hello, World!'
    reader = io.BytesIO(content)
    byte_size = len(content)
    client.api.tus_upload(
        reader,
        byte_size,
        upload_url=upload_url,
        chunk_size=5*units.B,
    )
    
    meta = client.get_resource_meta(resource_id)
    assert meta.file_name is None
    assert meta.byte_size == byte_size

    assert download_resource(client, resource_id) == content
