"Fetch data from the Shopify API"

import time
import inspect

from socket import gaierror
from pyactiveresource.connection import (
    ClientError as ActiveResourceClientError,
    ServerError as ActiveResourceServerError,
    ConnectionError as ActiveResourceConnectionError
)

import pandas as pd

import shopify

from gofetch.utils.decorator_utils import retry_decorator
from gofetch.parsers.shopify.parse_shopify import (
    parse_article, parse_blog, parse_collection,
    parse_customer, parse_discount, parse_event,
    parse_gift_card, parse_inventory_item,
    parse_marketing_event, parse_order,
    parse_page, parse_product
)


class FetchShopify:
    "Shopify fetching class"
    def __init__(self, api_key: str, access_token: str, shop_name: str, url: str):
        """
        Initializes the FetchShopify class with the given access token and shop name.

        @params:
        - api_key (str):
            The API key.
        - access_token (str):
            The access token for Shopify API.
        - shop_name (str):
            The name of the Shopify store.
        - url (str):
            The base URL for the site.
        """
        self.url = url
        self.resource = shopify.ShopifyResource
        self.resource.set_site(
            f"https://{api_key}:{access_token}@{shop_name}.myshopify.com/admin"
        )

    def clear_session(self):
        """
        Clears the current Shopify API session.
        """
        self.resource.clear_session()

    def depaginate_shopify(
        self,
        paginated_object: object,
        _print: bool = False
    ) -> list:
        """
        Depaginates a Shopify object.

        @params:
        - paginated_collection (shopify object):
            The paginated Shopify object to depaginate.
        - _print (bool):
            Whether to print the number of items processed.
            Default is False.

        @returns:
        - list:
            A list containing all items from the paginated collection.
        """
        items = []
        while True:
            items.extend(paginated_object)
            if _print:
                print(f"Fetched {len(items)} items so far.")  # Debug statement
            if paginated_object.has_next_page():
                time.sleep(1)
                paginated_object = paginated_object.next_page()
            else:
                break
        return items

    def check_fields(self, resource_type: shopify.ShopifyResource, parse_function: callable):
        """
        Checks which fields are available in a resource type
        and which are used in a parse function.

        Examples:
        - self.check_fields(resource_type=shopify.Article, parse_function=parse_article)
        - self.check_fields(resource_type=shopify.Product, parse_function=parse_product)
        - self.check_fields(resource_type=shopify.SmartCollection, parse_function=parse_collection)
        - self.check_fields(resource_type=shopify.Blog, parse_function=parse_blog)
        - self.check_fields(resource_type=shopify.Page, parse_function=parse_page)
        - self.check_fields(resource_type=shopify.Order, parse_function=parse_order)
        - self.check_fields(resource_type=shopify.Customer, parse_function=parse_customer)
        - self.check_fields(resource_type=shopify.Event, parse_function=parse_event)
        - self.check_fields(resource_type=shopify.DiscountCode, parse_function=parse_discount)
        - self.check_fields(resource_type=shopify.GiftCard, parse_function=parse_gift_card)
        - self.check_fields(resource_type=shopify.InventoryItem, parse_function=parse_inventory_item)
        - self.check_fields(resource_type=shopify.MarketingEvent, parse_function=parse_marketing_event)

        @params:
        - resource_type (shopify.ShopifyResource):
            The Shopify resource type e.g., Page, Product, etc.
        - parse_function (callable):
            The parsing function to use on the Shopify Resource.
        """
        sample_items = self.fetch_data(resource_type=resource_type, limit=1)
        if not sample_items:
            print(f"No data available to analyze fields for {resource_type.__name__}.")
            return

        sample_item = sample_items[0]
        func_params = inspect.signature(parse_function).parameters
        call_args = {}

        if 'site_url' in func_params:
            call_args['site_url'] = self.url

        parsed_data = parse_function(sample_item, **call_args)
        used_fields = set(parsed_data.keys())
        available_fields = set(sample_item.attributes.keys())
        unused_fields = sorted(available_fields - used_fields)
        #print(
        # f"Available fields in {resource_type.__name__}: "
        # f"{', '.join(sorted(available_fields))}")

        #print(f"Used fields in parsing function: {', '.join(sorted(used_fields))}")

        print(
            f"Potentially unused fields in {str(resource_type)}: "
            f"{', '.join(unused_fields) if unused_fields else "None"}")

    @retry_decorator(
        ActiveResourceClientError,
        ActiveResourceServerError,
        ActiveResourceConnectionError,
        gaierror,
        max_attempts=3, wait_seconds=1
    )
    def fetch_data(
        self,
        resource_type: shopify.ShopifyResource,
        from_date: str = None,
        to_date: str = None,
        **kwargs
    ) -> list:
        """
        Fetches data with optional date filtering.

        @params:
        - resource_type (shopify.ShopifyResource):
            Resource to fetch.
        - from_date (str):
            Start date for filtering (YYYY-MM-DD).
        - to_date (str):
            End date for filtering (YYYY-MM-DD).
        - **kwargs:
            Additional filtering options.
        """
        if from_date and to_date:
            kwargs.update({
                "created_at_min": from_date,
                "created_at_max": to_date
            })
        return self.depaginate_shopify(resource_type.find(**kwargs))

    def get_dataframe(
        self,
        resource_type: shopify.ShopifyResource,
        parse_function: callable,
        **kwargs
    ) -> pd.DataFrame:
        """
        Retrieves data as a DataFrame.

        @params:
        - resource_type (shopify.ShopifyResource):
            The Shopify resource to fetch (e.g., shopify.Product).
        - parse_function (function):
            The function to parse individual items.
        - **kwargs (dict):
            Additional arguments for fetching data.

        @returns:
        - pd.DataFrame:
            A DataFrame containing parsed data.
        """
        data = self.fetch_data(resource_type=resource_type, **kwargs)

        params = inspect.signature(parse_function).parameters
        if 'site_url' in params:
            results = [parse_function(item, site_url=self.url) for item in data]
        else:
            results = [parse_function(item) for item in data]

        return pd.DataFrame(results)

    def get_products_dataframe(self) -> pd.DataFrame:
        """
        Retrieves products as a DataFrame.

        @returns:
        - pd.DataFrame: A DataFrame containing the products.
        """
        return self.get_dataframe(
            resource_type=shopify.Product,
            parse_function=parse_product
        )

    def get_collections_dataframe(self) -> pd.DataFrame:
        """
        Retrieves collections as a DataFrame.

        @returns:
        - pd.DataFrame: A DataFrame containing the collections.
        """
        return pd.concat(
            [
                self.get_dataframe(
                    resource_type=shopify.SmartCollection,
                    parse_function=parse_collection
                ),
                self.get_dataframe(
                    resource_type=shopify.CustomCollection,
                    parse_function=parse_collection
                )
            ]
        )

    def get_articles_dataframe(self) -> pd.DataFrame:
        """
        Retrieves articles as a DataFrame.

        @returns:
        - pd.DataFrame: A DataFrame containing the articles.
        """
        return self.get_dataframe(resource_type=shopify.Article, parse_function=parse_article)

    def get_blogs_dataframe(self) -> pd.DataFrame:
        """
        Retrieves blogs as a DataFrame.

        @returns:
        - pd.DataFrame: A DataFrame containing the blogs.
        """
        return self.get_dataframe(resource_type=shopify.Blog, parse_function=parse_blog)

    def get_pages_dataframe(self) -> pd.DataFrame:
        """
        Retrieves pages as a DataFrame.

        @returns:
        - pd.DataFrame: A Dataframe containing the pages
        """
        return self.get_dataframe(resource_type=shopify.Page, parse_function=parse_page)

    def get_orders_dataframe(self, from_date=None, to_date=None) -> pd.DataFrame:
        """
        Retrieves orders within a specified date range.

        @params:
        - from_date (str):
            Start date for filtering (YYYY-MM-DD).
        - to_date (str):
            End date for filtering (YYYY-MM-DD).
        """
        return self.get_dataframe(
            resource_type=shopify.Order,
            parse_function=parse_order,
            from_date=from_date,
            to_date=to_date
        )

    def get_customers_dataframe(self, from_date=None, to_date=None) -> pd.DataFrame:
        """
        Retrieves customers within a specified date range as a DataFrame.

        @params:
        - from_date (str):
            Start date for filtering (YYYY-MM-DD).
        - to_date (str):
            End date for filtering (YYYY-MM-DD).

        @returns:
        - pd.DataFrame:
            A DataFrame containing the customers.
        """
        return self.get_dataframe(
            resource_type=shopify.Customer,
            parse_function=parse_customer,
            from_date=from_date,
            to_date=to_date
        )

    def get_events_dataframe(self, from_date=None, to_date=None) -> pd.DataFrame:
        """
        Retrieves events within a specified date range as a DataFrame.

        @params:
        - from_date (str):
            Start date for filtering (YYYY-MM-DD).
        - to_date (str):
            End date for filtering (YYYY-MM-DD).

        @returns:
        - pd.DataFrame:
            A DataFrame containing the events.
        """
        events = self.fetch_data(
            resource_type=shopify.Event,
            from_date=from_date,
            to_date=to_date
        )
        df_events = pd.DataFrame([parse_event(event) for event in events])
        return df_events

    def get_discounts_dataframe(self) -> pd.DataFrame:
        """
        Retrieves discounts as a DataFrame.

        @returns:
        - pd.DataFrame: A DataFrame containing the discounts.
        """
        discounts = self.fetch_data(resource_type=shopify.DiscountCode)
        return pd.DataFrame([parse_discount(discount) for discount in discounts])

    def get_gift_cards_dataframe(self) -> pd.DataFrame:
        """
        Retrieves gift cards as a DataFrame.

        @returns:
        - pd.DataFrame:
            A DataFrame containing the gift cards.
        """
        gift_cards = self.fetch_data(resource_type=shopify.GiftCard)
        return pd.DataFrame([parse_gift_card(gift_card) for gift_card in gift_cards])

    def get_inventory_items_dataframe(self) -> pd.DataFrame:
        """
        Retrieves inventory items as a DataFrame.

        @returns:
        - pd.DataFrame: A DataFrame containing the inventory items.
        """
        inventory_items = self.fetch_data(resource_type=shopify.InventoryItem)
        return pd.DataFrame([parse_inventory_item(item) for item in inventory_items])

    def get_marketing_events_dataframe(self) -> pd.DataFrame:
        """
        Retrieves marketing events as a DataFrame.

        @returns:
        - pd.DataFrame: A DataFrame containing the marketing events.
        """
        marketing_events = self.fetch_data(resource_type=shopify.MarketingEvent)
        return pd.DataFrame([parse_marketing_event(event) for event in marketing_events])
