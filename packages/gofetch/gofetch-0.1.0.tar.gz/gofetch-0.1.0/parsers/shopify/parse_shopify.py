"The parsing module for Shopify"

from bs4 import BeautifulSoup


from shopify import (
    Article, Product, CustomCollection,
    Blog, Page, Order, Customer, Event,
    DiscountCode, GiftCard, InventoryItem,
    MarketingEvent, Address
)

from utils.date_utils import convert_to_iso
from utils.nlp_utils import strip_text


def parse_article(article: Article, site_url: str) -> dict:
    """
    Parses a Shopify article into a dictionary.

    @params:
    - article (shopify.Article):
        The Shopify article to parse.
    - site_url (str):
        The base URL of the site. Used to generate url_full field.

    @returns:
    - dict:
        A dictionary containing the article data.
    """
    text = BeautifulSoup(article.body_html, "html.parser").get_text()

    url_full = (
        f"{site_url}/blogs/byte-sized-blogs/{article.handle}"
        if hasattr(article, 'handle') else None
    )

    _d = {
        "id": int(article.id),
        "blog_id": int(article.blog_id),
        "user_id": int(article.user_id),
        "url_full": url_full,
        "handle": article.handle,
        "title": article.title,
        "author": article.author,
        "body_html": article.body_html,
        "summary_html": article.summary_html if hasattr(article, 'summary_html') else None,
        "text": strip_text(text),
        "tags": article.tags(),
        "metafields": [
            {
                'namespace': mf.namespace,
                'key': mf.key,
                'value': mf.value
            } for mf in article.metafields()
        ] if hasattr(article, 'metafields') else [],
        "admin_graphql_api_id": article.admin_graphql_api_id,
        "template_suffix": article.template_suffix,
        "created_at": convert_to_iso(article.created_at),
        "published_at": convert_to_iso(article.published_at),
        "updated_at": convert_to_iso(article.updated_at)
    }

    return _d


def parse_product(product: Product, site_url: str) -> dict:
    """
    Parses a Shopify product into dictionaries.

    @params:
    - product (shopify.Product):
        The Shopify product to parse.
    - site_url (str):
        The site URL, used to create url_full

    @returns:
    - tuple[list[dict], list[dict]]:
        A tuple containing the product data and variant data.
    """
    text = BeautifulSoup(product.body_html, "html.parser").get_text()

    url_full = (
        f"{site_url}/products/{product.handle}"
        if hasattr(product, 'handle') else None
    )

    images = [
        {
            'src': img.src,
            'alt_text': img.alt,
            'width': img.width,
            'height': img.height
        }
        for img in product.images
    ]

    # Extract metafields
    metafields = [
        {
            'namespace': mf.namespace,
            'key': mf.key,
            'value': mf.value,
            'description': mf.description
        }
        for mf in product.metafields()
    ]

    _d = {
        "id": int(product.id),
        "url_full": url_full,
        "handle": product.handle,
        "title": product.title,
        "body_html": product.body_html,
        "text": strip_text(text),
        "status": product.status,
        "vendor": product.vendor,
        "product_type": product.product_type,
        "price_range": product.price_range(),
        "tags": [_s.strip() for _s in product.tags.split(',')],
        "metafields": metafields,
        "images": images,
        "published_scope": product.published_scope,
        "variants": [variant.id for variant in product.variants],
        "template_suffix": product.template_suffix,
        "admin_graphql_api_id": product.admin_graphql_api_id,
        "created_at": convert_to_iso(product.created_at),
        "published_at": convert_to_iso(product.published_at),
        "updated_at": convert_to_iso(product.updated_at)
    }

    return _d


