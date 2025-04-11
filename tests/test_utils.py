from dndbehind.utils import required_keys_present, \
    make_response_without_resource_state


def test_required_keys_present():
    data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    required = {'key1', 'key2'}
    assert required_keys_present(required, data) is True

    required = {'key4'}
    assert required_keys_present(required, data) is False


def test_make_response_without_resource_state(app):
    with app.app_context():
        response = make_response_without_resource_state('Test message', 200)
        assert response.status_code == 200
        assert response.json['msg'] == 'Test message'
        assert response.json['status'] == 200
