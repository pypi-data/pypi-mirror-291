# Useful: https://www.youtube.com/watch?v=kpXU8DM068U
# Maybe buy this? https://sevenstyles.com/p/585-midjourney-prompts-for-christianity-vol3-3779965/
def fresco_painting():
    return 'historical fresco, profile view, a timeless depiction of the Last Supper, communion, disciples sharing bread, rustic room, wooden table, warm lamplight, unity, aged effects, 1st century, Pompeii style, earthy oranges and browns, Classical, Hellenistic Classical, ancient, cracked plaster, worn wood, chipped cup, fellowship, fresco technique, biblical meal, authenticity'

def mary_the_virgin_sculpture():
    return 'ethereal carving, a gentle touch between Santa Maria and Jesucrist the child, serene, smooth, divine, contemplative, motherly connection, tranquil, altar background, soft diffused light, reverence, subtle marble texture, Renaissance, elegant baroque, delicate, smooth alabaster, timeless, in the style of Michelangelo, muted pastels, profile view, neoclassicism, classical contemporary, refined, polished marble, faith, reverence, sculpture, classical, pure elegance'

def oil_painting():
    return 'folk art simplicity, side on view, a peaceful nativity with animals and shepherds, joy, innocence and purity, familial bonding, pastoral landscape, thatched roof stable, warm evening glow, renaissance, angelic visitation, subtle moonlight effects, 16th century, Marc Chagall style, pastel hues, impressionism, roman mural, unrefined, coarse straw, smooth porcelain, magi, infant christ, animals'

def angels():
    return 'mystical renaissance art, angelic hierarchies in celestial dance, wings spread, halos glowing, reverence, divinity, cosmic order, high renaissance, sandro botticelli style, aerial view, humanism, mystical renaissance, celestial, ethereal, feathery, reverence, divinity, order, cosmos'

def tomb():
    return 'mystical fresco painting, wide angle view, empty tomb with light, hope, resurrection and miracle, peaceful garden, stone entrance, morning sunrise, new life, smooth surface, dawn of Christianity, Fra Angelico style, soft earth tones, Byzantine, Futurist, ethereal, stone texture and luminous rays, eternal hope, garden tomb, risen Christ, spiritual awakening'

def wood_cross():
    return 'minimalist cross, a simple wooden cross against a clear sky, faith and redemption, simplicity, cross on a hill, uncluttered, open sky, bright daylight, timeless, George Tooker style, basic color scheme, distant view, Christian symbolism, wooden cross, unadorned, smooth wood, faith, redemption, cross and sky'

def manuscripts():
    return 'impressionistic brushwork, detailed study of angelic figures in illuminated manuscripts, delicate wings, serene faces, golden halos, purity, gentle interaction with human figures, ethereal glow, historical library, soft natural light, sanctity, feathering technique, medieval period, jan van eyck style, pastel blues, medium close up, romanticism, luminous gothic, velvety smooth, textured parchment, subtle ink, grace, devotion, elegance, history, illumination'

def angels_and_daemons():
    return 'expressive portrayal of angels and demons in christian art, serene depiction of the virgin mary, graceful brushstrokes, symbolic elements, surreal imagination, ethereal atmosphere, baroque style, mythical motif, 17th century, dynamic interplay, heavenly glow, celestial backdrop, soft golden lighting, reverence, caravaggio style, celestial blue, low angle view, symbolism, abstract baroque, velvety texture, feathery wings, divine presence, seraphim, cherubim, motherly love, annunciation'

def quiet_monastery():
    return 'minimalist monastic, a quiet monastery courtyard with monks in contemplation, soft candlelight casting long shadows, solitude, monks meditating, serene, stone walls, subtle candlelight, medieval, Carthusian style, muted earth tones, low angle view, monasticism, contemplative quietude, austere, textured stone, contemplation, silence, simple living'

def reading_minimalist():
    return 'minimalist vector style, a saint reading scripture, simple shapes, an open book, contemplation, saint and scripture in dialogue, thoughtful, a sparse study room, even lighting, minimalism, vector art, 17th century, saul bass style, earth tones, high angle view, modernism, vector minimalism, geometric, flat texture, sacred reading, studious saint, divine wisdom, scriptural insight'

def metal_saint_relic():
    return "intricate metalwork, profile view, on a saint's relic, a chirho mesmerizes, legacy, Christ's monogram, metallic intricacy, saint's tomb, reflective sheen, heritage, etched elegance, Byzantine Empire, Benvenuto Cellini style, oxidized metal, renaissance, Christian metallurgy, etched, reflective, chirho symbol, Christ's legacy, metalwork, historical artistry"

def sacred_orthodox_fresco():
    return 'sacred Orthodox fresco, tilt view, Saint Catherine with the wheel, wisdom, St. Catherine standing, broken wheel, scholarly books, palm of martyrdom, intellect, fresco crackling effects, Orthodox period, Hilandar Monastery style, noble blues and reds, Byzantine Art, Serbian Byzantine, wise, jeweled crown, shattered spokes, open scroll, martyrdom, fresco layering, Saint Catherine, erudition'

def candle_minimalist():
    return "spiritual minimalism, a minimalist interpretation of early christian teachings, soulful connection, divine relationship, sacred ambiance, monastic walls, candlelit shadows, byzantine period, in the style of robert ryman, spiritual colors, high angle view, neoplasticism, robert ryman minimalism, pure, soft, gentle, graceful, minimalism, monochrome painting, robert ryman's spirituality, devotion, monastic minimalism"

def baroque_crucifix():
    return 'detailed baroque style, an ornate metalwork crucifix in a grand cathedral, intricate details, grandeur, majestic stance, gilded background, rich chandeliers, historical painting, reverence, da vinci style, gold and bronze, high angle, baroque, ornate golden filigree, artistic mastery, renaissance, elaborate metalwork, detailed, metal craftsmanship, art history, traditional richness'

def crown_of_thorns():
    return 'organic minimalism, a crown of thorns in a desert, sacrifice, isolation, arid desert, barren lands, harsh sunlight, solemnity, empty horizon, rusty browns, ancient times, ana mendieta style, tilt view, land art, organic simplicity, symbolic, coarse sand, twisted metal, sacrifice, desert, organic, minimal, abstract'

def __is_function_local(object):
    import types

    return isinstance(object, types.FunctionType) and object.__module__ == __name__

def random_prompt():
    """
    Returns a random prompts of the existing ones in this file.
    """
    import inspect
    import sys
    import random

    methods = []
    #print([name for name, value in inspect.getmembers(sys.modules[__name__], predicate = (isinstance(object, types.FunctionType) and object.__module__ == __name__))])
    for name, func in inspect.getmembers(sys.modules[__name__], predicate = __is_function_local):
        if name != 'random_prompt' and name != '__is_function_local':
            methods.append(func)

    # We make a dynamic call to that method and return the random prompt
    return random.choice(methods)()