def parse_collection(collection: CustomCollection, site_url: str) -> dict:
    """
    Parses a Shopify collection into a dictionary.

    @params:
    - collection (shopify.CustomCollection):
        The Shopify collection to parse.
    - site_url (str):
        The base URL of the site, to prepend to
        collection handles to create the full URL.

    @returns:
    - dict:
        A dictionary containing the collection data.
    """
    text = BeautifulSoup(collection.body_html, "html.parser").get_text()

    url_full = (
        f"{site_url}/collections/{collection.handle}"
        if hasattr(collection, 'handle') else None
    )

    products = collection.products()

    images = {
        'src': collection.image.src if collection.image else None,
        'alt_text': (
            collection.image.alt if collection.image and collection.image.alt
            else 'No alt text'
        )
    }

    # Collection metafields
    metafields = [
        {
            'namespace': mf.namespace,
            'key': mf.key,
            'value': mf.value
        } for mf in collection.metafields()
    ]

    _d = {
        "id": int(collection.id),
        "url_full": url_full,
        "handle": collection.handle,
        "title": collection.title,
        "body_html": collection.body_html,
        "text": strip_text(text),
        "product_count": len(products),
        "product_ids": [_p.id for _p in products],
        "template_suffix": collection.template_suffix,
        "images": images,
        "metafields": metafields,
        "disjunctive": collection.disjunctive,
        "published_scope": collection.published_scope,
        "admin_graphql_api_id": collection.admin_graphql_api_id,
        "published_at": convert_to_iso(collection.published_at),
        "updated_at": convert_to_iso(collection.updated_at)
    }

    return _d


def parse_blog(blog: Blog, site_url: str) -> dict:
    """
    Parses a Shopify blog into a dictionary.

    @params:
    - blog (shopify.Blog): The Shopify blog to parse.
    - site_url (str): The base URL for the Shop.

    @returns:
    - dict: A dictionary containing the blog data.
    """
    text = (
        BeautifulSoup(blog.body_html, "html.parser").get_text()
        if hasattr(blog, 'body_html') else None
    )

    url_full = (
        f"{site_url}/blogs/{blog.handle}"
        if hasattr(blog, 'handle') else None
    )

    _d = {
        "id": int(blog.id),
        "url_full": url_full,
        "handle": blog.handle,
        "title": blog.title,
        "body_html": blog.body_html if hasattr(blog, 'body_html') else None,
        "text": strip_text(text),
        "articles": [article.id for article in blog.articles()],
        "author": blog.author if hasattr(blog, 'author') else "Unknown",
        "tags": blog.tags if hasattr(blog, 'tags') else [],
        "commentable": blog.commentable if hasattr(blog, 'commentable') else None,
        "metafields": [
            {
                'namespace': mf.namespace,
                'key': mf.key,
                'value': mf.value
            } for mf in blog.metafields()
        ] if hasattr(blog, 'metafields') else [],
        "feedburner": blog.feedburner,
        "feedburner_location": blog.feedburner_location,
        "template_suffix": blog.template_suffix,
        "admin_graphql_api_id": blog.admin_graphql_api_id,
        "created_at": convert_to_iso(blog.created_at),
        "updated_at": convert_to_iso(blog.updated_at)
    }

    return _d


def parse_page(page: Page, site_url: str) -> dict:
    """
    Parses a Shopify page into a dictionary.

    @params:
    - page (shopify.Page):
        The Shopify page object to parse.
    - site_url (str):
        Base URL for the site, used for creating full URLs if needed.

    @returns:
    - dict:
        A dictionary containing essential page details.
    """
    text = BeautifulSoup(page.body_html, "html.parser").get_text()

    _d = {
        "id": int(page.id),
        "url_full": f"{site_url}/pages/{page.handle}",
        "title": page.title,
        "author": page.author,
        "body_html": page.body_html,
        "text": strip_text(text),
        "handle": page.handle,
        "template_suffix": page.template_suffix,
        "admin_graphql_api_id": page.admin_graphql_api_id,
        "shop_id": page.shop_id,
        "created_at": convert_to_iso(page.created_at),
        "published_at": convert_to_iso(page.published_at),
        "updated_at": convert_to_iso(page.updated_at)
    }

    return _d


def parse_order(order: Order) -> dict:
    """
    Parses a Shopify order into a dictionary.

    @params:
    - order (shopify.Order): The Shopify order object to parse.
    - site_url (str): Base URL for the site, used for creating full URLs if needed.

    @returns:
    - dict: A dictionary containing essential order details.
    """
    line_items = [
        {
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price
        }
        for item in order.line_items
    ]

    _d = {
        "order_id": int(order.id),
        "order_number": order.order_number,
        "total_price": order.total_price,
        "order_status_url": order.order_status_url,
        "financial_status": order.financial_status,
        "fulfillment_status": order.fulfillment_status,
        "created_at": convert_to_iso(order.created_at),
        "line_items": line_items
    }

    return _d


