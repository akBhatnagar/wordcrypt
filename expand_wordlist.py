#!/usr/bin/env python3
"""Expand the word list with more comprehensive 4-letter words."""

# Read current words
current_words = set()
try:
    with open('valid_words.txt', 'r') as f:
        for line in f:
            word = line.strip().upper()
            if len(word) == 4:
                current_words.add(word)
except FileNotFoundError:
    current_words = set()

# Comprehensive list of 4-letter words with unique letters
additional_words = [
    # Common words that were missing
    "SHIT", "CHIT", "WHIT", "TWIT", "GRIT", "SPIT", "FLIT",
    "QUIT", "SUIT", "FRUIT", "FLUB", "SLUG", "SMUG", "DRUG",
    
    # More A words
    "APEX", "ARCH", "AMID", "AXIS", "ACHY", "AGED", "AIDE", "AIMS", "AIRS",
    "AKIN", "ALPS", "ALTO", "AMEN", "AMID", "AMPS", "ANTE", "ANTI", "APEX",
    "ARMS", "ARTS", "AUNT", "AUTO", "AWRY", "AXES",
    
    # More B words
    "BACH", "BAIL", "BAIT", "BALD", "BALK", "BAND", "BANE", "BANK", "BARE",
    "BARK", "BARN", "BASE", "BASH", "BATH", "BATS", "BAYS", "BEAD", "BEAK",
    "BEAM", "BEAN", "BEAR", "BEAT", "BEDS", "BEEF", "BEEN", "BEER", "BEES",
    "BELL", "BELT", "BEND", "BENT", "BERG", "BEST", "BETA", "BIAS", "BIKE",
    "BILL", "BIND", "BINS", "BIRD", "BITE", "BITS", "BLOW", "BLUE", "BLUR",
    "BOAR", "BOAT", "BODY", "BOIL", "BOLD", "BOLT", "BOMB", "BOND", "BONE",
    "BOOK", "BOOM", "BOOT", "BORE", "BORN", "BOTH", "BOUT", "BOWL", "BOYS",
    "BRAD", "BRAG", "BRAT", "BRED", "BREW", "BRIM", "BROW", "BUCK", "BUDS",
    "BUGS", "BULB", "BULK", "BUMP", "BUNK", "BURN", "BURY", "BUSH", "BUST",
    "BUSY", "BUYS", "BUZZ",
    
    # More C words
    "CABO", "CAGE", "CAKE", "CALM", "CAME", "CAMP", "CANE", "CANT", "CAPE",
    "CAPS", "CARD", "CARE", "CARP", "CARS", "CART", "CASE", "CASH", "CAST",
    "CATS", "CAVE", "CENT", "CHAP", "CHAR", "CHAT", "CHEW", "CHIN", "CHIP",
    "CHIT", "CHOP", "CITE", "CITY", "CLAD", "CLAM", "CLAP", "CLAW", "CLAY",
    "CLIP", "CLUB", "CLUE", "COAL", "COAT", "CODE", "COIN", "COLD", "COLT",
    "COMB", "COME", "CONE", "COPY", "CORD", "CORE", "CORK", "CORN", "COST",
    "COZY", "CRAB", "CRAM", "CREW", "CRIB", "CROP", "CROW", "CUBE", "CUBS",
    "CUED", "CUPS", "CURB", "CURD", "CURE", "CURL", "CURT", "CUTS",
    
    # More D words
    "DAME", "DAMP", "DANE", "DANK", "DARE", "DARK", "DARN", "DART", "DASH",
    "DATA", "DATE", "DAWN", "DAYS", "DAZE", "DEAF", "DEAL", "DEAN", "DEAR",
    "DEBT", "DECK", "DENT", "DENY", "DESK", "DIAL", "DICE", "DIET", "DIME",
    "DINE", "DIPS", "DIRE", "DIRT", "DISC", "DISH", "DISK", "DIVE", "DOCK",
    "DOCS", "DOLE", "DOME", "DONE", "DOPE", "DORK", "DORM", "DOSE", "DOTS",
    "DOTE", "DOVE", "DOWN", "DOZE", "DRAB", "DRAG", "DRAM", "DRAW", "DREW",
    "DROP", "DRUG", "DRUM", "DUAL", "DUBS", "DUCK", "DUEL", "DUES", "DUMB",
    "DUMP", "DUNE", "DUNK", "DUPE", "DUSK", "DUST", "DUTY", "DYES",
    
    # More E words
    "EACH", "EARL", "EARN", "EARS", "EASE", "EAST", "EASY", "EATS", "ECHO",
    "EDIT", "EGGS", "EMIT", "ENVY", "EPIC", "ETCH", "EURO", "EVEN", "EVIL",
    "EXAM", "EXIT", "EYED", "EYES",
    
    # More F words
    "FACE", "FACT", "FADE", "FADS", "FAIL", "FAIR", "FAKE", "FALL", "FAME",
    "FANG", "FARE", "FARM", "FAST", "FATE", "FATS", "FAWN", "FAZE", "FEAR",
    "FEAT", "FELT", "FERN", "FEST", "FEUD", "FILE", "FILM", "FIND", "FINE",
    "FIRE", "FIRM", "FISH", "FIST", "FITS", "FIVE", "FLAG", "FLAK", "FLAP",
    "FLAT", "FLAW", "FLED", "FLEW", "FLIP", "FLIT", "FLOW", "FLUE", "FLUX",
    "FOAL", "FOAM", "FOIL", "FOLD", "FOLK", "FONT", "FORD", "FORK", "FORM",
    "FORT", "FOUR", "FOWL", "FOXY", "FRAT", "FRAY", "FRET", "FROM", "FUEL",
    "FULL", "FUME", "FUND", "FUNK", "FURY", "FUSE", "FUSS", "FUZZ",
    
    # More G words
    "GAIN", "GAIT", "GALE", "GALS", "GAME", "GANG", "GAPS", "GARB", "GATE",
    "GAVE", "GAZE", "GEAR", "GELS", "GEMS", "GENT", "GERM", "GETS", "GIFT",
    "GILD", "GIRL", "GIST", "GIVE", "GLAD", "GLAM", "GLEN", "GLIB", "GLOB",
    "GLOP", "GLOW", "GLUE", "GLUM", "GNAT", "GNAW", "GOAL", "GOAT", "GOBS",
    "GOES", "GOLD", "GOLF", "GONE", "GORY", "GOWN", "GRAB", "GRAD", "GRAM",
    "GRAY", "GREW", "GREY", "GRID", "GRIM", "GRIN", "GRIP", "GRIT", "GROW",
    "GRUB", "GULF", "GULP", "GUMS", "GUNS", "GUST", "GUTS", "GUYS", "GYMS",
    
    # More H words
    "HACK", "HAIL", "HAIR", "HALF", "HALL", "HALO", "HALT", "HAMS", "HAND",
    "HANG", "HARD", "HARE", "HARK", "HARM", "HARP", "HART", "HASH", "HAUL",
    "HAVE", "HAWK", "HAZE", "HAZY", "HEAD", "HEAL", "HEAP", "HEAR", "HEAT",
    "HECK", "HEEL", "HEIR", "HELD", "HELM", "HELP", "HEMP", "HENS", "HERB",
    "HERD", "HERO", "HERS", "HEWN", "HICK", "HIDE", "HIGH", "HIKE", "HILL",
    "HILT", "HIND", "HINT", "HIPS", "HIRE", "HIVE", "HOAX", "HOBS", "HOCK",
    "HOGS", "HOLD", "HOLE", "HOLY", "HOME", "HONE", "HONK", "HOPS", "HOPE",
    "HORN", "HOSE", "HOST", "HOUR", "HOVE", "HUBS", "HUGE", "HUGS", "HULK",
    "HUMS", "HUNG", "HUNK", "HUNT", "HURL", "HURT", "HUSK", "HYMN",
    
    # More I words
    "ICED", "ICON", "IDEA", "IDLE", "IDOL", "INCH", "INFO", "INKS", "INTO",
    "IOTA", "IRON", "ISLE", "ITCH", "ITEM",
    
    # More J words
    "JABS", "JACK", "JADE", "JAGS", "JAIL", "JAMS", "JANE", "JARS", "JAVA",
    "JAWS", "JAZZ", "JEAN", "JEEP", "JERK", "JEST", "JETS", "JINX", "JOBS",
    "JOEY", "JOHN", "JOIN", "JOKE", "JOLT", "JOTS", "JOWL", "JOYS", "JUMP",
    "JUNE", "JUNK", "JURY", "JUST",
    
    # More K words
    "KALE", "KEEP", "KEPT", "KEYS", "KICK", "KIDS", "KILO", "KILT", "KIND",
    "KING", "KITE", "KITS", "KNEE", "KNEW", "KNIT", "KNOB", "KNOT", "KNOW",
    
    # More L words
    "LABS", "LACE", "LACK", "LACY", "LADE", "LADS", "LADY", "LAID", "LAIN",
    "LAIR", "LAKE", "LAMB", "LAME", "LAMP", "LAND", "LANE", "LAPS", "LARD",
    "LARK", "LASH", "LAST", "LATE", "LAUD", "LAWN", "LAWS", "LAYS", "LAZY",
    "LEAD", "LEAF", "LEAK", "LEAN", "LEAP", "LEAS", "LEFT", "LEGS", "LEND",
    "LENS", "LENT", "LEVY", "LIAR", "LICE", "LICK", "LIDS", "LIED", "LIEN",
    "LIES", "LIFE", "LIFT", "LIKE", "LIMB", "LIME", "LIMP", "LINE", "LINK",
    "LINT", "LION", "LIPS", "LISP", "LIST", "LITE", "LIVE", "LOAD", "LOAF",
    "LOAM", "LOAN", "LOBE", "LOBS", "LOCK", "LODE", "LOFT", "LOGO", "LOGS",
    "LOIN", "LONE", "LONG", "LOOM", "LOON", "LOOT", "LOPE", "LORD", "LORE",
    "LOSE", "LOSS", "LOST", "LOTS", "LOUD", "LOUT", "LOVE", "LOWS", "LUCK",
    "LUGE", "LUGS", "LUMP", "LUNG", "LURE", "LURK", "LUSH", "LUST", "LUTE",
    
    # More M words
    "MACE", "MADE", "MAGE", "MAID", "MAIL", "MAIM", "MAIN", "MAKE", "MALE",
    "MALL", "MALT", "MANE", "MANS", "MANY", "MAPS", "MARE", "MARK", "MARS",
    "MART", "MASH", "MASK", "MASS", "MAST", "MATE", "MATH", "MATS", "MAUL",
    "MAZE", "MEAD", "MEAL", "MEAN", "MEAT", "MEEK", "MELD", "MELT", "MEMO",
    "MEND", "MENU", "MEOW", "MESH", "MESS", "MICA", "MICE", "MIKE", "MILD",
    "MILE", "MILK", "MILL", "MIME", "MIND", "MINE", "MING", "MINI", "MINK",
    "MINT", "MINX", "MIRE", "MIST", "MITE", "MITT", "MOAN", "MOAT", "MOBS",
    "MOCK", "MODE", "MOLD", "MOLE", "MOLT", "MONK", "MOOD", "MOPE", "MOPS",
    "MORE", "MORN", "MOST", "MOTH", "MOVE", "MOWN", "MUCH", "MUCK", "MUDS",
    "MULE", "MUMS", "MURK", "MUSE", "MUSH", "MUST", "MUTE", "MUTT", "MYTH",
    
    # More N words
    "NABS", "NAIL", "NAME", "NAPE", "NAPS", "NAVY", "NEAR", "NEAT", "NECK",
    "NEED", "NERD", "NEST", "NETS", "NEWS", "NEWT", "NEXT", "NICE", "NICK",
    "NINE", "NIPS", "NODE", "NODS", "NONE", "NOOK", "NOON", "NOPE", "NORM",
    "NOSE", "NOSY", "NOTE", "NOUN", "NOVA", "NUBS", "NUDE", "NUKE", "NULL",
    "NUMB", "NUNS", "NUTS",
    
    # More O words
    "OAFS", "OAKS", "OARS", "OATH", "OATS", "OBEY", "ODDS", "ODES", "ODOR",
    "OGRE", "OILS", "OILY", "OINK", "OKAY", "OMEN", "OMIT", "ONCE", "ONES",
    "ONLY", "ONTO", "ONUS", "OPAL", "OPEN", "OPTS", "ORAL", "ORCA", "ORCS",
    "ORES", "OURS", "OUST", "OVEN", "OVER", "OWED", "OWES", "OWLS", "OWNS",
    "OXEN",
    
    # More P words
    "PACE", "PACK", "PACT", "PADS", "PAGE", "PAID", "PAIL", "PAIN", "PAIR",
    "PALE", "PALM", "PALS", "PANE", "PANG", "PANS", "PANT", "PARK", "PART",
    "PASS", "PAST", "PATH", "PAVE", "PAWS", "PAYS", "PEAK", "PEAL", "PEAR",
    "PEAS", "PEAT", "PECK", "PEEK", "PEEL", "PEGS", "PELT", "PENS", "PEON",
    "PERK", "PERM", "PERT", "PEST", "PETS", "PEWS", "PICK", "PIES", "PIGS",
    "PIKE", "PILE", "PINE", "PING", "PINK", "PINS", "PINT", "PIPE", "PITS",
    "PITY", "PLAN", "PLAY", "PLEA", "PLED", "PLOD", "PLOP", "PLOT", "PLOW",
    "PLOY", "PLUG", "PLUM", "PLUS", "POEM", "POET", "POKE", "POLE", "POLK",
    "POLL", "POLO", "POMP", "POND", "PONE", "PONY", "PORK", "PORN", "PORT",
    "POSE", "POSH", "POST", "POTS", "POUR", "POUT", "PRAM", "PRAY", "PREY",
    "PRIM", "PROD", "PROM", "PROP", "PROS", "PROW", "PUBS", "PUCK", "PUGS",
    "PULL", "PULP", "PUMA", "PUMP", "PUNK", "PUNT", "PUNY", "PUPS", "PURE",
    "PURL", "PUSH", "PUTS", "PUTT",
    
    # More Q words
    "QUAD", "QUAY", "QUID", "QUIP", "QUIT", "QUIZ",
    
    # More R words
    "RACE", "RACK", "RACY", "RAFT", "RAGE", "RAGS", "RAID", "RAIL", "RAIN",
    "RAKE", "RAMP", "RAMS", "RANG", "RANK", "RANT", "RARE", "RASH", "RASP",
    "RATE", "RATS", "RAVE", "RAYS", "RAZE", "READ", "REAL", "REAM", "REAP",
    "REAR", "REDO", "REED", "REEF", "REEK", "REIN", "RELY", "REND", "RENT",
    "REST", "RIBS", "RICE", "RICH", "RIDE", "RIFE", "RIFT", "RIGS", "RILE",
    "RIME", "RIMS", "RIND", "RING", "RINK", "RIOT", "RIPE", "RISE", "RISK",
    "RITE", "ROAD", "ROAM", "ROAN", "ROAR", "ROBE", "ROCK", "RODE", "RODS",
    "ROIL", "ROLE", "ROLL", "ROMP", "ROOF", "ROOK", "ROOM", "ROOT", "ROPE",
    "ROSE", "ROSY", "ROTE", "ROTS", "ROUT", "ROVE", "ROWS", "RUBE", "RUBS",
    "RUBY", "RUCK", "RUDE", "RUES", "RUFF", "RUGS", "RUIN", "RULE", "RUMP",
    "RUMS", "RUNG", "RUNS", "RUNT", "RUSE", "RUSH", "RUSK", "RUST", "RUTS",
    
    # More S words
    "SACK", "SAFE", "SAGA", "SAGE", "SAGO", "SAID", "SAIL", "SAKE", "SALE",
    "SALT", "SAME", "SAND", "SANE", "SANG", "SANK", "SARI", "SASH", "SAVE",
    "SAWS", "SAYS", "SCAB", "SCAD", "SCAM", "SCAN", "SCAR", "SCAT", "SCOW",
    "SEAL", "SEAM", "SEAR", "SEAS", "SEAT", "SECT", "SEED", "SEEK", "SEEM",
    "SEEN", "SEEP", "SELF", "SELL", "SEMI", "SEND", "SENT", "SERF", "SETS",
    "SEWN", "SEWS", "SHAD", "SHAG", "SHAM", "SHED", "SHIN", "SHIP", "SHIT",
    "SHIV", "SHOE", "SHOP", "SHOT", "SHOW", "SHUN", "SHUT", "SICK", "SIDE",
    "SIFT", "SIGH", "SIGN", "SILK", "SILO", "SILT", "SING", "SINK", "SINS",
    "SIPS", "SIRE", "SITE", "SIZE", "SKEW", "SKID", "SKIM", "SKIN", "SKIP",
    "SKIS", "SKIT", "SLAB", "SLAG", "SLAM", "SLAP", "SLAT", "SLAW", "SLAY",
    "SLED", "SLEW", "SLID", "SLIM", "SLIP", "SLIT", "SLOB", "SLOE", "SLOG",
    "SLOP", "SLOT", "SLOW", "SLUE", "SLUG", "SLUM", "SLUR", "SMOG", "SMUG",
    "SNAG", "SNAP", "SNIP", "SNOB", "SNOT", "SNOW", "SNUB", "SNUG", "SOAK",
    "SOAP", "SOAR", "SOCK", "SODA", "SOFA", "SOFT", "SOIL", "SOLD", "SOLE",
    "SOLO", "SOME", "SONG", "SONS", "SOON", "SOOT", "SORE", "SORT", "SOUL",
    "SOUP", "SOUR", "SOWN", "SOWS", "SPAN", "SPAR", "SPAT", "SPAY", "SPEC",
    "SPED", "SPIN", "SPIT", "SPOT", "SPRY", "SPUD", "SPUN", "SPUR", "STAB",
    "STAG", "STAR", "STAY", "STEM", "STEP", "STEW", "STIR", "STOP", "STOW",
    "STUB", "STUD", "STUN", "SUCH", "SUDS", "SUED", "SUES", "SUIT", "SULK",
    "SUMP", "SUMS", "SUNG", "SUNK", "SUNS", "SURE", "SURF", "SWAB", "SWAG",
    "SWAM", "SWAN", "SWAP", "SWAT", "SWAY", "SWIG", "SWIM", "SWUM",
    
    # More T words
    "TABS", "TACK", "TACO", "TACT", "TAGS", "TAIL", "TAKE", "TALE", "TALK",
    "TALL", "TAME", "TAMP", "TANG", "TANK", "TANS", "TAPE", "TAPS", "TARE",
    "TARN", "TARP", "TARS", "TART", "TASK", "TAUT", "TAXI", "TEAK", "TEAL",
    "TEAM", "TEAR", "TEAS", "TECH", "TEEM", "TEEN", "TELL", "TEMP", "TEND",
    "TENS", "TENT", "TERM", "TERN", "TEST", "TEXT", "THAN", "THAT", "THAW",
    "THEM", "THEN", "THEW", "THEY", "THIN", "THIS", "THOU", "THUD", "THUG",
    "THUS", "TICK", "TIDE", "TIDY", "TIED", "TIER", "TIES", "TIFF", "TILE",
    "TILL", "TILT", "TIME", "TINE", "TING", "TINS", "TINT", "TINY", "TIPS",
    "TIRE", "TOAD", "TOES", "TOFU", "TOGA", "TOIL", "TOLD", "TOLL", "TOMB",
    "TOME", "TONE", "TONG", "TONS", "TOOK", "TOOL", "TOOT", "TOPS", "TORE",
    "TORN", "TOSS", "TOTE", "TOUR", "TOUT", "TOWN", "TOYS", "TRAM", "TRAP",
    "TRAY", "TREE", "TREK", "TREY", "TRIM", "TRIO", "TRIP", "TROD", "TROT",
    "TROY", "TRUE", "TSAR", "TUBA", "TUBE", "TUBS", "TUCK", "TUFT", "TUGS",
    "TUNA", "TUNE", "TUNS", "TURD", "TURF", "TURN", "TUSK", "TUTU", "TWIG",
    "TWIN", "TWIT", "TYPE", "TYPO", "TYRE",
    
    # More U words
    "UGLY", "UNDO", "UNIT", "UNTO", "UPON", "URGE", "URNS", "USED", "USER", "USES",
    
    # More V words
    "VAIN", "VALE", "VAMP", "VANE", "VANS", "VARY", "VASE", "VAST", "VATS",
    "VEAL", "VEIN", "VEND", "VENT", "VERB", "VERY", "VEST", "VETO", "VIBE",
    "VICE", "VIED", "VIES", "VIEW", "VILE", "VINE", "VIOL", "VISE", "VOID",
    "VOLT", "VOTE", "VOWS",
    
    # More W words
    "WADE", "WADS", "WAFT", "WAGE", "WAGS", "WAIL", "WAIT", "WAKE", "WALK",
    "WALL", "WAND", "WANE", "WANT", "WARD", "WARE", "WARM", "WARN", "WARP",
    "WARS", "WART", "WARY", "WASH", "WASP", "WAVE", "WAVY", "WAXY", "WAYS",
    "WEAK", "WEAL", "WEAN", "WEAR", "WEDS", "WEEK", "WEEP", "WEIR", "WELD",
    "WELL", "WELT", "WENT", "WEPT", "WERE", "WEST", "WETS", "WHAM", "WHAT",
    "WHEN", "WHET", "WHEY", "WHIM", "WHIP", "WHIR", "WHIT", "WHIZ", "WHOM",
    "WICK", "WIDE", "WIFE", "WIGS", "WILD", "WILE", "WILL", "WILT", "WILY",
    "WIMP", "WIND", "WINE", "WING", "WINK", "WINS", "WIPE", "WIRE", "WIRY",
    "WISE", "WISH", "WISP", "WITH", "WITS", "WOKE", "WOLF", "WOMB", "WONK",
    "WONT", "WOOD", "WOOF", "WOOL", "WORD", "WORE", "WORK", "WORM", "WORN",
    "WORT", "WRAP", "WREN", "WRIT",
    
    # More X words
    "XRAY",
    
    # More Y words
    "YANK", "YARD", "YARN", "YAWN", "YAWP", "YAWS", "YEAR", "YELL", "YELP",
    "YETI", "YEWS", "YOGA", "YOGI", "YOKE", "YOLK", "YORE", "YOUR", "YOWL",
    "YUAN", "YUCK", "YULE", "YURT",
    
    # More Z words
    "ZANY", "ZEAL", "ZERO", "ZEST", "ZINC", "ZING", "ZION", "ZIPS", "ZITS", "ZONE", "ZOOM", "ZOOS"
]

# Filter to only valid words (4 letters, unique letters, meaningful)
all_words = current_words.copy()

for word in additional_words:
    word = word.upper().strip()
    if len(word) == 4 and len(set(word)) == 4 and word.isalpha():
        all_words.add(word)

# Sort the final list
final_words = sorted(list(all_words))

# Write to new file
with open('valid_words.txt', 'w') as f:
    for word in final_words:
        f.write(word + '\n')

print(f"Original words: {len(current_words)}")
print(f"New words added: {len(final_words) - len(current_words)}")
print(f"Total words: {len(final_words)}")

# Show some examples of new words
new_words = sorted(list(set(final_words) - current_words))
if new_words:
    print(f"\nSample new words: {', '.join(new_words[:20])}")
    if "SHIT" in new_words:
        print("✓ SHIT is now included")
    if "CHIT" in new_words:
        print("✓ CHIT is now included")