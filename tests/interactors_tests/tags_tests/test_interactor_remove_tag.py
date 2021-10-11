from unittest.mock import MagicMock, patch

from pytest import fixture

from desafiolib.interactors.interactors_tags.interactor_remove_tag import \
    DeleteTagRequestModel, DeleteTagResponseModel, DeleteTagInteractor

patch_root = 'desafiolib.interactors.interactors_tags.interactor_remove_tag'


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return DeleteTagInteractor(mock_request,
                                   mock_adapter)

    return request_interactor


def test_delete_tag_request_model():
    tag_mock = MagicMock()

    request = DeleteTagRequestModel(tag_mock)

    assert request.tag_id == tag_mock


def test_remove_tag_response_model():
    tag_mock = MagicMock()

    response = DeleteTagResponseModel(tag_mock)

    assert response.tag == tag_mock


def test_remove_tag_response_model_call():
    tag_mock = MagicMock()

    result = DeleteTagResponseModel(tag_mock)()

    assert result == tag_mock


def test_remove_tag_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


def test_remove_tag_interactor_get_tag(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_tag()

    tag_mock = interactor.adapter.query().filter().first()

    assert result == tag_mock


@patch.object(DeleteTagInteractor, '_get_tag')
def test_check_tag_delete(mock_get_remove_tag,
                          interactor_factory):
    interactor = interactor_factory()

    interactor._get_tag.return_value = None

    interactor._get_tag()

    mock_get_remove_tag.assert_called_once()


@patch(f'{patch_root}.Tag')
def test_remove_tag_interactor_delete_tag(tag_db_mock,
                                          interactor_factory):
    mock_tag = MagicMock()
    interactor = interactor_factory()

    result = interactor._delete_tag(mock_tag)

    interactor.adapter.query.assert_called_once_with(tag_db_mock)

    interactor.adapter.query().filter.assert_called_once_with(
        tag_db_mock.id == mock_tag.id)

    interactor.adapter.query().filter().delete.assert_called_once()

    interactor.adapter.commit.assert_called_once()

    assert result == {
        "status": 200,
        "message": "Tag was deleted",
        "tag": mock_tag
    }


@patch.object(DeleteTagInteractor, '_check_tag_delete')
@patch.object(DeleteTagInteractor, '_delete_tag')
@patch(f'{patch_root}.DeleteTagResponseModel')
def test_remove_tag_interactor_run(mock_response,
                                   mock_delete,
                                   mock_check_del_tag,
                                   interactor_factory):
    interactor = interactor_factory()

    result = interactor.run()

    mock_check_del_tag.assert_called_once()

    mock_delete.assert_called_once_with(mock_check_del_tag())

    mock_response.assert_called_once_with(mock_delete())

    assert result == mock_response()
