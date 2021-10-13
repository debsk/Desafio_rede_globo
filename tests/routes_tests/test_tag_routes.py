from desafiolib.routes.tag_routes import \
    post_create_tag, get_read_tag, delete_tag, put_update_tag
from unittest.mock import patch, MagicMock

patch_root = 'desafiolib.routes.tag_routes'


@patch(f'{patch_root}.tag_models')
@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.CreateTagRequestModel')
@patch(f'{patch_root}.CreateTagInteractor')
def test_get_create_card(mock_create_tag_interactor,
                         mock_create_tag_request_model,
                         mock_card_alchemy_adapter,
                         mock_depends,
                         mock_tag):
    result = post_create_tag(mock_tag.Schema,
                             mock_depends(mock_card_alchemy_adapter))

    mock_create_tag_request_model.assert_called_once_with(
        mock_tag.Schema)

    mock_create_tag_interactor.assert_called_once_with(
        mock_create_tag_request_model(),
        mock_depends(mock_card_alchemy_adapter))

    mock_create_tag_interactor().run.assert_called_once()

    assert result == mock_create_tag_interactor().run()()


@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.ReadTagRequestModel')
@patch(f'{patch_root}.ReadTagInteractor')
def test_get_read_tag(mock_read_tag_interactor,
                      mock_read_tag_request_model,
                      mock_read_tag_alchemy_adapter,
                      mock_depends):
    mock_tags = MagicMock()
    result = get_read_tag(mock_tags,
                          mock_depends(mock_read_tag_alchemy_adapter))

    mock_read_tag_request_model.assert_called_once_with(mock_tags)

    mock_read_tag_interactor.assert_called_once_with(
        mock_read_tag_request_model(),
        mock_depends(mock_read_tag_alchemy_adapter))

    mock_read_tag_interactor().run.assert_called_once()

    assert result == mock_read_tag_interactor().run()()


@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.DeleteTagRequestModel')
@patch(f'{patch_root}.DeleteTagInteractor')
def test_delete_tag(mock_delete_tag_interactor,
                    mock_delete_tag_request_model,
                    mock_delete_tag_alchemy_adapter,
                    mock_depends):
    mock_tags = MagicMock()

    result = delete_tag(mock_tags,
                        mock_depends(mock_delete_tag_alchemy_adapter))

    mock_delete_tag_request_model.assert_called_once_with(mock_tags)

    mock_delete_tag_interactor.assert_called_once_with(
        mock_delete_tag_request_model(),
        mock_depends(mock_delete_tag_alchemy_adapter))

    mock_delete_tag_interactor().run.assert_called_once()

    assert result == mock_delete_tag_interactor().run()()


@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.UpdateTagRequestModel')
@patch(f'{patch_root}.UpdateTagInteractor')
def test_put_update_tag(mock_update_tag_interactor,
                        mock_update_tag_request_model,
                        mock_update_tag_alchemy_adapter,
                        mock_depends):
    mock_tags = MagicMock()
    result = put_update_tag(mock_tags,
                            mock_depends(mock_update_tag_alchemy_adapter))

    mock_update_tag_request_model.assert_called_once_with(mock_tags)

    mock_update_tag_interactor.assert_called_once_with(
        mock_update_tag_request_model(),
        mock_depends(mock_update_tag_alchemy_adapter))

    mock_update_tag_interactor().run.assert_called_once()

    assert result == mock_update_tag_interactor().run()()
