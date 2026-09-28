from urllib.parse import quote_plus


def search_url(
    platform: str,
    query: str,
) -> str:

    return (
        "https://www.google.com/search?q="
        + quote_plus(
            platform + " " + query
        )
    )


def _item(
    category,
    name,
    description,
    price,
    platform,
    quantity,
    reason,
    currency,
):

    return {
        "category": category,
        "name": name,
        "description": description,
        "estimated_price": price,
        "currency": currency,
        "platform": platform,
        "search_url": search_url(
            platform,
            name,
        ),
        "quantity": quantity,
        "reason": reason,
    }


def home_fallback(data):

    budget = data["budget"]
    currency = data["currency"]

    items = (
        data.get("items")
        or [
            {
                "name": "LED ceiling light",
                "quantity": 2,
            },
            {
                "name": "side table",
                "quantity": 1,
            },
        ]
    )

    per = max(
        1,
        budget / max(
            1,
            len(items),
        ),
    )

    recs = []

    for item in items:

        qty = item["quantity"]

        unit = min(
            per / max(qty, 1),
            budget
            / max(
                qty * len(items),
                1,
            ),
        )

        unit = max(
            800,
            round(unit / 100) * 100,
        )

        platform = (
            "IKEA"
            if "IKEA"
            in data.get(
                "preferred_platforms",
                [],
            )
            else "Amazon"
        )

        recs.append(
            _item(
                "Home",
                item["name"],
                (
                    f"{data.get('style', 'Modern')} "
                    "option for "
                    + ", ".join(
                        data.get(
                            "rooms",
                            [],
                        )
                    )
                    + "."
                ),
                unit,
                platform,
                qty,
                (
                    "Fits the requested style "
                    "and budget planning context."
                ),
                currency,
            )
        )

    total = sum(
        x["estimated_price"]
        * x["quantity"]
        for x in recs
    )

    return {
        "title": "Starter Home Interior Plan",
        "summary": (
            "A conservative starter plan "
            "generated locally because live "
            "AI/product data was not available."
        ),
        "estimated_total": total,
        "budget_status": (
            "within budget"
            if total <= budget
            else "over budget"
        ),
        "allocations": {
            "furniture": round(
                total * 0.45,
                2,
            ),
            "lighting": round(
                total * 0.20,
                2,
            ),
            "decor": round(
                total * 0.20,
                2,
            ),
            "contingency": round(
                total * 0.15,
                2,
            ),
        },
        "recommendations": recs,
        "tips": [
            "Compare at least two sellers before purchasing.",
            "Keep a 10-15% contingency for delivery and installation.",
        ],
    }


def party_fallback(data):

    budget = data["budget"]
    currency = data["currency"]
    guests = data["guests"]

    food = round(
        budget * 0.45,
        2,
    )

    decor = round(
        budget * 0.15,
        2,
    )

    venue = (
        round(
            budget * 0.20,
            2,
        )
        if str(
            data["venue"]
        ).lower()
        != "home"
        else 0
    )

    entertainment = round(
        budget * 0.10,
        2,
    )

    contingency = round(
        budget
        - food
        - decor
        - venue
        - entertainment,
        2,
    )

    recs = [
        _item(
            "Food",
            (
                f"{data['event_type']} "
                f"catering for {guests} guests"
            ),
            (
                f"{data['food_preferences']} "
                "menu planning."
            ),
            food,
            "Zomato",
            1,
            (
                "Largest allocation because "
                "food scales with guest count."
            ),
            currency,
        ),
        _item(
            "Decoration",
            "Balloon and backdrop decoration",
            "Simple theme decoration package.",
            decor,
            "Amazon",
            1,
            "High visual impact at moderate cost.",
            currency,
        ),
        _item(
            "Entertainment",
            "Bluetooth speaker and playlist setup",
            "DIY entertainment setup.",
            entertainment,
            "Amazon",
            1,
            "Keeps entertainment flexible.",
            currency,
        ),
    ]

    if venue:

        recs.append(
            _item(
                "Venue",
                (
                    f"Small event venue in "
                    f"{data.get('city') or 'your city'}"
                ),
                "Search for a venue within the allocation.",
                venue,
                "OYO",
                1,
                (
                    "Reserved portion of the "
                    "budget for venue cost."
                ),
                currency,
            )
        )

    return {
        "title": (
            f"{data['event_type']} Party Budget"
        ),
        "summary": (
            f"A simple plan for {guests} guests."
        ),
        "estimated_total": sum(
            x["estimated_price"]
            for x in recs
        ),
        "budget_status": "within budget",
        "allocations": {
            "food": food,
            "decoration": decor,
            "venue": venue,
            "entertainment": entertainment,
            "contingency": contingency,
        },
        "recommendations": recs,
        "tips": [
            "Ask vendors for package pricing.",
            "Keep guest count and menu fixed before committing to a venue.",
        ],
    }


def jewelry_fallback(
    data,
    image_supplied=False,
):

    budget = data["budget"]
    currency = data["currency"]

    options = [
        (
            "Earrings",
            "Classic statement earrings",
            0.22,
            "Amazon",
        ),
        (
            "Necklace",
            "Minimal pendant necklace",
            0.28,
            "Flipkart",
        ),
        (
            "Bangles",
            "Elegant bangle set",
            0.18,
            "Amazon",
        ),
        (
            "Ring",
            "Minimal occasion ring",
            0.14,
            "Flipkart",
        ),
    ]

    recs = []

    for (
        category,
        name,
        share,
        platform,
    ) in options:

        recs.append(
            _item(
                category,
                name,
                (
                    f"{data['style']} style "
                    f"for {data['occasion']}."
                ),
                round(
                    budget * share,
                    2,
                ),
                platform,
                1,
                (
                    "Selected as a flexible style "
                    "match within the stated budget."
                ),
                currency,
            )
        )

    return {
        "title": (
            f"{data['occasion']} Jewelry Plan"
        ),
        "summary": (
            "A style-first jewelry shortlist "
            "generated locally."
            + (
                " The uploaded image can be "
                "reviewed by Gemini when configured."
                if image_supplied
                else ""
            )
        ),
        "estimated_total": round(
            sum(
                x["estimated_price"]
                for x in recs
            ),
            2,
        ),
        "budget_status": "within budget",
        "allocations": {
            "earrings": round(
                budget * 0.22,
                2,
            ),
            "necklace": round(
                budget * 0.28,
                2,
            ),
            "bangles": round(
                budget * 0.18,
                2,
            ),
            "ring": round(
                budget * 0.14,
                2,
            ),
            "reserve": round(
                budget * 0.18,
                2,
            ),
        },
        "recommendations": recs,
        "tips": [
            "Match metal tone to the outfit and other accessories.",
            "Keep some budget unspent for delivery or alterations.",
        ],
    }
    