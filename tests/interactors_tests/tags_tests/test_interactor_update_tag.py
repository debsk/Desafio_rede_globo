from unittest.mock import MagicMock, patch

from pytest import fixture

from desafiolib.interactors.interactors_tags.interactor_update_tag import \
    UpdateTagRequestModel, UpdateTagResponseModel, UpdateTagInteractor

patch_root = 'desafiolib.interactors.interactors_tags.interactor_update_tag'


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return UpdateTagInteractor(mock_request,
                                   mock_adapter)

    return request_interactor


def test_update_tag_request_model():
    body_mock = MagicMock()
    body_mock.return_value = {"id": MagicMock(),
                              "name": MagicMock()}

    request = UpdateTagRequestModel(body_mock)

    assert request.id == body_mock.id
    assert request.name == body_mock.name


def test_update_tag_response_model():
    tag_mock = MagicMock()

    response = UpdateTagResponseModel(tag_mock)

    assert response.tag == tag_mock


def test_update_tag_response_model_call():
    tag_mock = MagicMock()

    result = UpdateTagResponseModel(tag_mock)()

    tag_mock.to_json.assert_called_once_with()

    assert result == tag_mock.to_json()


def test_update_tag_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


def test_get_tag_update_interactor(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_tag()

    mock_tag = interactor.adapter.query().filter().first()

    assert result == mock_tag


def test_update_tag_update_interactor(interactor_factory):
    tag_mock = MagicMock()
    tag_mock.return_value = {"name": MagicMock()}
    interactor = interactor_factory()

    result = interactor._update_tag(tag_mock)

    interactor.adapter.commit.assert_called_once()

    assert tag_mock.name == interactor.request.name
    assert result == tag_mock


@patch.object(UpdateTagInteractor, '_get_tag')
@patch.object(UpdateTagInteractor, '_update_tag')
@patch(f'{patch_root}.UpdateTagResponseModel')
def test_tag_interactor_run(mock_response,
                            mock_update,
                            mock_get_tag,
                            interactor_factory):
    interactor = interactor_factory()

    result = interactor.run()

    mock_get_tag.assert_called_once()

    mock_update.assert_called_once_with(mock_get_tag())

    mock_response.assert_called_once_with(mock_get_tag())

    assert result == mock_response()
