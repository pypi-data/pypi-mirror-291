import random

def get_filename(ext="txt"):
    # 200개의 새 이름 목록 정의
    bird_names = [
        "albatross", "avocet", "blackbird", "bluejay", "canary", "cardinal", "chickadee", "crane",
        "cuckoo", "dove", "duck", "eagle", "egret", "falcon", "flamingo", "finch", "goldfinch",
        "goose", "gull", "hawk", "heron", "hummingbird", "ibis", "jay", "kingfisher", "kiwi",
        "kookaburra", "lapwing", "lark", "loon", "magpie", "mallard", "mockingbird", "nightingale",
        "nuthatch", "osprey", "ostrich", "owl", "parrot", "partridge", "peacock", "pelican", "penguin",
        "pheasant", "pigeon", "plover", "ptarmigan", "puffin", "quail", "raven", "redpoll", "robin",
        "rook", "sandpiper", "seagull", "sparrow", "stork", "swallow", "swift", "tern", "thrush",
        "toucan", "vulture", "warbler", "waxwing", "woodpecker", "wren", "bunting", "buzzard", 
        "cormorant", "curlew", "dotterel", "dowitcher", "flicker", "godwit", "goldeneye", "goshawk", 
        "grebe", "grosbeak", "harrier", "hoopoe", "hornbill", "hornedlark", "ibisbill", "jacamar", 
        "jacana", "jackdaw", "junglefowl", "kestrel", "kite", "lapwing", "leafbird", "linnet", 
        "manakin", "meadowlark", "merganser", "murre", "noddynot", "nuthatch", "oriole", "oxpecker", 
        "parula", "petrel", "phoebe", "potoo", "puffleg", "quailfinch", "quailthrush", "quelea", 
        "quetzal", "rail", "redstart", "reeve", "rhea", "rosefinch", "ross'goose", "rufous", "sandgrouse", 
        "scoter", "serin", "shearwater", "shrike", "skua", "skylark", "snipe", "solitaire", "spoonbill", 
        "starling", "stilts", "stonechat", "stork", "stint", "stormpetrel", "sunbird", "swiftlet", 
        "tanager", "tattler", "teal", "tern", "thickknee", "thornbill", "thrush", "titmouse", 
        "toucanet", "towhee", "treepie", "triller", "trogan", "turaco", "turnstone", "verdin", 
        "vireo", "vulture", "wagtail", "weaver", "whimbrel", "whippoorwill", "whistlingduck", 
        "woodcock", "wren", "yellowlegs", "yellowthroat", "zittingcisticola"
    ]
    
    # 새 이름 목록에서 랜덤하게 하나 선택
    random_name = random.choice(bird_names)
    
    # 파일 이름에 확장자를 붙여서 반환
    filename = f"{random_name}.{ext}"
    
    return filename

import random

def get_text():
    # 영어 격언 문장 20개
    english_quotes = [
        "The early bird catches the worm.",
        "A stitch in time saves nine.",
        "Actions speak louder than words.",
        "A journey of a thousand miles begins with a single step.",
        "Don't judge a book by its cover.",
        "Better late than never.",
        "Birds of a feather flock together.",
        "A picture is worth a thousand words.",
        "Every cloud has a silver lining.",
        "Fortune favors the bold.",
        "Honesty is the best policy.",
        "Hope for the best, but prepare for the worst.",
        "If it ain't broke, don't fix it.",
        "Practice makes perfect.",
        "Rome wasn't built in a day.",
        "The pen is mightier than the sword.",
        "When in Rome, do as the Romans do.",
        "Where there's smoke, there's fire.",
        "You can lead a horse to water, but you can't make it drink.",
        "You can't judge a book by its cover."
    ]
    
    # 한글 격언 문장 20개
    korean_quotes = [
        "가는 말이 고와야 오는 말이 곱다.",
        "개천에서 용 난다.",
        "구슬이 서 말이라도 꿰어야 보배다.",
        "금강산도 식후경.",
        "낮말은 새가 듣고 밤말은 쥐가 듣는다.",
        "누워서 떡 먹기.",
        "등잔 밑이 어둡다.",
        "말 한마디로 천 냥 빚 갚는다.",
        "백지장도 맞들면 낫다.",
        "서당 개 삼 년에 풍월을 읊는다.",
        "세 살 버릇 여든까지 간다.",
        "수박 겉 핥기.",
        "아는 것이 힘이다.",
        "없는 자식 귀여운 줄 모른다.",
        "열 번 찍어 안 넘어가는 나무 없다.",
        "오르지 못할 나무는 쳐다보지도 마라.",
        "원숭이도 나무에서 떨어진다.",
        "천 리 길도 한 걸음부터.",
        "하늘이 무너져도 솟아날 구멍이 있다.",
        "호랑이도 제 말 하면 온다."
    ]
    
    # 영어 격언과 한글 격언을 합친 리스트
    all_quotes = english_quotes + korean_quotes
    
    # 리스트에서 랜덤하게 하나 선택하여 반환
    return random.choice(all_quotes)