def parse_customer(customer: Customer) -> dict:
    """
    Parses a Shopify customer into a dictionary.

    @params:
    - customer (shopify.Customer):
        The Shopify customer object to parse.
    - site_url (str):
        Base URL for the site, used for creating full URLs if needed.

    @returns:
    - dict:
        A dictionary containing essential customer details.
    """
    default_address = format_address(customer.default_address) if customer.default_address else {}
    email_marketing_consent = extract_email_consent(customer.email_marketing_consent)
    sms_marketing_consent = extract_sms_consent(customer.sms_marketing_consent)

    _d = {
        "id": int(customer.id),
        "verified_email": customer.verified_email,
        "default_address1": default_address.get('address1'),
        "default_address2": default_address.get('address2'),
        "default_city": default_address.get('city'),
        "default_province": default_address.get('province'),
        "default_zip": default_address.get('zip'),
        "default_country": default_address.get('country'),
        "orders_count": customer.orders_count,
        "total_spent": float(customer.total_spent),
        "tags": customer.tags,
        "currency": customer.currency,
        "accepts_marketing": customer.accepts_marketing,
        "accepts_marketing_updated_at": convert_to_iso(customer.accepts_marketing_updated_at),
        "marketing_opt_in_level": customer.marketing_opt_in_level,
        "email_marketing_status": email_marketing_consent.get('email_consent_status'),
        "email_marketing_opt_in": email_marketing_consent.get('email_opt_in_level'),
        "sms_marketing_status": sms_marketing_consent.get('sms_consent_status'),
        "sms_marketing_opt_in": sms_marketing_consent.get('sms_opt_in_level'),
        "last_order_id": customer.last_order_id,
        "last_order_name": customer.last_order_name,
        "state": customer.state,
        "note": customer.note,
        "multipass_identifier": customer.multipass_identifier,
        "tax_exempt": customer.tax_exempt,
        "tax_exemptions": customer.tax_exemptions,
        "admin_graphql_api_id": customer.admin_graphql_api_id,
        "created_at": convert_to_iso(customer.created_at),
        "updated_at": convert_to_iso(customer.updated_at),
    }

    return _d


def parse_event(event: Event) -> dict:
    """
    Parses a Shopify event into a dictionary.

    @params:
    - event (shopify.Event):
        The Shopify event object to parse.

    @returns:
    - dict:
        A dictionary containing essential event details.
    """
    api_client_id = extract_api_client_id(event.arguments)
    first_argument = extract_first_argument(event.arguments)
    article_id = None
    if event.subject_type == 'Article' and len(event.arguments) > 1:
        article_id = event.arguments[1]

    _d = {
        "id": int(event.id),
        "subject_id": event.subject_id,
        "subject_type": event.subject_type,
        "verb": event.verb,
        "body": event.body,
        "message": event.message,
        "path": event.path,
        "author": event.author,
        "description": event.description,
        "created_at": convert_to_iso(event.created_at),
        "api_client_id": api_client_id,
        "affected_item": first_argument,
        "article_id": article_id
    }

    return _d


def parse_discount(discount: DiscountCode) -> dict:
    """
    Parses a Shopify discount into a dictionary.

    @params:
    - discount (shopify.DiscountCode):
        The discount object to parse.

    @returns:
    - dict:
        A dictionary containing essential discount details.
    """
    return {
        "id": int(discount.id),
        "code": discount.code,
        "amount": discount.amount,
        "type": discount.type,
        "starts_at": convert_to_iso(discount.starts_at),
        "ends_at": convert_to_iso(discount.ends_at),
        "usage_count": discount.usage_count
    }


def parse_gift_card(gift_card: GiftCard) -> dict:
    """
    Parses a Shopify gift card into a dictionary.

    @params:
    - gift_card (shopify.GiftCard): The gift card object to parse.

    @returns:
    - dict: A dictionary containing essential gift card details.
    """
    return {
        "id": int(gift_card.id),
        "initial_value": gift_card.initial_value,
        "balance": gift_card.balance,
        "code": gift_card.code,
        "created_at": convert_to_iso(gift_card.created_at),
        "expires_on": convert_to_iso(gift_card.expires_on)
    }


