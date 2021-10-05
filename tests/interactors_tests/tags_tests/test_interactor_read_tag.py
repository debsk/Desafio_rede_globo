from unittest.mock import MagicMock, patch

from pytest import fixture

from desafiolib.interactors.interactors_tags.interactor_read_tag import \
    ReadTagRequestModel, ReadTagResponseModel, ReadTagInteractor

patch_root = 'desafiolib.interactors.interactors_tags.interactor_read_tag'


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return ReadTagInteractor(mock_request,
                                 mock_adapter)

    return request_interactor


def test_read_tag_request_model():
    tag_mock = MagicMock()

    request = ReadTagRequestModel(tag_mock)

    assert request.tag_id == tag_mock


def test_read_tag_response_model():
    tag_mock = MagicMock()

    response = ReadTagResponseModel(tag_mock)

    assert response.tag == tag_mock


def test_read_tag_response_model_call():
    tag_mock = MagicMock()

    result = ReadTagResponseModel(tag_mock)()

    tag_mock.to_json.assert_called_once_with()

    assert result == tag_mock.to_json()


def test_read_tag_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


def test_read_tag_interactor_get_read_tag(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_read_tag()

    tag_mock = interactor.adapter.tag_models().filter().first()

    assert result == tag_mock


@patch.object(ReadTagInteractor, '_get_read_tag')
@patch(f'{patch_root}.ReadTagResponseModel')
def test_read_tag_interactor_run(mock_response,
                                 mock_read_tag,
                                 interactor_factory):
    interactor = interactor_factory()

    result = interactor.run()

    mock_read_tag.assert_called_once()

    mock_response.assert_called_once_with(mock_read_tag())

    assert result == mock_response()