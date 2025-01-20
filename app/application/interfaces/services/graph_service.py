from typing import Iterable
from sqlalchemy import select
from app.domain.repositories.ilisting_repository import IListingRepository

import seaborn as sns
import pandas as pd
import matplotlib

from app.presentation.schemas.listing_schema import ListingDB
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

from app.infrastructure.models.listing_model import Listing

class GraphService:

    def __init__(self, repository: IListingRepository):
        
        self.repository = repository

    async def generate_graph_buffer(self, year_or_all: int | None = None):
        
        sns.set_theme("poster")

        plt.figure(figsize=(12, 7), dpi=100)

        listings: Iterable[ListingDB] = await self.repository.get_listings(select(Listing))

        dates_data = []
        price_data = []
        area_data = []
        
        
        for listing in listings:
            data = listing.model_dump(include=["price", "area", "created_at"])

            dates_data.append(data["created_at"])

            price_data.append(data["price"])

            area_data.append(data["area"])

        datetime_series = pd.Series(dates_data)

        price_series = pd.Series(price_data)

        area_series = pd.Series(area_data)
        
        price_per_meter = price_series/area_series

        df = pd.DataFrame({
            'date': datetime_series
        })

        df = pd.DataFrame({
            'year': df['date'].dt.year,
            'month': df['date'].dt.month,
            'price': price_per_meter,
        })

        df = df.groupby(['year', 'month']).mean().round()

        if year_or_all:
            sns.relplot(data=df.loc[year_or_all], x="month", y="price", kind="line", height=6, aspect=2)
        else:
            sns.relplot(data=df, x="month", y="price", kind="line", hue="year", height=6, aspect=2)
        
        plt.xlim(1, 12)

        buffer = io.BytesIO()

        plt.savefig(buffer, format='png')
        plt.close('all')

        buffer.seek(0)
        
        return buffer
