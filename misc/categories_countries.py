EU_COUNTRY_CODES = [
    'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR',  # 'EL' - Greece can be by both GR and EL
    'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE'   # code 'EU' for EU
]

ALL_COUNTRY_CODES = [
    "IT",
    "FR",
    "ES",
    "GR",
    "PT",
    "DE",
    "HU",
    "RO",
    "HR",
    "BG",
    "AT",
    "SI",
    "CZ",
    "BE",
    "NL",
    "PL",
    "SK",
    "SE",
    "CY",
    "FI",
    "IE",
    "LT",
    "DK",
    "LV",
    "MT",
    "LU",
    "EE",
    "US",
    "CH",
    "JP",
    "CL",
    "CN",
    "AU",
    "RS",
    "ZA",
    "KR",
    "TR",
    "GB",
    "GE",
    "VN",
    "AL",
    "LI",
    "NZ",
    "CO",
    "SV",
    "BA",
    "PE",
    "CA",
    "ME",
    "MD",
    "ID",
    "MX",
    "TH",
    "NO",
    "EC",
    "GT",
    "KH",
    "MN",
    "CR",
    "IN",
    "HN",
    "IS",
    "UA",
    "AD",
    "AM",
    "BR",
    "CM",
    "CU",
    "DO",
    "GY",
    "LK",
    "PA",
    "PK",
    "RU",
    "ST",
    "VE"
]

