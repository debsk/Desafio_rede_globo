from unittest.mock import MagicMock, patch

from pytest import fixture

from desafiolib.interactors.interactors_cards.interactor_remove_card import \
    DeleteCardRequestModel, DeleteCardResponseModel, DeleteCardInteractor

patch_root = 'desafiolib.interactors.interactors_cards.interactor_remove_card'


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return DeleteCardInteractor(mock_request,
                                    mock_adapter)

    return request_interactor


def test_delete_card_request_model():
    card_mock = MagicMock()

    request = DeleteCardRequestModel(card_mock)

    assert request.card_id == card_mock


def test_remove_card_response_model():
    card_mock = MagicMock()

    response = DeleteCardResponseModel(card_mock)

    assert response.card == card_mock


def test_remove_card_response_model_call():
    card_mock = MagicMock()

    result = DeleteCardResponseModel(card_mock)()

    assert result == card_mock


def test_remove_card_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


def test_remove_card_interactor_get_card(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_card()

    card_mock = interactor.adapter.query().filter().first()

    assert result == card_mock


@patch.object(DeleteCardInteractor, '_get_card')
def test_check_card_delete(mock_get_remove_card,
                           interactor_factory):
    interactor = interactor_factory()

    interactor._get_card.return_value = None

    interactor._get_card()

    mock_get_remove_card.assert_called_once()


@patch(f'{patch_root}.Card')
def test_remove_card_interactor_delete_card(card_db_mock,
                                            interactor_factory):
    mock_card = MagicMock()
    interactor = interactor_factory()

    result = interactor._delete_card(mock_card)

    interactor.adapter.query.assert_called_once_with(card_db_mock)

    interactor.adapter.query().filter.assert_called_once_with(
        card_db_mock.id == mock_card.id)

    interactor.adapter.query().filter().delete.assert_called_once()

    interactor.adapter.commit.assert_called_once()

    assert result == {
        "status": 200,
        "message": "Card was deleted",
        "card": mock_card
    }


@patch.object(DeleteCardInteractor, '_check_card_delete')
@patch.object(DeleteCardInteractor, '_delete_card')
@patch(f'{patch_root}.DeleteCardResponseModel')
def test_remove_card_interactor_run(mock_response,
                                    mock_delete,
                                    mock_check_del_card,
                                    interactor_factory):
    interactor = interactor_factory()

    result = interactor.run()

    mock_check_del_card.assert_called_once()

    mock_delete.assert_called_once_with(mock_check_del_card())

    mock_response.assert_called_once_with(mock_delete())

    assert result == mock_response()
