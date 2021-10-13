from unittest.mock import MagicMock, patch

from pytest import fixture

from desafiolib.interactors.interactors_cards.interactor_read_card import \
    ReadCardRequestModel, ReadCardResponseModel, ReadCardInteractor

patch_root = 'desafiolib.interactors.interactors_cards.interactor_read_card'


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return ReadCardInteractor(mock_request,
                                  mock_adapter)

    return request_interactor


def test_read_card_request_model():
    card_mock = MagicMock()

    request = ReadCardRequestModel(card_mock)

    assert request.card_id == card_mock


def test_read_card_response_model():
    card_mock = MagicMock()

    response = ReadCardResponseModel(card_mock)

    assert response.card == card_mock


def test_read_card_response_model_call():
    card_mock = MagicMock()

    result = ReadCardResponseModel(card_mock)()

    assert result == card_mock


def test_read_card_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


@patch.object(ReadCardInteractor, '_get_read_card')
def test_check_user_exists(mock_get_read_card,
                           interactor_factory):
    interactor = interactor_factory()

    interactor._get_read_card.return_value = None

    interactor._get_read_card()

    mock_get_read_card.assert_called_once()


def test_read_card_interactor_get_read_card(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_read_card()

    card_mock = interactor.adapter.query().filter().first()

    assert result == card_mock


@patch.object(ReadCardInteractor, '_get_read_card')
@patch.object(ReadCardInteractor, '_check_exist_read_card')
@patch(f'{patch_root}.ReadCardResponseModel')
def test_read_card_interactor_run(mock_response,
                                  mock_check,
                                  mock_read_card,
                                  interactor_factory):
    interactor = interactor_factory()

    result = interactor.run()

    mock_read_card.assert_called_once()

    mock_check.assert_called_once_with(mock_read_card())

    mock_response.assert_called_once_with(mock_read_card())

    assert result == mock_response()