def parse_inventory_item(item: InventoryItem) -> dict:
    """
    Parses an inventory item into a dictionary.

    @params:
    - item (shopify.InventoryItem):
        The inventory item to parse.

    @returns:
    - dict:
        A dictionary containing essential inventory item details.
    """
    return {
        "id": int(item.id),
        "sku": item.sku,
        "cost": item.cost,
        "quantity": item.available,
        "created_at": convert_to_iso(item.created_at),
        "updated_at": convert_to_iso(item.updated_at)
    }


def parse_marketing_event(event: MarketingEvent) -> dict:
    """
    Parses a marketing event into a dictionary.

    @params:
    - event (shopify.MarketingEvent):
        The marketing event to parse.

    @returns:
    - dict:
        A dictionary containing essential marketing event details.
    """
    return {
        "id": int(event.id),
        "event_type": event.event_type,
        "status": event.status,
        "start_date": convert_to_iso(event.start_date),
        "end_date": convert_to_iso(event.end_date)
    }


def format_address(address_obj: Address) -> dict:
    """
    Extracts fields from a Shopify address object into a dictionary.

    @params:
    - address_obj (shopify.Address):
        The Shopify address object.

    @returns:
    - dict:
        A dictionary with keys for each address part.
    """
    address_parts = {
        'address1': getattr(address_obj, 'address1', None),
        'address2': getattr(address_obj, 'address2', None),
        'city': getattr(address_obj, 'city', None),
        'province': getattr(address_obj, 'province', None),
        'zip': getattr(address_obj, 'zip', None),
        'country': getattr(address_obj, 'country', None)
    }
    return address_parts


def extract_email_consent(consent_obj) -> dict:
    """
    Extracts consent information from an email_marketing_consent object.

    @params:
    - consent_obj:
        The email marketing consent object from Shopify.

    @returns:
    - dict:
        A dictionary containing consent details.
    """
    if consent_obj is None:
        return {
            "email_consent_status": None,
            "email_opt_in_level": None
        }

    return {
        "email_consent_status": getattr(consent_obj, 'status', None),
        "email_opt_in_level": getattr(consent_obj, 'opt_in_level', None)
    }


def extract_sms_consent(constent_obj) -> dict:
    """
    Extracts consent information from an sms_marketing_consent object.

    @params:
    - consent_obj:
        The SMS marketing consent object from Shopify.

    @returns:
    - dict:
        A dictionary containing sms_consent_status and sms_opt_in_leve.
    """
    if constent_obj is None:
        return {
            "sms_consent_status": None,
            "sms_opt_in_level": None
        }

    return {
        "sms_consent_status": getattr(constent_obj, 'status', None),
        "sms_opt_in_level": getattr(constent_obj, 'opt_in_level', None)
    }


def extract_api_client_id(event_arguments: list) -> str|None:
    """
    Extracts the API client ID from a list of event arguments.
    The function searches for the key 'api_client_id' and
    returns the following value in the list.

    @params:
    - event_arguments (list):
        List containing pairs of keys and values.

    @returns:
    - str|None:
        The value following 'api_client_id' in the list or
        None if 'api_client_id' is not found or has no
        subsequent value.
    """
    if 'api_client_id' in event_arguments:
        # Find the index of 'api_client_id' and get the next item
        idx = event_arguments.index('api_client_id')
        # Ensure there is an item after 'api_client_id'
        if idx + 1 < len(event_arguments):
            return event_arguments[idx + 1]
    # Return None if 'api_client_id' is not found or it has no following number
    return None


def extract_first_argument(event_arguments: list) -> str|None:
    """
    Extracts the first argument from a list of
    event arguments if the list is not empty.

    @params:
    - event_arguments (list):
        A list of event arguments.

    @returns:
    - str|None:
        The first element of the list if it is
        not empty; otherwise, None.
    """
    if event_arguments:  # Check if the list is not empty
        return event_arguments[0]
    return None  # Return None if the list is empty


def extract_article_id(row: dict) -> str|None:
    """
    Extracts the article ID from a row dictionary if specific conditions
    are met. It checks if the subject type is 'Article' and if there are
    more than one argument, then returns the second argument as the
    article ID.

    @params:
    - row (dict):
        A dictionary containing keys 'subject_type' and 'arguments',
        where 'subject_type' is a string and 'arguments' is a list.

    @returns:
    - str|None:
        The second element of 'arguments' if conditions are met;
        otherwise, None.
    """
    if row['subject_type'] == 'Article' and len(row['arguments']) > 1:
        return row['arguments'][1]
    return None
