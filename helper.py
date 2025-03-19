def format_coins(coins):
    if coins > 1_000_000:
        return f"{coins / 1_000_000:.2f}M"
    if coins > 1_000:
        return f"{coins / 1_000:.1f}K"
    return f"{coins:.1f}"

def format_wood_type(wood):
    EMOJIS = {
        "ENCHANTED_ACACIA_LOG": 1350908708447719566,
        "ENCHANTED_BIRCH_LOG": 1350908710343544935,
        "ENCHANTED_DARK_OAK_LOG": 1350908712436629554,
        "ENCHANTED_JUNGLE_LOG": 1350908714747695285,
        "ENCHANTED_OAK_LOG": 1350908717469667328,
        "ENCHANTED_SPRUCE_LOG": 1350908719654768681,
        "ENCHANTED_DIAMOND_BLOCK": 1352011357997764668,
        "ENCHANTED_COBBLESTONE": 1352012686141161532
    }
    return f"<:{wood}:{EMOJIS[wood]}> {wood.title().replace('_', ' ')}"