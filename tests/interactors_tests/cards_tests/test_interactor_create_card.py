from unittest.mock import MagicMock, patch

from pytest import fixture

from desafiolib.interactors.interactors_cards.interactor_create_card import \
    CreateCardRequestModel, CreateCardResponseModel, CreateCardInteractor

patch_root = 'desafiolib.interactors.interactors_cards.interactor_create_card'


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return CreateCardInteractor(mock_request,
                                    mock_adapter)
    return request_interactor


def test_create_card_request_model():
    body_mock = MagicMock()
    body_mock.return_value = {"text": MagicMock(),
                              "tags": MagicMock()}
    request = CreateCardRequestModel(body_mock)

    assert request.text == body_mock.text
    assert request.tags == body_mock.tags


def test_create_card_response_model():
    card_mock = MagicMock()

    response = CreateCardResponseModel(card_mock)

    assert response.card == card_mock


def test_create_card_response_model_call():
    card_mock = MagicMock()

    result = CreateCardResponseModel(card_mock)()

    card_mock.to_json.assert_called_once_with()

    assert result == card_mock.to_json()


def test_create_card_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


def test_read_card_interactor_get_card(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_card()

    card_mock = interactor.adapter.query().filter().first()

    assert result == card_mock


@patch.object(CreateCardInteractor, '_get_card')
def test_check_card_exists(mock_get_card,
                           interactor_factory):
    interactor = interactor_factory()

    interactor._get_card.return_value = None

    interactor._get_card()

    mock_get_card.assert_called_once()


@patch(f'{patch_root}.json')
@patch(f'{patch_root}.Card')
def test_create_card_interactor_create_card(mock_function_card,
                                            json_mock,
                                            interactor_factory):
    interactor = interactor_factory()

    result = interactor._create_card()
    mock_card = mock_function_card(text=interactor.request.text,
                                   tags=json_mock.dumps(
                                       interactor.request.tags))

    interactor.adapter.add.assert_called_once_with(mock_card)
    interactor.adapter.commit.assert_called_once()
    interactor.adapter.refresh.assert_called_once_with(mock_card)

    assert result == mock_card


@patch.object(CreateCardInteractor, '_create_card')
@patch.object(CreateCardInteractor, '_check_exist_card')
@patch(f'{patch_root}.CreateCardResponseModel')
def test_post_create_user_interactor_run(mock_response,
                                         mock_check,
                                         mock_create_card,
                                         interactor_factory):

    interactor = interactor_factory()

    result = interactor.run()

    mock_check.assert_called_once()

    mock_create_card.assert_called_once()

    mock_response.assert_called_once_with(mock_create_card())

    assert result == mock_response()
