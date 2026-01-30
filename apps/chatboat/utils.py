KEYWORDS = {
    "products": [
        "chocolate", "chocolates", "dark chocolate", "milk chocolate",
        "white chocolate", "couverture", "truffle", "praline",
        "bar", "bites", "bonbon", "ganache"
    ],
    "nuts": [
        "nut", "nuts", "almond", "almonds", "cashew", "cashews",
        "pistachio", "pistachios", "hazelnut", "walnut", "peanut"
    ],
    "flavors": [
        "cocoa", "cocoa powder", "vanilla", "caramel",
        "sea salt", "orange", "mint", "coffee", "espresso"
    ],
    "availability": [
        "available", "stock", "in stock", "out of stock",
        "fresh", "new arrival"
    ],
    "pricing": [
        "price", "cost", "rate", "expensive", "cheap", "offer",
        "discount", "deal"
    ],
    "ordering": [
        "order", "buy", "purchase", "checkout",
        "delivery", "shipping", "cod", "online"
    ],
    "dietary": [
        "sugar free", "no sugar", "diabetic",
        "vegan", "gluten free", "organic"
    ],
    "gifting": [
        "gift", "gift box", "hamper", "festival",
        "wedding", "birthday", "anniversary"
    ],
    "responses": [
        "yes","no"
    ]
}

GREETINGS = [
    "hi", "hello", "hey", "hai",
    "good morning", "good afternoon", "good evening",
    "greetings", "howdy"
]


def is_chocolate_query(message: str) -> bool:
    msg = message.lower()

    for category, words in KEYWORDS.items():
        for word in words:
            if word in msg:
                return True

    return False


def is_greeting(message: str) -> bool:
    msg = message.lower().strip()

    # Exact match or startswith to avoid false positives
    return any(
        msg == g or msg.startswith(g + " ")
        for g in GREETINGS
    )


def greeting_response() -> str:
    return (
        "Hello and welcome to Choconut. "
        "Are you looking for dark chocolates, gift boxes, or something sugar-free today?"
    )
