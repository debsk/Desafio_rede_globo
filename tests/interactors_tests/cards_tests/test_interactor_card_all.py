from unittest.mock import MagicMock, patch

from pytest import fixture

from desafiolib.interactors.interactors_cards.interactor_card_all import \
    AllCardRequestModel, AllCardResponseModel, AllCardInteractor

patch_root = 'desafiolib.interactors.interactors_cards.interactor_card_all'


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return AllCardInteractor(mock_request,
                                 mock_adapter)

    return request_interactor


def test_all_card_request_model():
    tag_mock = MagicMock()

    request = AllCardRequestModel(tag_mock)

    assert request.tag_id == tag_mock


def test_all_card_response_model():
    cards_mock = MagicMock()

    cards_mock.return_value = [{'card': MagicMock()}]

    response = AllCardResponseModel(cards_mock)

    assert response.cards == cards_mock


def test_all_card_response_model_call():
    cards_mock = MagicMock()

    result = AllCardResponseModel(cards_mock)()

    assert result == cards_mock


def test_all_card_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


@patch(f'{patch_root}.json')
@patch(f'{patch_root}.Card')
def test_all_card_interactor_get_all_card(
        card_mock,
        json_mock,
        interactor_factory):
    interactor = interactor_factory()

    interactor._get_all_card()

    interactor.adapter.query.assert_called_once_with(card_mock)

    interactor.adapter.query().all.assert_called_once()


@patch.object(AllCardInteractor, '_get_all_card')
@patch(f'{patch_root}.AllCardResponseModel')
def test_all_card_interactor_run(mock_response,
                                 mock_all_card,
                                 interactor_factory):
    interactor = interactor_factory()

    result = interactor.run()

    mock_all_card.assert_called_once()

    mock_response.assert_called_once_with(mock_all_card())

    assert result == mock_response()
