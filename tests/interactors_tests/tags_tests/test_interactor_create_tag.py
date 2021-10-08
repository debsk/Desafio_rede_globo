from unittest.mock import MagicMock, patch

from pytest import fixture

from desafiolib.interactors.interactors_tags.interactor_create_tag import \
    CreateTagRequestModel, CreateTagInteractor, CreateTagResponseModel


path_root = 'desafiolib.interactors.interactors_tags.interactor_create_tag'


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return CreateTagInteractor(mock_request,
                                   mock_adapter)
    return request_interactor


def test_create_card_request_model():
    body_mock = MagicMock()
    body_mock.return_value = {"name": MagicMock()}

    request = CreateTagRequestModel(body_mock)

    assert request.name == body_mock.name


def test_create_tag_response_model():
    tag_mock = MagicMock()

    response = CreateTagResponseModel(tag_mock)

    assert response.tag == tag_mock


def test_create_tag_response_model_call():
    tag_mock = MagicMock()

    result = CreateTagResponseModel(tag_mock)()

    tag_mock.to_json.assert_called_once_with()

    assert result == tag_mock.to_json()


def test_create_card_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter

def test_read_tag_interactor_get_tag(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_tag()

    tag_mock = interactor.adapter.query().filter().first()

    assert result == tag_mock


@patch.object(CreateTagInteractor, '_get_tag')
def test_check_tag_exists(mock_get_tag,
                           interactor_factory):
    interactor = interactor_factory()

    interactor._get_tag.return_value = None

    interactor._get_tag()

    mock_get_tag.assert_called_once()


@patch(f'{path_root}.Tag')
def test_create_tag_interactor_create_tag(tag_function_mock,
                                          interactor_factory):

    interactor = interactor_factory()

    result = interactor._create_tag()

    tag_mock = tag_function_mock(name=interactor.request.name)

    interactor.adapter.add.assert_called_once_with(tag_mock)
    interactor.adapter.commitassert_called_once()
    interactor.adapter.refreshassert_called_once_with(tag_mock)

    assert result == tag_mock


@patch.object(CreateTagInteractor, '_create_tag')
@patch.object(CreateTagInteractor, '_check_exist_tag')
@patch(f'{path_root}.CreateTagResponseModel')
def test_post_create_user_interactor_run(mock_response,
                                         mock_check,
                                         mock_create_tag,
                                         interactor_factory):

    interactor = interactor_factory()

    result = interactor.run()

    mock_check.assert_called_once()

    mock_create_tag.assert_called_once()

    mock_response.assert_called_once_with(mock_create_tag())

    assert result == mock_response()
