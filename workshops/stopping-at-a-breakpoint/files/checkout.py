"""A small shop: the price list at /, and a checkout that charges for an item.

The checkout stops at a breakpoint before it charges, for five minutes,
so a debugger can be attached to it from another terminal.
"""

PRICES = {"teapot": 12, "cup": 3, "saucer": 2}


def application(environ, start_response):
    path = environ["PATH_INFO"]
    query = dict(pair.split("=", 1) for pair in environ["QUERY_STRING"].split("&") if "=" in pair)
    item = query.get("item", "")

    if path == "/checkout":
        price = PRICES.get(item, 0)
        breakpoint(timeout=300)
        body = f"charged {price} for {item}\n"
    elif path == "/refund":
        price = PRICES.get(item, 0)
        breakpoint(timeout=5)
        body = f"refunded {price} for {item}\n"
    else:
        body = "".join(f"{name} {price}\n" for name, price in PRICES.items())

    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    return [body.encode()]