CATEGORIES = {
    10000: 'Fruit',
    10001: 'Other',
    10002: 'Coffee',
    10003: "Bread, pastry, cakes, confectionery, biscuits and other baker's wares",
    10004: 'Cheese',
    10005: '1.7 Fresh fish',
    10006: 'Flowers and ornamental plants',
    10007: 'Fruits',
    10008: 'Other '
           'products of '
           'Annex I of '
           'the Treaty ('
           'spices '
           'etc.)',
    10009: 'cocoa',
    10010: 'Plant extract',
    10011: 'Cheeses', 10012: 'Other products of animal origin ('
                                                                     'eggs, honey, various dairy products '
                                                                     'except butter, etc.)',
    10013: 'Other '
                                                                                                    'spirit '
                                                                                                    'drinks',
    10014: 'Spirit drinks', 10015: 'Fruit, vegetables and cereals fresh or processed', 10016: 'Fresh meat (and offal)',
    10017: 'Beverages made from plant extracts', 10018: 'Other products listed in Annex I to the Treaty (spices etc.)',
    10019: 'Fresh fish, molluscs, and crustaceans and products derived therefrom', 10020: 'Grape marc spirit',
    10021: 'Vegetable', 10022: '2. Wine spirit', 10023: '3. Other spirit drinks', 10024: '1. Fruit spirit',
    10025: 'Infusion', 10026: 'Meat', 10027: 'Garlic', 10028: 'Green Tea', 10029: 'Oriental Melon', 10030: 'Rice',
    10031: 'Milk Vetch Root', 10032: 'Beef', 10033: 'Mugwort', 10034: 'Jujube (date)', 10035: 'White Ginseng',
    10036: 'Fresh Ginseng', 10037: 'White or Taekuk Ginseng Products', 10038: 'Taekuk Ginseng', 10039: 'Red Ginseng',
    10040: 'Red Ginseng Products', 10041: 'Black Raspberry', 10042: 'Black Raspberry Wine', 10043: 'Citron',
    10044: 'Apricot', 10045: 'Sap', 10046: 'Red Pepper', 10047: 'Red Pepper Powder', 10048: 'Corni fructus',
    10049: 'Gunsan Chalssalborissal', 10050: 'Fern', 10051: 'White Lotus Tea', 10052: 'Onion', 10053: 'Apple',
    10054: 'Pine-mushroom', 10055: 'Persimmon Dried', 10056: 'Gochujang', 10057: 'Sweet Potato', 10058: 'Fig',
    10059: 'Ulleungdo Miyeokchwi', 10060: 'Ulleungdo Bujigaengi', 10061: 'Aruncus dioicus', 10062: 'Ulleungdo Chamgobi',
    10063: 'Oak-mushroom', 10064: 'Waxy Corn', 10065: 'Chestnut', 10066: 'Pork', 10067: 'Spirits',
    10068: 'Angelica Gigas Nakai Root', 10069: 'Boxthorn', 10070: 'Watermelon', 10071: 'Chinese Cabbage',
    10072: 'Fruit spirit', 10073: 'Liqueurs', 10074: 'Cider Spirit and perry spirit ', 10075: 'Wine spirit',
    10076: 'Meat products and charcuterie', 10077: 'Juniper-flavoured spirit drinks ', 10078: 'Gentian spirit',
    10079: 'Spices', 10080: 'Baked goods', 10081: 'Milling products', 10082: 'Agave spirit drink',
    10083: 'Sugarcane spirit drink', 10084: 'Dasylirion spirit drink', 10085: 'Spirits',
    10086: 'Agricultural products and foodstuffs', 10087: 'Wines', 10088: 'Beers', 10089: 'Wine', 1: 'Wine',
    142: 'Class 1.1 Fresh meat (and offal)', 143: 'Class 1.2. Meat products (cooked, salted, smoked, etc.)',
    144: 'Class 1.3. Cheeses',
    145: 'Class 1.4. Other products of animal origin (eggs, honey, various dairy products except butter, etc.)',
    146: 'Class 1.5. Oils and fats (butter, margarine, oil, etc.)',
    147: 'Class 1.6. Fruit, vegetables and cereals fresh or processed',
    148: 'Class 1.7. Fresh fish, molluscs, and crustaceans and products derived there from',
    149: 'Class 1.8. Other products of Annex I of the Treaty (spices etc.)', 151: 'Class 2.1. Beers',
    152: 'Class 2.2. chocolate and derived products',
    153: "Class 2.3. Bread, pastry, cakes, confectionery, biscuits and other baker's wares",
    154: 'Class 2.4. Beverages made from plant extracts', 155: 'Class 2.5. Pasta', 156: 'Class 2.6. Salt',
    157: 'Class 2.7. Natural gums and resins', 158: 'Class 2.8. Mustard paste', 159: 'Class 2.9. Hay',
    160: 'Class 2.10. Essential oils', 161: 'Class 2.11. Cork',
    162: 'Class 2.12. Cochineal (raw product of animal origin)', 163: 'Class 2.13. Flowers and ornamental plants',
    164: 'Class 2.14. Cotton', 165: 'Class 2.15. Wool', 166: 'Class 2.16. Wicker', 167: 'Class 2.17. Scutched flax',
    168: 'Class 2.18. leather', 169: 'Class 2.19. fur', 170: 'Class 2.20. feather',
    10090: ' Fresh fish, molluscs, and crustaceans and products derived therefrom', 10091: 'Seishu (Sake)', 10092: '',
    10093: 'Spirit drinks', 10094: 'distilled spirits / spirit drinks', 10095: 'fresh and processed vegetable products',
    10096: 'oilseeds', 10097: 'fresh, frozen and processed meats', 10098: 'confectionery and baked products',
    10099: 'beer', 10100: 'hops', 10101: 'cheeses', 10102: 'table and processed olives', 10103: 'oils and animal fats',
    10104: 'spices', 10105: 'natural gums and resins — chewing gum', 10106: 'fresh and processed fruits and nuts',
    10107: 'essential oils', 10108: 'fresh, frozen and processed fish products', 10109: 'dry cured meats',
    10110: 'vinegar', 10111: 'dry-cured meats', 10112: 'cereals', 10113: 'Cider Spirit and perry spirit',
    10114: 'Juniper-flavoured spirit drinks', 10115: 'Fresh and processed fruits and nuts', 10116: 'Cereals',
    10117: 'Nuts', 10118: 'NA', 10119: 'Honey', 10120: 'Spirit drink', 10121: 'Aromatised wine', 10122: 'Food',
    10123: 'Cheeses', 10124: 'Meat products (cooked, salted, smoked, etc.)', 10125: 'Essential oil',
    10126: "Bread, pastry, cakes, confectionary, biscuits and other baker's wares",
    10127: 'Fruit, vegetables and cereal fresh or processed', 10128: 'Oils and fats (butter, margarine, oil, etc.)',
    10129: 'Aromatised Wine', 10130: 'Alcoholic beverage', 10131: 'Agricultural products', 10132: 'Spirit',
    10133: 'Aromatised wines', 10134: 'Agriculture and fishery products and foodstuffs', 10135: 'Spirit drink ',
    10136: 'Other products', 10137: 'Fresh fish, molluscs, and crustaceans and products derived therefrom',
    10138: 'Fruit, vegetables and cereals fresh or processed', 10139: 'Natural gums and resins',
    10140: 'Oils and fats (butter, margarine, oil, etc.) - Pumpkin seed oil',
    10141: 'Other products of Annex I to the Treaty on the Functioning\nof the European Union ( the "Treaty") (spices etc.) - Hops',
    10142: 'Cheese', 10143: 'Fruit, vegetables and cereals fresh or processed - Table olives',
    10144: 'Natural gums and resins - Chewing gum', 10145: 'Oils and fats (butter, margarine, oil, etc.) - Olive oil',
    10146: 'Fruit, vegetables and cereals fresh or processed - Dried cooked plums',
    10147: 'Other products of Annex I to the Treaty (spices etc.) - Sauces',
    10148: 'Meat products (cooked, salted, smoked, etc.) - Hams', 10149: 'Agricultural product [green onion]',
    10150: 'Agricultural product [Japanese white radish (daikon)]',
    10151: 'Agricultural product [buckwheat]  Processed agricultural product [buckwheat flour]',
    10152: 'Agricultural product [celery]', 10153: 'Agricultural product [tomato]',
    10154: 'Processed agricultural product [freeze dried bean curd]', 10155: 'Fresh meat[beef]',
    10156: 'Agricultural product [taro] ',
    10157: 'Marine product [snow crab]  Processed marine product [boiled snow crab]',
    10158: 'Agricultural product [broccoli]', 10159: 'Fresh meat [chicken, offal meat]',
    10160: 'Agricultural product [Japanese persimmon]', 10161: 'Agricultural product [burdock]',
    10162: 'Agricultural product [grapes]', 10163: 'Agricultural product [hosta]',
    10164: 'Agricultural product [soy beans]', 10165: 'Processed agricultural product [pickles]',
    10166: 'Agricultural product [watermelon]', 10167: 'Agricultural product [carrot]', 10168: 'Fresh meat [beef]',
    10169: 'Agricultural product [buckwheat]', 10170: 'Wine',
    10171: 'Processed agricultural product [dried Japanese persimmon]', 191: '1. Rum', 192: '2. Whisky or whiskey',
    193: '3. Grain spirit', 194: '4. Wine spirit', 195: '5. Brandy or Weinbrand',
    196: '6. Grape marc spirit or grape marc', 197: '7. Fruit marc spirit', 198: '8. Raisin spirit or raisin brandy',
    199: '9. Fruit spirit', 200: '10. Cider spirit, perry spirit and cider and perry spirit', 201: '11. Honey spirit',
    202: '12. Hefebrand or lees spirit', 203: '13. Beer spirit', 204: '14. Topinambur or Jerusalem artichoke spirit',
    205: '15. Vodka',
    206: '16. Spirit (supplemented by the name of the fruit, berries or nuts) obtained by maceration and distillation',
    207: '17. Geist (supplemented by the name of the fruit or the raw materials used)', 208: '18. Gentian',
    209: '19. Juniper-flavoured spirit drink', 210: '20. Gin', 211: '21. Distilled gin', 212: '22. London gin',
    213: '23. Caraway-flavoured spirit drink or Kümmel', 214: '24. Akvavit or aquavit',
    215: '25. Aniseed-flavoured spirit drink', 216: '26. Pastis', 217: '27. Pastis de Marseille',
    218: '28. Anis or janeževec', 219: '29. Distilled anis', 220: '30. Bitter-tasting spirit drink or bitter',
    221: '31. Flavoured vodka', 222: '32. Sloe-aromatised spirit drink or pacharán', 223: '33. Liqueur',
    224: '34. Crème de (supplemented by the name of a fruit or other raw material used)', 225: '35. Sloe gin',
    226: '36. Sambuca', 227: '37. Maraschino, marrasquino or maraskino', 228: '38. Nocino or orehovec',
    229: '39. Egg liqueur or advocaat or avocat or advokat', 230: '40. Liqueur with egg', 231: '41. Mistrà',
    232: '42. Väkevä glögi or spritglögg', 233: '43. Berenburg or Beerenburg', 234: '44. Honey nectar or mead nectar',
    235: '45. Spirit drinks', 10172: 'Seishu (Sake)', 10173: 'Agricultural product [sweet potato]', 10174: 'WINE',
    10175: 'SPIRIT', 10176: 'FOOD', 10177: 'AROMATISED_WINE', 10178: 'Pepper',
    10179: 'Other products of animal origin (eggs, honey, various dairy products except butter, etc.)',
    10180: 'Fruit, vegetables and cereals, fresh or processed',
    10181: 'Other products of Annex I to the Treaty (spices, etc.)', 10182: 'Wine',
    10183: 'Fruit, vegetables and cereals, fresh or processed',
    10184: 'Other products of Annex I to the Treaty (spices, etc.)', 10185: 'Agricultural product [squash]',
    10186: 'Agricultural product [eggplant]', 10187: 'Agricultural product [okra]',
    10188: 'Agricultural product [potato]', 10189: 'Marine product [cutlass fish]', 10190: 'Marine product [clam]',
    10191: 'Agricultural product [bean sprouts]', 10192: 'Processed marine product [dried sea cucumber]',
    10193: 'Agricultural product [fig]', 10194: 'Agricultural product [pomelo]', 10195: 'Agricultural product [ginger]',
    10196: 'Agricultural product [Yuzu (citrus)]', 10197: 'Agricultural product [arrowhead]',
    10198: 'Agricultural product [pear]', 10199: 'Agricultural product [Japanese yam]',
    10200: 'Marine product [freshwater clam]', 10201: 'Plants for ornamental purposes [lily]',
    10202: 'Agricultural product [mandarin (citrus)]', 10203: 'Agricultural product [dropwort]',
    10204: 'Agricultural product [pepper] Seasonings [pepper]', 10205: 'Other kinds of liquor',
    10206: 'Aromatised drinks', 188: 'Class 2.21. Aromatised wines', 189: 'Class 2.22. Other alcoholic beverages',
    190: 'Class 2.23. Beeswax', 10207: 'wine', 10208: 'Other', 10209: 'Fruit paste', 10210: 'Olive', 10211: 'Cacao',
    10212: 'Plant product', 10213: 'Peanut', 10214: 'Pear', 10215: 'Black Ginseng Products', 10216: 'Black Ginseng',
    10217: 'Grape', 10218: 'Plum', 10219: 'Omija', 10220: 'Persimmon', 10221: 'Wild-cultivated Ginseng',
    10222: 'Jujube', 10223: 'Pine Nut', 10224: 'Gondre (Korean Thistle) ', 10225: 'Oak Mushroom', 10226: 'Sea Mustard',
    10227: 'Sea Tangle', 10228: 'Laver', 10229: 'Oyster', 10230: 'Wild Grape Wine', 10231: 'Aromatised drinks',
    10232: 'Agricultural product [lotus root]', 10233: 'Agricultural product [Ume\u3000(Japanese apricot)]',
    10234: 'Fresh Meat [beef]', 10235: 'Processed agricultural product [Dried Japanese persimmon]',
    10236: 'Seasonings and Soups [miso paste]', 10237: 'Oils and fats [perilla oil]', 10238: 'Vegetables',
    10239: 'Baked products', 10240: 'Fresh Meat [chicken, offal meat]', 10241: 'Processed livestock product [cheese]',
    10242: 'Agricultural product [Sudachi (citrus)]', 10243: 'Processed agricultural product [tea leaves]',
    10244: 'Barley', 10245: 'Golden rod', 10246: 'Aster', 10247: 'Fish [coho salmon]', 10248: 'Gondre (Korean Thistle)',
    10249: 'Agricultural product [taro]', 10250: 'Agricultural product [Ume (Japanese apricot)]',
    10251: 'Other kinds of liquor', 10252: 'Spirit distilled from wine', 10253: 'N/A', 10254: 'Fresh fish',
    10255: 'Aromatised drinks', 10256: 'Spirits', 10257: 'Vinegar', 10258: 'Wines ',
    10259: 'Fresh and processed vegetable products', 10260: 'Fresh, frozen and processed meats', 10261: 'Spices',
    10262: 'Oils and animals fats', 10263: 'Oil and animal fats', 10264: 'Beer',
    10265: 'Confecionery and baked products', 10266: 'Butter', 10267: 'Fresh, frozen and processed meat products',
    10268: 'Cereals', 10269: 'Fresh , frozen and proceesed meats', 10270: 'Essential oils',
    10271: 'Fresh and processed meats', 10272: 'Fresh frozen and procesed meat',
    10273: 'Confectionary and baked products', 10274: 'Fresh and processed vegetable products ',
    10275: 'Confectionery and baked products', 10276: 'Fresh and processed fruit and nuts', 10277: 'Honey',
    10278: 'Oils and animal fats', 10279: 'Mustard paste', 10280: 'spirits',
    10281: 'Fresh and processed fruits and nuts', 10282: 'Confectionery  and baked products', 10283: 'Hops',
    10284: 'Tabe and processed olives', 10285: 'Table and processed olives', 10286: 'Gums and natural resins',
    10287: 'wines', 10288: 'Other spirit drinks', 10289: 'Fruit spirit', 10290: 'Liqueurs', 10291: 'Grape marc spirit',
    10292: 'Cider Spirit and perry spirit', 10293: 'Wine spirit', 10294: 'Juniper-flavoured spirit drinks',
    10295: 'Gentian spirit', 10296: 'Spirit distilled from wine', 10297: 'Agave spirit drink',
    10298: 'Dasylirion spirit drink', 10299: 'Sugarcane spirit drink', 10300: 'Spirit drinks'
}