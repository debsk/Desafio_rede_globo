from desafiolib.routes.tag_routes import \
    create_tag
from unittest.mock import patch

patch_root = 'desafiolib.routes.tag_routes'


@patch(f'{patch_root}.tag_models')
@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.CreateTagRequestModel')
@patch(f'{patch_root}.CreateTagInteractor')
def test_create_card(mock_create_tag_interactor,
                     mock_create_tag_request_model,
                     mock_card_alchemy_adapter,
                     mock_depends,
                     mock_tag):
    result = create_tag(mock_tag.Schema,
                        mock_depends(mock_card_alchemy_adapter))

    mock_create_tag_request_model.assert_called_once_with(
        mock_tag.Schema)

    mock_create_tag_interactor.assert_called_once_with(
        mock_create_tag_request_model(),
        mock_depends(mock_card_alchemy_adapter))

    mock_create_tag_interactor().run.assert_called_once()

    assert result == mock_create_tag_interactor().run()()
