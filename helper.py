def format_coins(coins):
    if coins > 1_000_000:
        return f"{coins / 1_000_000:.2f}M"
    if coins > 1_000:
        return f"{coins / 1_000:.1f}K"
    return f"{coins:.1f}"