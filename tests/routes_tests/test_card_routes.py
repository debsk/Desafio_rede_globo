from desafiolib.routes.card_routes import \
    create_card
from unittest.mock import patch

patch_root = 'desafiolib.routes.card_routes'


@patch(f'{patch_root}.Card')
@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.CreateCardRequestModel')
@patch(f'{patch_root}.CreateCardInteractor')
def test_create_card(mock_create_card_interactor,
                     mock_create_card_request_model,
                     mock_card_alchemy_adapter,
                     mock_depends,
                     mock_card):
    result = create_card(mock_card.Schema,
                         mock_depends(mock_card_alchemy_adapter))

    mock_create_card_request_model.assert_called_once_with(
        mock_card.Schema)

    mock_create_card_interactor.assert_called_once_with(
        mock_create_card_request_model(),
        mock_depends(mock_card_alchemy_adapter))

    mock_create_card_interactor().run.assert_called_once()

    assert result == mock_create_card_interactor().run()()
