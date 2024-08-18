import moto.server as server
from moto import mock_aws


@mock_aws
def test_kinesisvideoarchivedmedia_server_is_up():
    backend = server.create_backend_app("kinesis-video-archived-media")
    test_client = backend.test_client()
    res = test_client.post("/getHLSStreamingSessionURL")
    # Just checking server is up
    assert res.status_code == 404
