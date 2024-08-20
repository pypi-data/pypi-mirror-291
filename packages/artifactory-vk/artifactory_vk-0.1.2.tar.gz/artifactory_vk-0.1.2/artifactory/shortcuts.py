import io
from .client import Client


def upload_resource(
    client: Client,
    content: str | bytes,
    *,
    file_name: str | None = None,
    checksum_md5: str | None = None,
    context: dict | None = None,
    description: str | None = None,
    tags: list[str] | None = None,
    soft_ttl_s: int | None = None,
    hard_ttl_s: int | None = None,
):
    content_b = None
    match content:
        case str():
            content_b = content.encode('utf-8')
        case bytes():
            content_b = content
        case _:
            raise RuntimeError(f'content argument should be either str or bytes')
    assert content_b is not None
    
    resource_id = client.upload_resource(
        io.BytesIO(content_b),
        file_name=file_name,
        checksum_md5=checksum_md5,
        context=context,
        description=description,
        tags=tags,
        soft_ttl_s=soft_ttl_s,
        hard_ttl_s=hard_ttl_s,
    )
    return resource_id


def download_resource(
    client: Client,
    resource_id: str,    
) -> bytes:
    stream = client.download_resource(resource_id)
    return b''.join(stream)
