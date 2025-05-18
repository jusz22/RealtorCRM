import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from unittest.mock import call as mock_call

from pydantic import UUID4

from app.application.interfaces.services.listing_service import ListingService


class MockListingPhoto:
    def __init__(self, id, url):
        self.id = id
        self.url = url


class MockListingIn:
    def __init__(self, title, description):
        self.title = title
        self.description = description


class MockListingDB:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description


class MockSortOptions:
    def __init__(self, sort_func_to_return=None):
        self._sort_func_to_return = sort_func_to_return
        self.get_sort_func_mock = MagicMock(return_value=self._sort_func_to_return)

    def get_sort_func(self):
        return self.get_sort_func_mock()


class MockFilterDTO:
    def __init__(self, field, value, operator_to_return):
        self.field = field
        self.value = value
        self._operator_to_return = operator_to_return
        self.get_operator_mock = MagicMock(return_value=operator_to_return)

    def get_operator(self):
        return self.get_operator_mock()


MockListingModel = MagicMock(name="MockListingModel")


class TestListingService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_repository = AsyncMock()
        self.listing_service = ListingService(repository=self.mock_repository)
        self.test_listing_id = UUID4("123e4567-e89b-12d3-a456-426614174000")

    async def test_save_photos_calls_repository(self):
        mock_photos = [MockListingPhoto(id=1, url="test.jpg")]
        await self.listing_service.save_photos(photos=mock_photos)
        self.mock_repository.save_photos.assert_called_once_with(photos=mock_photos)

    async def test_save_photos_returns_repository_result(self):
        mock_photos = [MockListingPhoto(id=1, url="test.jpg")]
        expected_result = "photos_saved_confirmation"
        self.mock_repository.save_photos.return_value = expected_result
        result = await self.listing_service.save_photos(photos=mock_photos)
        self.assertEqual(result, expected_result)

    async def test_save_photos_with_empty_list(self):
        await self.listing_service.save_photos(photos=[])
        self.mock_repository.save_photos.assert_called_once_with(photos=[])

    async def test_save_photos_repository_raises_exception(self):
        mock_photos = [MockListingPhoto(id=1, url="test.jpg")]
        self.mock_repository.save_photos.side_effect = Exception("DB Save Photo Error")
        with self.assertRaisesRegex(Exception, "DB Save Photo Error"):
            await self.listing_service.save_photos(photos=mock_photos)

    async def test_save_photos_multiple_photos(self):
        mock_photos = [
            MockListingPhoto(id=1, url="test1.jpg"),
            MockListingPhoto(id=2, url="test2.jpg"),
        ]
        await self.listing_service.save_photos(photos=mock_photos)
        self.mock_repository.save_photos.assert_called_once_with(photos=mock_photos)

    async def test_save_listing_calls_repository(self):
        mock_listings_in = [MockListingIn(title="Test", description="Desc")]
        await self.listing_service.save_listing(listings=mock_listings_in)
        self.mock_repository.save_listing.assert_called_once_with(
            listings=mock_listings_in
        )

    async def test_save_listing_returns_repository_result(self):
        mock_listings_in = [MockListingIn(title="Test", description="Desc")]
        expected_result = [
            MockListingDB(id=self.test_listing_id, title="Test", description="Desc")
        ]
        self.mock_repository.save_listing.return_value = expected_result
        result = await self.listing_service.save_listing(listings=mock_listings_in)
        self.assertEqual(result, expected_result)

    async def test_save_listing_with_empty_iterable(self):
        await self.listing_service.save_listing(listings=[])
        self.mock_repository.save_listing.assert_called_once_with(listings=[])

    async def test_save_listing_repository_raises_exception(self):
        mock_listings_in = [MockListingIn(title="Test", description="Desc")]
        self.mock_repository.save_listing.side_effect = Exception(
            "DB Save Listing Error"
        )
        with self.assertRaisesRegex(Exception, "DB Save Listing Error"):
            await self.listing_service.save_listing(listings=mock_listings_in)

    async def test_save_listing_multiple_listings(self):
        mock_listings_in = [
            MockListingIn(title="Test1", description="Desc1"),
            MockListingIn(title="Test2", description="Desc2"),
        ]
        await self.listing_service.save_listing(listings=mock_listings_in)
        self.mock_repository.save_listing.assert_called_once_with(
            listings=mock_listings_in
        )

    async def test_get_single_listing_calls_repository(self):
        await self.listing_service.get_single_listing(listing_id=self.test_listing_id)
        self.mock_repository.get_single_listing.assert_called_once_with(
            listing_id=self.test_listing_id
        )

    async def test_get_single_listing_returns_repository_result_found(self):
        expected_listing = MockListingDB(
            id=self.test_listing_id, title="Found", description="Yes"
        )
        self.mock_repository.get_single_listing.return_value = expected_listing
        result = await self.listing_service.get_single_listing(
            listing_id=self.test_listing_id
        )
        self.assertEqual(result, expected_listing)

    async def test_get_single_listing_returns_repository_result_not_found(self):
        self.mock_repository.get_single_listing.return_value = None
        result = await self.listing_service.get_single_listing(
            listing_id=self.test_listing_id
        )
        self.assertIsNone(result)

    async def test_get_single_listing_repository_raises_exception(self):
        self.mock_repository.get_single_listing.side_effect = Exception(
            "DB Get Single Error"
        )
        with self.assertRaisesRegex(Exception, "DB Get Single Error"):
            await self.listing_service.get_single_listing(
                listing_id=self.test_listing_id
            )

    async def test_remove_listing_calls_repository(self):
        await self.listing_service.remove_listing(listing_id=self.test_listing_id)
        self.mock_repository.delete_listing.assert_called_once_with(
            listing_id=self.test_listing_id
        )

    async def test_remove_listing_returns_repository_result(self):
        expected_result = "delete_confirmation"
        self.mock_repository.delete_listing.return_value = expected_result
        result = await self.listing_service.remove_listing(
            listing_id=self.test_listing_id
        )
        self.assertEqual(result, expected_result)

    async def test_remove_listing_repository_raises_exception(self):
        self.mock_repository.delete_listing.side_effect = Exception("DB Delete Error")
        with self.assertRaisesRegex(Exception, "DB Delete Error"):
            await self.listing_service.remove_listing(listing_id=self.test_listing_id)

    async def test_remove_listing_with_different_id_type(self):
        str_uuid = "abcdef01-2345-6789-abcd-ef0123456789"
        await self.listing_service.remove_listing(listing_id=str_uuid)
        self.mock_repository.delete_listing.assert_called_once_with(listing_id=str_uuid)

    @patch(
        "app.application.interfaces.services.listing_service.Listing",
        new=MockListingModel,
    )
    @patch("app.application.interfaces.services.listing_service.select")
    async def test_get_listings_calls_select_with_listing_model(
        self, mock_sqlalchemy_select
    ):
        mock_sqlalchemy_select.return_value = MagicMock()
        mock_sort_options = MockSortOptions()
        await self.listing_service.get_listings(
            sort_options=mock_sort_options, filter=None
        )
        mock_sqlalchemy_select.assert_called_once_with(MockListingModel)

    @patch(
        "app.application.interfaces.services.listing_service.Listing",
        new=MockListingModel,
    )
    @patch("app.application.interfaces.services.listing_service.select")
    async def test_get_listings_no_filter_no_sort_calls_repo(
        self, mock_sqlalchemy_select
    ):
        mock_query = MagicMock()
        mock_sqlalchemy_select.return_value = mock_query
        mock_sort_options = MockSortOptions(sort_func_to_return=None)
        await self.listing_service.get_listings(
            sort_options=mock_sort_options, filter=None
        )
        mock_query.where.assert_not_called()
        mock_query.order_by.assert_not_called()
        self.mock_repository.get_listings.assert_called_once_with(query=mock_query)

    @patch(
        "app.application.interfaces.services.listing_service.Listing",
        new=MockListingModel,
    )
    @patch("app.application.interfaces.services.listing_service.select")
    @patch("app.application.interfaces.services.listing_service.getattr")
    async def test_get_listings_filter_like_getattr_and_calls(
        self, mock_getattr, mock_sqlalchemy_select
    ):
        mock_query = MagicMock()
        mock_filtered_query = MagicMock()
        mock_sqlalchemy_select.return_value = mock_query
        mock_query.where.return_value = mock_filtered_query

        mock_filter_column = MagicMock(name="MockFilterColumn")
        mock_filter_expression_method = MagicMock(name="MockLikeExpressionMethod")

        mock_getattr.side_effect = [mock_filter_column, mock_filter_expression_method]

        mock_sort_options = MockSortOptions()
        mock_filter_dto = MockFilterDTO(
            field="title", value="test", operator_to_return="like"
        )

        await self.listing_service.get_listings(
            sort_options=mock_sort_options, filter=mock_filter_dto
        )

        expected_getattr_calls = [
            mock_call(MockListingModel, "title"),
            mock_call(mock_filter_column, "like"),
        ]
        mock_getattr.assert_has_calls(expected_getattr_calls, any_order=False)
        mock_filter_dto.get_operator_mock.assert_called_once()

        mock_query.where.assert_called_once()
        mock_filter_expression_method.assert_called_once_with("%test%")
        self.mock_repository.get_listings.assert_called_once_with(
            query=mock_filtered_query
        )

    @patch(
        "app.application.interfaces.services.listing_service.Listing",
        new=MockListingModel,
    )
    @patch("app.application.interfaces.services.listing_service.select")
    @patch("app.application.interfaces.services.listing_service.getattr")
    async def test_get_listings_filter_other_operator_getattr_and_calls(
        self, mock_getattr, mock_sqlalchemy_select
    ):
        mock_query = MagicMock()
        mock_filtered_query = MagicMock()
        mock_sqlalchemy_select.return_value = mock_query
        mock_query.where.return_value = mock_filtered_query

        mock_filter_column = MagicMock(name="MockFilterColumn")
        mock_operator_method = MagicMock(name="MockOperatorMethod")

        mock_filter_dto = MockFilterDTO(
            field="price", value=1000, operator_to_return="__eq__"
        )

        mock_getattr.side_effect = [mock_filter_column, mock_operator_method]

        mock_sort_options = MockSortOptions()

        await self.listing_service.get_listings(
            sort_options=mock_sort_options, filter=mock_filter_dto
        )

        expected_getattr_calls = [
            mock_call(MockListingModel, "price"),
            mock_call(mock_filter_column, "__eq__"),
        ]
        mock_getattr.assert_has_calls(expected_getattr_calls, any_order=False)
        mock_filter_dto.get_operator_mock.assert_called_once()

        mock_query.where.assert_called_once()
        mock_operator_method.assert_called_once_with(1000)
        self.mock_repository.get_listings.assert_called_once_with(
            query=mock_filtered_query
        )

    @patch("app.application.interfaces.services.listing_service.select")
    async def test_get_listings_sort_calls(self, mock_sqlalchemy_select):
        mock_query = MagicMock()
        mock_ordered_query = MagicMock()
        mock_sqlalchemy_select.return_value = mock_query
        mock_query.order_by.return_value = mock_ordered_query

        mock_sort_function = MagicMock(name="sort_function")
        mock_sort_options = MockSortOptions(sort_func_to_return=mock_sort_function)

        await self.listing_service.get_listings(
            sort_options=mock_sort_options, filter=None
        )

        mock_sort_options.get_sort_func_mock.assert_called_once()
        mock_query.order_by.assert_called_once_with(mock_sort_function)
        self.mock_repository.get_listings.assert_called_once_with(
            query=mock_ordered_query
        )

    @patch(
        "app.application.interfaces.services.listing_service.Listing",
        new=MockListingModel,
    )
    @patch("app.application.interfaces.services.listing_service.select")
    @patch("app.application.interfaces.services.listing_service.getattr")
    async def test_get_listings_filter_and_sort_combined_calls(
        self, mock_getattr, mock_sqlalchemy_select
    ):
        mock_query = MagicMock()
        mock_filtered_query = MagicMock()
        mock_ordered_query = MagicMock()
        mock_sqlalchemy_select.return_value = mock_query
        mock_query.where.return_value = mock_filtered_query
        mock_filtered_query.order_by.return_value = mock_ordered_query

        mock_filter_column = MagicMock(name="MockFilterColumn")
        mock_filter_expression_method = MagicMock(name="MockLikeExpressionMethod")

        mock_getattr.side_effect = [mock_filter_column, mock_filter_expression_method]

        mock_sort_function = MagicMock(name="sort_function")
        mock_sort_options = MockSortOptions(sort_func_to_return=mock_sort_function)
        mock_filter_dto = MockFilterDTO(
            field="description", value="nice", operator_to_return="like"
        )

        await self.listing_service.get_listings(
            sort_options=mock_sort_options, filter=mock_filter_dto
        )

        expected_getattr_calls = [
            mock_call(MockListingModel, "description"),
            mock_call(mock_filter_column, "like"),  # This is the operator name
        ]
        mock_getattr.assert_has_calls(expected_getattr_calls, any_order=False)
        mock_filter_dto.get_operator_mock.assert_called_once()
        mock_sort_options.get_sort_func_mock.assert_called_once()

        mock_query.where.assert_called_once()
        mock_filter_expression_method.assert_called_once_with("%nice%")
        mock_filtered_query.order_by.assert_called_once_with(mock_sort_function)
        self.mock_repository.get_listings.assert_called_once_with(
            query=mock_ordered_query
        )

    async def test_get_listings_repository_raises_exception(self):
        mock_sort_options = MockSortOptions()
        self.mock_repository.get_listings.side_effect = Exception(
            "DB GetListings Error"
        )
        with self.assertRaisesRegex(Exception, "DB GetListings Error"):
            await self.listing_service.get_listings(
                sort_options=mock_sort_options, filter=None
            )

    @patch("app.application.interfaces.services.listing_service.select")
    async def test_get_listings_filter_is_none_no_where_call(
        self, mock_sqlalchemy_select
    ):
        mock_query = MagicMock()
        mock_sqlalchemy_select.return_value = mock_query
        mock_sort_options = MockSortOptions(sort_func_to_return=None)

        await self.listing_service.get_listings(
            sort_options=mock_sort_options, filter=None
        )
        mock_query.where.assert_not_called()
        self.mock_repository.get_listings.assert_called_once_with(query=mock_query)

    @patch("app.application.interfaces.services.listing_service.select")
    async def test_get_listings_sort_func_is_none_no_orderby_call(
        self, mock_sqlalchemy_select
    ):
        mock_query = MagicMock()
        mock_sqlalchemy_select.return_value = mock_query
        mock_sort_options = MockSortOptions(sort_func_to_return=None)

        await self.listing_service.get_listings(
            sort_options=mock_sort_options, filter=None
        )
        mock_query.order_by.assert_not_called()
        self.mock_repository.get_listings.assert_called_once_with(query=mock_query)

    @patch(
        "app.application.interfaces.services.listing_service.Listing",
        new=MockListingModel,
    )
    @patch("app.application.interfaces.services.listing_service.select")
    @patch("app.application.interfaces.services.listing_service.getattr")
    async def test_get_listings_getattr_filter_field_raises_attributeerror(
        self, mock_getattr, mock_sqlalchemy_select
    ):
        mock_sqlalchemy_select.return_value = MagicMock()
        mock_sort_options = MockSortOptions()
        mock_filter_dto = MockFilterDTO(
            field="invalid_field", value="test", operator_to_return="like"
        )

        mock_getattr.side_effect = AttributeError("Invalid field")

        with self.assertRaisesRegex(AttributeError, "Invalid field"):
            await self.listing_service.get_listings(
                sort_options=mock_sort_options, filter=mock_filter_dto
            )
        mock_getattr.assert_called_once_with(MockListingModel, "invalid_field")

    @patch(
        "app.application.interfaces.services.listing_service.Listing",
        new=MockListingModel,
    )
    @patch("app.application.interfaces.services.listing_service.select")
    @patch("app.application.interfaces.services.listing_service.getattr")
    async def test_get_listings_getattr_filter_operator_raises_attributeerror(
        self, mock_getattr, mock_sqlalchemy_select
    ):
        mock_query = MagicMock()
        mock_sqlalchemy_select.return_value = mock_query

        mock_filter_column = MagicMock(name="MockFilterColumn")
        mock_filter_dto = MockFilterDTO(
            field="title", value="test", operator_to_return="invalid_op"
        )

        def getattr_side_effect(obj, name):
            if obj is MockListingModel and name == "title":
                return mock_filter_column
            if obj is mock_filter_column and name == "invalid_op":
                raise AttributeError("Invalid operator")
            return unittest.mock.DEFAULT

        mock_getattr.side_effect = getattr_side_effect

        mock_sort_options = MockSortOptions()

        with self.assertRaisesRegex(AttributeError, "Invalid operator"):
            await self.listing_service.get_listings(
                sort_options=mock_sort_options, filter=mock_filter_dto
            )

        expected_getattr_calls = [
            mock_call(MockListingModel, "title"),
            mock_call(mock_filter_column, "invalid_op"),
        ]
        mock_getattr.assert_has_calls(expected_getattr_calls)
        mock_query.where.assert_not_called()

    @patch("app.application.interfaces.services.listing_service.select")
    async def test_get_listings_returns_iterable_from_repo(self, mock_select):
        mock_select.return_value = MagicMock()
        mock_sort_options = MockSortOptions()
        expected_return = [MockListingDB(id=1, title="t", description="d")]
        self.mock_repository.get_listings.return_value = expected_return

        result = await self.listing_service.get_listings(
            sort_options=mock_sort_options, filter=None
        )
        self.assertEqual(result, expected_return)
        self.assertIsInstance(result, list)

    @patch("app.application.interfaces.services.listing_service.select")
    async def test_get_listings_repo_returns_empty_iterable(self, mock_select):
        mock_select.return_value = MagicMock()
        mock_sort_options = MockSortOptions()
        self.mock_repository.get_listings.return_value = []

        result = await self.listing_service.get_listings(
            sort_options=mock_sort_options, filter=None
        )
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
