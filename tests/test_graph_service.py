import io
import unittest
from datetime import datetime
from unittest.mock import ANY, AsyncMock, patch

import numpy as np
import pandas as pd

from app.application.interfaces.services.graph_service import GraphService


class MockListingDB:
    def __init__(self, price: float, area: float, created_at: datetime):
        self.price = price
        self.area = area
        self.created_at = created_at

    def model_dump(self, include=None):
        return {"price": self.price, "area": self.area, "created_at": self.created_at}


class TestGraphServiceExpanded(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_listing_repo = AsyncMock()
        self.graph_service = GraphService(repository=self.mock_listing_repo)

        self.mock_listings_data_multi_year = [
            MockListingDB(price=100000, area=50, created_at=datetime(2022, 1, 15)),
            MockListingDB(price=120000, area=60, created_at=datetime(2022, 1, 20)),
            MockListingDB(price=110000, area=55, created_at=datetime(2022, 2, 10)),
            MockListingDB(price=150000, area=70, created_at=datetime(2023, 3, 5)),
            MockListingDB(price=160000, area=75, created_at=datetime(2023, 3, 12)),
            MockListingDB(price=140000, area=65, created_at=datetime(2023, 4, 1)),
        ]
        self.single_listing_data = [
            MockListingDB(price=200000, area=100, created_at=datetime(2023, 5, 10))
        ]

    def assert_common_plot_calls(
        self, mock_sns, mock_plt, expected_title, is_all_years_plot=True
    ):
        mock_sns.set_theme.assert_called_once_with("poster")
        mock_plt.figure.assert_called_once_with(figsize=(12, 7), dpi=100)
        mock_sns.relplot.assert_called_once()

        call_args, call_kwargs = mock_sns.relplot.call_args
        self.assertEqual(call_kwargs["x"], "month")
        self.assertEqual(call_kwargs["y"], "price")
        self.assertEqual(call_kwargs["kind"], "line")
        if is_all_years_plot:
            self.assertEqual(call_kwargs["hue"], "year")
        else:
            self.assertNotIn("hue", call_kwargs)

        mock_plt.title.assert_called_once_with(expected_title)
        mock_plt.xlim.assert_called_once_with(1, 12)
        mock_plt.savefig.assert_called_once_with(ANY, format="png")
        mock_plt.close.assert_called_once_with("all")

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_all_years_repo_and_initial_plot_setup(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=None)
        self.mock_listing_repo.get_listings.assert_called_once()
        mock_sns.set_theme.assert_called_once_with("poster")
        mock_plt.figure.assert_called_once_with(figsize=(12, 7), dpi=100)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_all_years_relplot_data_structure(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=None)
        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args
        actual_df_arg = call_kwargs["data"]
        self.assertIsInstance(actual_df_arg, pd.DataFrame)
        self.assertIn("price", actual_df_arg.columns)
        self.assertEqual(actual_df_arg.index.names, ["year", "month"])
        self.assertFalse(actual_df_arg.empty)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_all_years_relplot_arguments(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=None)
        call_args, call_kwargs = mock_sns.relplot.call_args
        self.assertEqual(call_kwargs["x"], "month")
        self.assertEqual(call_kwargs["y"], "price")
        self.assertEqual(call_kwargs["kind"], "line")
        self.assertEqual(call_kwargs["hue"], "year")

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_all_years_plot_finalization(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=None)
        mock_plt.title.assert_called_once_with("All years")
        mock_plt.xlim.assert_called_once_with(1, 12)
        mock_plt.savefig.assert_called_once_with(ANY, format="png")
        mock_plt.close.assert_called_once_with("all")

    async def test_all_years_return_type(self):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        with (
            patch("app.application.interfaces.services.graph_service.plt"),
            patch("app.application.interfaces.services.graph_service.sns"),
        ):
            buffer = await self.graph_service.generate_graph_buffer(year_or_all=None)
        self.assertIsInstance(buffer, io.BytesIO)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_specific_year_repo_and_initial_plot_setup(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=2022)
        self.mock_listing_repo.get_listings.assert_called_once()
        mock_sns.set_theme.assert_called_once_with("poster")
        mock_plt.figure.assert_called_once_with(figsize=(12, 7), dpi=100)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_specific_year_relplot_data_structure(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=2022)
        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args
        actual_df_arg = call_kwargs["data"]
        self.assertIsInstance(actual_df_arg, pd.DataFrame)
        self.assertIn("price", actual_df_arg.columns)
        self.assertEqual(actual_df_arg.index.name, "month")
        self.assertFalse(actual_df_arg.empty)
        self.assertEqual(len(actual_df_arg), 2)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_specific_year_relplot_arguments(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=2022)
        call_args, call_kwargs = mock_sns.relplot.call_args
        self.assertEqual(call_kwargs["x"], "month")
        self.assertEqual(call_kwargs["y"], "price")
        self.assertEqual(call_kwargs["kind"], "line")
        self.assertNotIn("hue", call_kwargs)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_specific_year_plot_finalization(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=2022)
        mock_plt.title.assert_called_once_with("2022")
        mock_plt.xlim.assert_called_once_with(1, 12)
        mock_plt.savefig.assert_called_once_with(ANY, format="png")
        mock_plt.close.assert_called_once_with("all")

    async def test_specific_year_return_type(self):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        with (
            patch("app.application.interfaces.services.graph_service.plt"),
            patch("app.application.interfaces.services.graph_service.sns"),
        ):
            buffer = await self.graph_service.generate_graph_buffer(year_or_all=2022)
        self.assertIsInstance(buffer, io.BytesIO)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_year_not_exists_defaults_to_all_years_plot(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=2025)
        self.assert_common_plot_calls(
            mock_sns, mock_plt, "All years", is_all_years_plot=True
        )

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_year_not_exists_relplot_data_structure(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=2025)
        call_args, call_kwargs = mock_sns.relplot.call_args
        actual_df_arg = call_kwargs["data"]
        self.assertIsInstance(actual_df_arg, pd.DataFrame)
        self.assertEqual(actual_df_arg.index.names, ["year", "month"])

    async def test_year_not_exists_return_type(self):
        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        with (
            patch("app.application.interfaces.services.graph_service.plt"),
            patch("app.application.interfaces.services.graph_service.sns"),
        ):
            buffer = await self.graph_service.generate_graph_buffer(year_or_all=2025)
        self.assertIsInstance(buffer, io.BytesIO)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_no_listings_setup_calls(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = []
        await self.graph_service.generate_graph_buffer(year_or_all=None)

        self.mock_listing_repo.get_listings.assert_called_once()
        mock_sns.set_theme.assert_called_once_with("poster")
        mock_plt.figure.assert_called_once_with(figsize=(12, 7), dpi=100)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_no_listings_relplot_data_structure(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = []
        await self.graph_service.generate_graph_buffer(year_or_all=None)

        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args
        actual_df_arg = call_kwargs["data"]
        self.assertIsInstance(actual_df_arg, pd.DataFrame)
        self.assertTrue(
            actual_df_arg.empty, "DataFrame should be empty for no listings."
        )
        self.assertIn(
            "price",
            actual_df_arg.columns,
            "DataFrame should still have 'price' column.",
        )

        if isinstance(actual_df_arg.index, pd.MultiIndex):
            self.assertEqual(actual_df_arg.index.names, ["year", "month"])

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_no_listings_plot_finalization(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = []
        await self.graph_service.generate_graph_buffer(year_or_all=None)

        self.assert_common_plot_calls(
            mock_sns, mock_plt, "All years", is_all_years_plot=True
        )

    async def test_no_listings_return_type(self):
        self.mock_listing_repo.get_listings.return_value = []
        with (
            patch("app.application.interfaces.services.graph_service.plt"),
            patch("app.application.interfaces.services.graph_service.sns"),
        ):
            buffer = await self.graph_service.generate_graph_buffer(year_or_all=None)
        self.assertIsInstance(buffer, io.BytesIO)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_single_listing_repo_and_initial_plot_setup(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = self.single_listing_data
        await self.graph_service.generate_graph_buffer(year_or_all=None)
        self.mock_listing_repo.get_listings.assert_called_once()
        mock_sns.set_theme.assert_called_once_with("poster")
        mock_plt.figure.assert_called_once_with(figsize=(12, 7), dpi=100)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_single_listing_relplot_data_structure(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = self.single_listing_data
        await self.graph_service.generate_graph_buffer(year_or_all=None)
        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args
        actual_df_arg = call_kwargs["data"]
        self.assertIsInstance(actual_df_arg, pd.DataFrame)
        self.assertIn("price", actual_df_arg.columns)
        self.assertEqual(actual_df_arg.index.names, ["year", "month"])
        self.assertEqual(len(actual_df_arg), 1)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_single_listing_plot_finalization(self, mock_sns, mock_plt):
        self.mock_listing_repo.get_listings.return_value = self.single_listing_data
        await self.graph_service.generate_graph_buffer(year_or_all=None)
        mock_plt.title.assert_called_once_with("All years")
        mock_plt.xlim.assert_called_once_with(1, 12)
        mock_plt.savefig.assert_called_once_with(ANY, format="png")

    async def test_single_listing_return_type(self):
        self.mock_listing_repo.get_listings.return_value = self.single_listing_data
        with (
            patch("app.application.interfaces.services.graph_service.plt"),
            patch("app.application.interfaces.services.graph_service.sns"),
        ):
            buffer = await self.graph_service.generate_graph_buffer(year_or_all=None)
        self.assertIsInstance(buffer, io.BytesIO)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_data_with_zero_area_leads_to_inf_price(self, mock_sns, mock_plt):
        data_with_zero_area = [
            MockListingDB(price=100000, area=0, created_at=datetime(2022, 1, 15))
        ]
        self.mock_listing_repo.get_listings.return_value = data_with_zero_area

        await self.graph_service.generate_graph_buffer(year_or_all=None)

        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args
        df_arg = call_kwargs["data"]
        self.assertTrue(np.isinf(df_arg["price"].iloc[0]))

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_data_with_negative_area_leads_to_negative_price(
        self, mock_sns, mock_plt
    ):
        data_with_neg_area = [
            MockListingDB(price=100000, area=-50, created_at=datetime(2022, 1, 15))
        ]
        self.mock_listing_repo.get_listings.return_value = data_with_neg_area
        await self.graph_service.generate_graph_buffer(year_or_all=None)
        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args
        df_arg = call_kwargs["data"]
        self.assertTrue(df_arg["price"].iloc[0] < 0)

    async def test_data_with_malformed_date_string(self):
        pass

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_data_missing_required_key_from_model_dump(self, mock_sns, mock_plt):
        class FaultyMockListingDB:
            def model_dump(self, include=None):
                return {"price": 100, "created_at": datetime(2022, 1, 1)}

        self.mock_listing_repo.get_listings.return_value = [FaultyMockListingDB()]
        with self.assertRaises(KeyError):
            await self.graph_service.generate_graph_buffer(year_or_all=None)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_graph_service_handles_repository_raising_general_exception(
        self, mock_sns, mock_plt
    ):
        self.mock_listing_repo.get_listings.side_effect = Exception(
            "Unexpected DB Error"
        )
        with self.assertRaisesRegex(Exception, "Unexpected DB Error"):
            await self.graph_service.generate_graph_buffer(year_or_all=None)

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_plotting_functions_called_in_order(self, mock_sns, mock_plt):
        manager = unittest.mock.Mock()
        manager.attach_mock(mock_sns.set_theme, "set_theme")
        manager.attach_mock(mock_plt.figure, "figure")
        manager.attach_mock(mock_sns.relplot, "relplot")
        manager.attach_mock(mock_plt.title, "title")
        manager.attach_mock(mock_plt.xlim, "xlim")
        manager.attach_mock(mock_plt.savefig, "savefig")
        manager.attach_mock(mock_plt.close, "close")

        self.mock_listing_repo.get_listings.return_value = (
            self.mock_listings_data_multi_year
        )
        await self.graph_service.generate_graph_buffer(year_or_all=None)

        mock_sns.set_theme.assert_called_once()
        mock_plt.figure.assert_called_once()
        mock_sns.relplot.assert_called_once()
        mock_plt.title.assert_called_once()
        mock_plt.xlim.assert_called_once()
        mock_plt.savefig.assert_called_once()
        mock_plt.close.assert_called_once()

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_data_with_only_one_year_multiple_months(self, mock_sns, mock_plt):
        one_year_data = [
            MockListingDB(price=100, area=10, created_at=datetime(2023, 1, 1)),
            MockListingDB(price=120, area=10, created_at=datetime(2023, 2, 1)),
            MockListingDB(price=110, area=10, created_at=datetime(2023, 3, 1)),
        ]
        self.mock_listing_repo.get_listings.return_value = one_year_data
        await self.graph_service.generate_graph_buffer(year_or_all=None)

        call_args, call_kwargs = mock_sns.relplot.call_args
        df_arg = call_kwargs["data"]
        self.assertEqual(df_arg.index.get_level_values("year").nunique(), 1)
        self.assertEqual(len(df_arg), 3)
        self.assertEqual(call_kwargs["hue"], "year")

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_data_with_all_prices_zero(self, mock_sns, mock_plt):
        zero_price_data = [
            MockListingDB(price=0, area=50, created_at=datetime(2022, 1, 15)),
            MockListingDB(price=0, area=60, created_at=datetime(2022, 2, 20)),
        ]
        self.mock_listing_repo.get_listings.return_value = zero_price_data
        await self.graph_service.generate_graph_buffer(year_or_all=None)

        call_args, call_kwargs = mock_sns.relplot.call_args
        df_arg = call_kwargs["data"]
        self.assertTrue((df_arg["price"] == 0).all())


if __name__ == "__main__":
    unittest.main()
