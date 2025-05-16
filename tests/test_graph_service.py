import io
import unittest
from datetime import datetime
from unittest.mock import ANY, AsyncMock, patch

import pandas as pd

from app.application.interfaces.services.graph_service import GraphService


class MockListingDB:
    def __init__(self, price: int, area: float, created_at: datetime):
        self.price = price
        self.area = area
        self.created_at = created_at

    def model_dump(self, include=None):
        return {"price": self.price, "area": self.area, "created_at": self.created_at}


class TestGraphService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_repo = AsyncMock()
        self.graph_service = GraphService(repository=self.mock_repo)
        self.mock_listings_data = [
            MockListingDB(price=100000, area=50, created_at=datetime(2022, 1, 15)),
            MockListingDB(price=120000, area=60, created_at=datetime(2022, 1, 20)),
            MockListingDB(price=110000, area=55, created_at=datetime(2022, 2, 10)),
            MockListingDB(price=150000, area=70, created_at=datetime(2023, 3, 5)),
            MockListingDB(price=160000, area=75, created_at=datetime(2023, 3, 12)),
            MockListingDB(price=140000, area=65, created_at=datetime(2023, 4, 1)),
        ]

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_generate_graph_buffer_all_years(self, mock_sns, mock_plt):
        self.mock_repo.get_listings.return_value = self.mock_listings_data

        buffer = await self.graph_service.generate_graph_buffer(year_or_all=None)

        self.assertIsInstance(buffer, io.BytesIO)

        self.mock_repo.get_listings.assert_called_once()
        mock_sns.set_theme.assert_called_once_with("poster")
        mock_plt.figure.assert_called_once_with(figsize=(12, 7), dpi=100)

        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args

        actual_df_arg = call_kwargs["data"]
        self.assertIsInstance(
            actual_df_arg, pd.DataFrame, "Data should be a DataFrame."
        )
        self.assertIn(
            "price", actual_df_arg.columns, "DataFrame should have a 'price' column."
        )
        self.assertEqual(
            actual_df_arg.index.names,
            ["year", "month"],
            "DataFrame index should be ('year', 'month').",
        )
        self.assertFalse(
            actual_df_arg.empty,
            "DataFrame for plotting should not be empty.",
        )

        self.assertEqual(call_kwargs["x"], "month")
        self.assertEqual(call_kwargs["y"], "price")
        self.assertEqual(call_kwargs["kind"], "line")
        self.assertEqual(call_kwargs["hue"], "year")

        mock_plt.title.assert_called_once_with("All years")
        mock_plt.xlim.assert_called_once_with(1, 12)
        mock_plt.savefig.assert_called_once_with(ANY, format="png")
        mock_plt.close.assert_called_once_with("all")

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_generate_graph_buffer_specific_year_exists(self, mock_sns, mock_plt):
        self.mock_repo.get_listings.return_value = self.mock_listings_data
        target_year = 2022

        buffer = await self.graph_service.generate_graph_buffer(year_or_all=target_year)

        self.assertIsInstance(buffer, io.BytesIO)

        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args

        actual_df_arg = call_kwargs["data"]
        self.assertIsInstance(actual_df_arg, pd.DataFrame)
        self.assertIn("price", actual_df_arg.columns)
        self.assertEqual(
            actual_df_arg.index.name, "month", "DataFrame index should be 'month'."
        )
        self.assertFalse(actual_df_arg.empty)
        self.assertEqual(
            len(actual_df_arg),
            2,
            "Should have 2 months of data for 2022 after grouping.",
        )

        self.assertEqual(call_kwargs["x"], "month")
        self.assertEqual(call_kwargs["y"], "price")
        self.assertEqual(call_kwargs["kind"], "line")
        self.assertNotIn("hue", call_kwargs)
        mock_plt.title.assert_called_once_with(f"{target_year}")
        mock_plt.savefig.assert_called_once_with(ANY, format="png")

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_generate_graph_buffer_specific_year_not_exists(
        self, mock_sns, mock_plt
    ):
        self.mock_repo.get_listings.return_value = self.mock_listings_data
        target_year = 2025

        buffer = await self.graph_service.generate_graph_buffer(year_or_all=target_year)

        self.assertIsInstance(buffer, io.BytesIO)

        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args

        actual_df_arg = call_kwargs["data"]
        self.assertIsInstance(actual_df_arg, pd.DataFrame)
        self.assertIn("price", actual_df_arg.columns)
        self.assertEqual(actual_df_arg.index.names, ["year", "month"])
        self.assertFalse(actual_df_arg.empty)

        self.assertEqual(call_kwargs["kind"], "line")
        self.assertEqual(call_kwargs["hue"], "year")
        mock_plt.title.assert_called_once_with("All years")
        mock_plt.savefig.assert_called_once_with(ANY, format="png")

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_generate_graph_buffer_no_listings(self, mock_sns, mock_plt):
        self.mock_repo.get_listings.return_value = []

        buffer = await self.graph_service.generate_graph_buffer(year_or_all=None)

        self.assertIsInstance(buffer, io.BytesIO)

        mock_sns.set_theme.assert_called_once_with("poster")
        mock_plt.figure.assert_called_once_with(figsize=(12, 7), dpi=100)

        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args

        actual_df_arg = call_kwargs["data"]
        self.assertIsInstance(actual_df_arg, pd.DataFrame)
        self.assertTrue(
            actual_df_arg.empty, "DataFrame should be empty when no listings."
        )
        self.assertIn(
            "price",
            actual_df_arg.columns,
            "DataFrame should still have 'price' column.",
        )
        self.assertEqual(
            actual_df_arg.index.names,
            ["year", "month"],
            "Empty DataFrame index should be ('year', 'month').",
        )

        self.assertEqual(call_kwargs["x"], "month")
        self.assertEqual(call_kwargs["y"], "price")
        self.assertEqual(call_kwargs["kind"], "line")
        self.assertEqual(call_kwargs["hue"], "year")

        mock_plt.title.assert_called_once_with("All years")
        mock_plt.savefig.assert_called_once_with(ANY, format="png")
        mock_plt.close.assert_called_once_with("all")

    @patch("app.application.interfaces.services.graph_service.plt")
    @patch("app.application.interfaces.services.graph_service.sns")
    async def test_generate_graph_buffer_single_listing(self, mock_sns, mock_plt):
        single_listing_data = [
            MockListingDB(price=200000, area=100, created_at=datetime(2023, 5, 10))
        ]
        self.mock_repo.get_listings.return_value = single_listing_data

        buffer = await self.graph_service.generate_graph_buffer(year_or_all=None)

        self.assertIsInstance(buffer, io.BytesIO)

        mock_sns.relplot.assert_called_once()
        call_args, call_kwargs = mock_sns.relplot.call_args

        actual_df_arg = call_kwargs["data"]
        self.assertIsInstance(actual_df_arg, pd.DataFrame)
        self.assertIn("price", actual_df_arg.columns)
        self.assertEqual(actual_df_arg.index.names, ["year", "month"])
        self.assertEqual(
            len(actual_df_arg), 1, "DataFrame should have one row for a single listing."
        )
        self.assertAlmostEqual(actual_df_arg["price"].iloc[0], 2000.0, places=1)

        self.assertEqual(call_kwargs["kind"], "line")
        self.assertEqual(call_kwargs["hue"], "year")
        mock_plt.title.assert_called_once_with("All years")
        mock_plt.savefig.assert_called_once_with(ANY, format="png")


if __name__ == "__main__":
    unittest.main()
