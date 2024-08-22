import requests
from bs4 import BeautifulSoup

# URL веб-страницы, к которой вы хотите сделать запрос

class Currency:
    AED = "AED"  # Дирхам ОАЭ
    AFN = "AFN"  # Афгани
    ALL = "ALL"  # Лек
    AMD = "AMD"  # Драм
    ANG = "ANG"  # Антильский гульден
    AOA = "AOA"  # Кванза
    ARS = "ARS"  # Аргентинское песо
    AUD = "AUD"  # Австралийский доллар
    AWG = "AWG"  # Арубанский флорин
    AZN = "AZN"  # Азербайджанский манат
    BAM = "BAM"  # Конвертируемая марка
    BBD = "BBD"  # Барбадосский доллар
    BDT = "BDT"  # Бангладешская така
    BGN = "BGN"  # Болгарский лев
    BHD = "BHD"  # Динар Бахрейна
    BIF = "BIF"  # Бурунди франк
    BMD = "BMD"  # Бермудский доллар
    BND = "BND"  # Доллар Брунея
    BOB = "BOB"  # Боливиано
    BRL = "BRL"  # Бразильский реал
    BSD = "BSD"  # Багамский доллар
    BTN = "BTN"  # Нгултрум
    BWP = "BWP"  # Пула
    BYN = "BYN"  # Белорусский рубль
    BZD = "BZD"  # Белизский доллар
    CAD = "CAD"  # Канадский доллар
    CDF = "CDF"  # Конголезский франк
    CHF = "CHF"  # Швейцарский франк
    CLP = "CLP"  # Чилийское песо
    CNY = "CNY"  # Китайский юань
    COP = "COP"  # Колумбийское песо
    CRC = "CRC"  # Костариканский колон
    CUP = "CUP"  # Кубинское песо
    CVE = "CVE"  # Эскудо Кабо-Верде
    CZK = "CZK"  # Чешская крона
    DJF = "DJF"  # Джибутийский франк
    DKK = "DKK"  # Датская крона
    DOP = "DOP"  # Доминиканское песо
    DZD = "DZD"  # Алжирский динар
    EGP = "EGP"  # Египетский фунт
    ERN = "ERN"  # Накафа
    ETB = "ETB"  # Эфиопский бирр
    EUR = "EUR"  # Евро
    FJD = "FJD"  # Доллар Фиджи
    FKP = "FKP"  # Фунт стерлингов Фолклендских островов
    FOK = "FOK"  # Фарерская крона
    GEL = "GEL"  # Грузинский лари
    GHS = "GHS"  # Ганский седи
    GIP = "GIP"  # Гибралтарский фунт
    GMD = "GMD"  # Даласи
    GNF = "GNF"  # Гвинейский франк
    GTQ = "GTQ"  # Гватемальский кетсаль
    GYD = "GYD"  # Гайанский доллар
    HKD = "HKD"  # Гонконгский доллар
    HNL = "HNL"  # Лемпира
    HRK = "HRK"  # Хорватская куна
    HTG = "HTG"  # Гаитянский гурд
    HUF = "HUF"  # Венгерский форинт
    IDR = "IDR"  # Индонезийская рупия
    ILS = "ILS"  # Новый израильский шекель
    IMP = "IMP"  # Фунт стерлингов острова Мэн
    INR = "INR"  # Индийская рупия
    IQD = "IQD"  # Иракский динар
    IRR = "IRR"  # Иранский риал
    ISK = "ISK"  # Исландская крона
    JMD = "JMD"  # Ямайский доллар
    JOD = "JOD"  # Иорданский динар
    JPY = "JPY"  # Японская иена
    KES = "KES"  # Кенийский шиллинг
    KGS = "KGS"  # Киргизский сом
    KHR = "KHR"  # Риель
    KID = "KID"  # Доллар Кука
    KMF = "KMF"  # Франк Коморских островов
    KRW = "KRW"  # Южнокорейская вона
    KWD = "KWD"  # Кувейтский динар
    KYD = "KYD"  # Доллар Каймановых островов
    KZT = "KZT"  # Казахстанский тенге
    LAK = "LAK"  # Лаосский кип
    LBP = "LBP"  # Ливанский фунт
    LKR = "LKR"  # Шри-ланкийская рупия
    LRD = "LRD"  # Либерийский доллар
    LSL = "LSL"  # Лоти
    LYD = "LYD"  # Ливийский динар
    MAD = "MAD"  # Дирхам Марокко
    MDL = "MDL"  # Молдавский лей
    MGA = "MGA"  # Ариари
    MKD = "MKD"  # Македонский денар
    MMK = "MMK"  # Мьянмский кьят
    MNT = "MNT"  # Монгольский тугрик
    MOP = "MOP"  # Патака
    MRU = "MRU"  # Угия
    MUR = "MUR"  # Маврикийская рупия
    MVR = "MVR"  # Мальдивская руфия
    MWK = "MWK"  # Малавийская квача
    MXN = "MXN"  # Мексиканское песо
    MYR = "MYR"  # Малайзийский ринггит
    MZN = "MZN"  # Мозамбикский метикал
    NAD = "NAD"  # Намибийский доллар
    NGN = "NGN"  # Нигерийская найра
    NIO = "NIO"  # Никарагуанская кордоба
    NOK = "NOK"  # Норвежская крона
    NPR = "NPR"  # Непальская рупия
    NZD = "NZD"  # Новозеландский доллар
    OMR = "OMR"  # Оманский риал
    PAB = "PAB"  # Панамское балбоа
    PEN = "PEN"  # Перуанский соль
    PGK = "PGK"  # Кина
    PHP = "PHP"  # Филиппинское песо
    PKR = "PKR"  # Пакистанская рупия
    PLN = "PLN"  # Польский злотый
    PYG = "PYG"  # Парагвайский гуарани
    QAR = "QAR"  # Катартский риал
    RON = "RON"  # Румынский лей
    RSD = "RSD"  # Сербский динар
    RUB = "RUB"  # Российский рубль
    RWF = "RWF"  # Руанде франк
    SAR = "SAR"  # Саудовский риял
    SBD = "SBD"  # Доллар Соломоновых островов
    SCR = "SCR"  # Сейшельская рупия
    SDG = "SDG"  # Суданский фунт
    SEK = "SEK"  # Шведская крона
    SGD = "SGD"  # Сингапурский доллар
    SHP = "SHP"  # Фунт Святой Елены
    SLL = "SLL"  # Леоне
    SOS = "SOS"  # Сомали шиллинг
    SRD = "SRD"  # Суринамский доллар
    SSP = "SSP"  # Южносуданский фунт
    STN = "STN"  # Добра
    SVC = "SVC"  # Сальвадорский колон
    SYP = "SYP"  # Сирийский фунт
    SZL = "SZL"  # Лилангени
    THB = "THB"  # Тайский бат
    TJS = "TJS"  # Таджикский сомони
    TMT = "TMT"  # Туркменский манат
    TND = "TND"  # Тунисский динар
    TOP = "TOP"  # Тонганский паанга
    TRY = "TRY"  # Турецкая лира
    TTD = "TTD"  # Доллар Тринидада и Тобаго
    TWD = "TWD"  # Новый тайваньский доллар
    TZS = "TZS"  # Танзанийский шиллинг
    UAH = "UAH"  # Украинская гривна
    UGX = "UGX"  # Угандийский шиллинг
    USD = "USD"  # Доллар США
    UYU = "UYU"  # Уругвайское песо
    UZS = "UZS"  # Узбекский сум
    VND = "VND"  # Вьетнамский донг
    VUV = "VUV"  # Вату
    WST = "WST"  # Самоанский талла
    XAF = "XAF"  # Франк КФА (Центральная Африка)
    XAG = "XAG"  # Серебро
    XAU = "XAU"  # Золото
    XCD = "XCD"  # Восточно-карибский доллар
    XDR = "XDR"  # СПЗ (специальные права заимствования)
    XOF = "XOF"  # Франк КФА (Западная Африка)
    XPF = "XPF"  # Франк CFP
    YER = "YER"  # Йеменский риал
    ZAR = "ZAR"  # Южноафриканский рэнд
    ZMW = "ZMW"  # Замбийская квача
    ZWL = "ZWL"  # Доллар Зимбабве


def convert(amount:int, _from:str, _to:str):
    '''
    First - Value
    Second - From
    Third - To
    '''
    url = f'https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={_from}&To={_to}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        element = soup.select_one('.sc-e08d6cef-1.fwpLse')

        if element:
            text = element.get_text(strip=True)
            cur = int(text.split('.')[0].replace(',', ''))
            return cur
        else:
            print('err')
    else:
        print('err with response: ', response.status_code)