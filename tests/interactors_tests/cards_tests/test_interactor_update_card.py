from unittest.mock import MagicMock, patch

from pytest import fixture

from desafiolib.interactors.interactors_cards.interactor_update_card import \
    UpdateCardRequestModel, UpdateCardResponseModel, UpdateCardInteractor

patch_root = 'desafiolib.interactors.interactors_cards.interactor_update_card'


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return UpdateCardInteractor(mock_request,
                                    mock_adapter)

    return request_interactor


def test_update_card_request_model():
    body_mock = MagicMock()
    body_mock.return_value = {"id": MagicMock(),
                              "text": MagicMock(),
                              "tags": MagicMock()}

    request = UpdateCardRequestModel(body_mock)

    assert request.id == body_mock.id
    assert request.text == body_mock.text
    assert request.tags == body_mock.tags


def test_update_card_response_model():
    card_mock = MagicMock()

    response = UpdateCardResponseModel(card_mock)

    assert response.card == card_mock


def test_update_card_response_model_call():
    card_mock = MagicMock()

    result = UpdateCardResponseModel(card_mock)()

    card_mock.to_json.assert_called_once_with()

    assert result == card_mock.to_json()


def test_update_card_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


def test_get_card_update_card_interactor(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_card()

    mock_card = interactor.adapter.query().filter().first()

    assert result == mock_card


@patch(f'{patch_root}.json')
@patch(f'{patch_root}.Card')
def test_update_card_interactor(mock_function_card,
                                json_mock,
                                interactor_factory):
    interactor = interactor_factory()

    result = interactor._update_card()

    mock_card = mock_function_card(text=interactor.request.text,
                                   tags=json_mock.dumps(
                                       interactor.request.tags))

    interactor.adapter.commit.assert_called_once()

    assert result == mock_card


@patch.object(UpdateCardInteractor, '_get_card')
@patch.object(UpdateCardInteractor, '_update_card')
@patch(f'{patch_root}.UpdateCardResponseModel')
def test_post_create_user_interactor_run(mock_response,
                                         mock_update,
                                         mock_get_card,
                                         interactor_factory):

    interactor = interactor_factory()

    result = interactor.run()

    mock_get_card.assert_called_once()

    mock_update.assert_called_once_with()

    mock_response.assert_called_once_with(mock_get_card())

    assert result == mock_response()
