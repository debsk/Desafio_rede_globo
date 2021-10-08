from desafiolib.routes.card_routes import \
    post_create_card, get_read_card, delete_card, put_update_card, \
    get_all_cards

from unittest.mock import patch, MagicMock

patch_root = 'desafiolib.routes.card_routes'


@patch(f'{patch_root}.Card')
@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.CreateCardRequestModel')
@patch(f'{patch_root}.CreateCardInteractor')
def test_post_create_card(mock_create_card_interactor,
                          mock_create_card_request_model,
                          mock_card_alchemy_adapter,
                          mock_depends,
                          mock_card):
    result = post_create_card(mock_card.Schema,
                              mock_depends(mock_card_alchemy_adapter))

    mock_create_card_request_model.assert_called_once_with(
        mock_card.Schema)

    mock_create_card_interactor.assert_called_once_with(
        mock_create_card_request_model(),
        mock_depends(mock_card_alchemy_adapter))

    mock_create_card_interactor().run.assert_called_once()

    assert result == mock_create_card_interactor().run()()


@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.ReadCardRequestModel')
@patch(f'{patch_root}.ReadCardInteractor')
def test_get_read_card(mock_read_card_interactor,
                       mock_read_card_request_model,
                       mock_card_alchemy_adapter,
                       mock_depends):
    mock_card = MagicMock()
    result = get_read_card(mock_card,
                           mock_depends(mock_card_alchemy_adapter))

    mock_read_card_request_model.assert_called_once_with(mock_card)

    mock_read_card_interactor.assert_called_once_with(
        mock_read_card_request_model(),
        mock_depends(mock_card_alchemy_adapter))

    mock_read_card_interactor().run.assert_called_once()

    assert result == mock_read_card_interactor().run()()


@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.DeleteCardRequestModel')
@patch(f'{patch_root}.DeleteCardInteractor')
def test_delete_card(mock_delete_card_interactor,
                     mock_delete_card_request_model,
                     mock_card_alchemy_adapter,
                     mock_depends):
    mock_card = MagicMock()
    result = delete_card(mock_card,
                         mock_depends(mock_card_alchemy_adapter))

    mock_delete_card_request_model.assert_called_once_with(mock_card)

    mock_delete_card_interactor.assert_called_once_with(
        mock_delete_card_request_model(),
        mock_depends(mock_card_alchemy_adapter))

    mock_delete_card_interactor().run.assert_called_once()

    assert result == mock_delete_card_interactor().run()()


@patch(f'{patch_root}.Card')
@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.UpdateCardRequestModel')
@patch(f'{patch_root}.UpdateCardInteractor')
def test_put_update_card(mock_update_card_interactor,
                         mock_update_card_request_model,
                         mock_card_alchemy_adapter,
                         mock_depends,
                         mock_card):
    result = put_update_card(mock_card.Schema,
                             mock_depends(mock_card_alchemy_adapter))

    mock_update_card_request_model.assert_called_once_with(
        mock_card.Schema)

    mock_update_card_interactor.assert_called_once_with(
        mock_update_card_request_model(),
        mock_depends(mock_card_alchemy_adapter))

    mock_update_card_interactor().run.assert_called_once()

    assert result == mock_update_card_interactor().run()()


@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.AllCardRequestModel')
@patch(f'{patch_root}.AllCardInteractor')
def test_all_card(mock_all_card_interactor,
                  mock_all_card_request_model,
                  mock_card_alchemy_adapter,
                  mock_depends):
    mock_card = MagicMock()
    result = get_all_cards(mock_card,
                           mock_depends(mock_card_alchemy_adapter))

    mock_all_card_request_model.assert_called_once_with(mock_card)

    mock_all_card_interactor.assert_called_once_with(
        mock_all_card_request_model(),
        mock_depends(mock_card_alchemy_adapter))

    mock_all_card_interactor().run.assert_called_once()

    assert result == mock_all_card_interactor().run()()
