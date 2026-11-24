#!/usr/bin/env python3
"""Generate the kupit-kvartiru-v-tbilisi.com draft site into ../site/."""
import json, os, shutil, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
DOMAIN = 'https://kupit-kvartiru-v-tbilisi.com'
UPDATED = 'ноябрь 2026'
ROBOTS = '<meta name="robots" content="noindex, nofollow">'  # remove at launch

def brik(content):
    return ('https://real-estate-georgia.com/?utm_source=kupit-kvartiru-v-tbilisi'
            f'&amp;utm_medium=referral&amp;utm_campaign=minisite&amp;utm_content={content}')

SRC = {
 'ii_2026': ('Цены и доходность в Тбилиси и Батуми, 2026 (International Investment: TBC Capital, Galt &amp; Taggart, Colliers, Geostat)',
             'https://internationalinvestment.biz/en/real-estate/8910-georgia-real-estate-2026-prices-and-yields-in-tbilisi-and-batumi.html'),
 'geostat_q3': ('Geostat: цены на жильё в Тбилиси по районам, III квартал 2026 (Georgia Today)', 'https://georgiatoday.ge/?p=115443'),
 'tbc_sep': ('TBC Capital: средняя цена в Тбилиси в сентябре 2026 (International Investment)',
             'https://internationalinvestment.biz/en/real-estate/9034-tbilisi-apartment-sale-prices-september-tbc-capital.html'),
 'gt_sep': ('Galt &amp; Taggart: районы Тбилиси, сентябрь 2026 (International Investment)',
            'https://internationalinvestment.biz/en/real-estate/9088-tbilisi-districts-property-prices-and-sales.html'),
 'tbc_2025': ('TBC Capital: итоги 2025 года и прогноз на 2026 (Georgia Today)', 'https://georgiatoday.ge/georgias-real-estate-market-grows-6-in-2025/'),
 'gt_2025': ('Galt &amp; Taggart: рост цен на первичном рынке Тбилиси 2023–2025 (GBC)',
             'https://www.gbc.ge/en/news/Economics-news/galttaggart-predicts-single-digit-growth-in-apartment-prices-in-tbilisi-in-2026'),
 'gt_sales': ('Galt &amp; Taggart: 42 388 сделок в Тбилиси в 2025 году (BM.ge)', 'https://bm.ge/en/news/over-42000-apartments-sold-in-tbilisi-in-2025'),
 'rent_apr': ('Galt &amp; Taggart: аренда по районам, апрель 2026 (BM.ge)',
              'https://bm.ge/en/news/tbilisi-apartment-rents-up-52-in-april-vake-remains-most-expensive-district'),
 'rent_guide': ('Сколько стоит аренда в Тбилиси по районам (Georgia Today)', 'https://georgiatoday.ge/what-it-costs-to-rent-an-apartment-in-tbilisi/'),
 'myhome': ('MyHome.ge: цена м² в Тбилиси и состояние квартиры', 'https://www.myhome.ge/en/blog/what-does-1-sqm-cost-in-tbilisi-by-neighborhood/'),
 'khrushchevka': ('Chai Khana: хрущёвки и брежневки в Сабуртало', 'https://chaikhana.media/en/stories/651/mishenebis-perspeqtivit'),
 'dilapidated': ('Chai Khana: программа замены аварийных домов в Тбилиси', 'https://chaikhana.media/en/stories/1576/lekh-kachinskis-9-nomeri-safrtkhis-shemtsveli-shenobebis-bedi-tbilisshi'),
 'oldtbilisi': ('Georgia Today: программа замены аварийных домов распространена на Старый Тбилиси', 'https://georgiatoday.ge/?p=100036'),
 'civil': ('Civil.ge: проект Eagle Hills в Крцаниси и Гонио', 'https://civil.ge/archives/711355'),
 'madloba_buy': ('Madloba: покупка жилья иностранцем в Грузии', 'https://madloba.info/en/faq/housing/buying-property-in-georgia-as-a-foreigner/'),
 'madloba_poa': ('Madloba: доверенность для сделки в Грузии', 'https://madloba.info/en/blog/laws-of-georgia/doverennost-ne-grazhdaninu-gruzii'),
 'madloba_rent': ('Madloba: налог на сдачу квартиры (ст. 81 Налогового кодекса)', 'https://madloba.info/en/faq/work-business-taxes/tax-on-renting-out-an-apartment-in-georgia/'),
 'madloba_tax': ('Madloba: налоги в Грузии, статус малого бизнеса', 'https://madloba.info/faq/work-business-taxes/taxes-and-vat-in-georgia/'),
 'madloba_rp': ('Madloba: сроки рассмотрения ВНЖ', 'https://madloba.info/en/faq/residence-and-citizenship/check-residence-permit-status-georgia/'),
 'chambers': ('Chambers Real Estate 2026: Georgia', 'https://practiceguides.chambers.com/practice-guides/real-estate-2026/georgia'),
 'eig': ('EIG Law: порог ВНЖ через недвижимость с 1 марта 2026',
         'https://eiglaw.com/georgia-to-increase-real-estate-investment-threshold-for-residence-permits-effective-march-1-2026/'),
 'visaatlas': ('VisaAtlas: краткосрочный ВНЖ для владельцев недвижимости', 'https://visaatlas.org/visas/georgia/short-term-residence-real-estate'),
 'sda': ('Агентство развития государственных услуг: виды на жительство', 'https://sda.gov.ge/en/products/migration-residence-permits/'),
 'andersen': ('Andersen Georgia: налог при продаже жилья', 'https://ge.andersen.com/georgia-property-tax/'),
 'sova': ('SOVA: порог налога на имущество повышен до 100 000 лари',
          'https://sovanews.tv/en/2026/09/30/georgian-parliament-approves-abolition-of-40000-gel-property-tax-threshold/amp/'),
 'gpg_buy': ('Global Property Guide: расходы на сделку в Грузии', 'https://www.globalpropertyguide.com/asia/georgia/buying-guide'),
 'korter_frames': ('Korter: чёрный, белый и зелёный каркас', 'https://korter.ge/en/new-projects-tbilisi-black-frame'),
 'cappuccino': ('Cappuccino Estate: покупка новостройки в Тбилиси', 'https://cappuccino-estate.com/articles/tobuy_newdevelopment_guide_tbilisi_eng'),
 'safebuy': ('SafeBuy: проверка новостроек по реестру', 'https://safebuy.ge/properties/new-developments'),
 'napr': ('Национальное агентство публичного реестра', 'https://napr.gov.ge'),
 'rs': ('Служба доходов Грузии', 'https://www.rs.ge'),
}

def sources(keys):
    items = ''.join(f'<li><a href="{SRC[k][1]}">{SRC[k][0]}</a></li>' for k in keys)
    return (f'<section class="band" style="padding-top:0"><div class="wrap"><h2 style="font-size:20px">Источники</h2><ul class="sources">{items}</ul>'
            '<p class="sub">У каждой цифры указаны период и исследование. TBC Capital, Galt &amp; Taggart и Geostat считают цены по-разному, поэтому сравнивайте цифры только внутри одного источника.</p></div></section>')

def fmt(n):
    return f'{n:,}'.replace(',', ' ')

# Geostat median asking price, new developments, Q3 2026, GEL per m2 (all 10 districts, one series)
GEO = [('Мтацминда', 7004), ('Ваке', 6046), ('Крцаниси', 4635), ('Сабуртало', 4444), ('Дидубе', 4168),
       ('Чугурети', 4121), ('Исани', 4032), ('Надзаладеви', 3932), ('Глдани', 3830), ('Самгори', 3657)]

# district pages: TBC Capital July 2026 new-build prices ($/m2, white frame) where published
D = [
 dict(slug='vake', name='Ваке', usd=3180, cls='премиум', rent=15.1, sales='884', short='зелёный престижный район, самые высокие цены TBC'),
 dict(slug='mtacminda-sololaki', name='Мтацминда и Сололаки', usd=None, geo=7004, cls='премиум', rent=13.0, sales='441', short='исторический центр под горой Мтацминда'),
 dict(slug='saburtalo', name='Сабуртало', usd=1732, cls='бизнес', rent=11.4, sales='4 926', short='большой жилой район, много сделок'),
 dict(slug='krcanisi', name='Крцаниси', usd=1671, cls='бизнес', rent=None, sales=None, short='спокойный зелёный район на юге'),
 dict(slug='didube', name='Дидубе', usd=1425, cls='бизнес', rent=None, sales=None, short='средний сегмент у центра'),
 dict(slug='isani', name='Исани', usd=1407, cls='бизнес', rent=None, sales=None, short='левый берег, средний сегмент'),
 dict(slug='didi-digomi', name='Диди Дигоми', usd=1148, cls='доступное', rent=8.7, sales='5 740', short='больше всего сделок в городе'),
 dict(slug='gldani', name='Глдани', usd=1146, cls='доступное', rent=8.6, sales=None, short='доступный район на севере'),
]

NAV = [('', 'Главная'), ('rajony/', 'Районы'), ('ceny/', 'Цены'), ('kak-kupit/', 'Как купить'),
       ('staryj-fond-ili-novostrojka/', 'Старый фонд или новостройка'), ('rashody-i-nalogi/', 'Налоги'),
       ('vnzh-za-nedvizhimost/', 'ВНЖ'), ('faq/', 'Вопросы')]

def link(depth, target):
    return '../' * depth + target + 'index.html'

def a(target, text, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="@/{target}index.html">{text}</a>'

def page(path, title, desc, crumbs, body, h1=None, lede=None, srcs=None, head_extra=''):
    depth = path.count('/')
    L = lambda t: link(depth, t)
    nav = ''.join(
        f'<a href="{L(t)}"' + (' aria-current="page"' if (t == path or (t and path.startswith(t))) and (t or not path) else '') + f'>{n}</a>'
        for t, n in NAV)
    crumb_html = ''
    ld_items = [{'@type': 'ListItem', 'position': 1, 'name': 'Главная', 'item': DOMAIN + '/'}]
    if crumbs:
        parts = [f'<a href="{L("")}">Главная</a>']
        for i, (t, n) in enumerate(crumbs):
            ld_items.append({'@type': 'ListItem', 'position': i + 2, 'name': n, 'item': f'{DOMAIN}/{t}'})
            parts.append(f'<a href="{L(t)}">{n}</a>' if t != path else f'<span aria-current="page">{n}</span>')
        crumb_html = '<nav class="crumbs" aria-label="Навигация">' + ' / '.join(parts) + '</nav>'
    ld = json.dumps([
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': ld_items},
        {'@context': 'https://schema.org', '@type': 'Article', 'headline': h1 or title, 'inLanguage': 'ru',
         'dateModified': '2026-11-24', 'publisher': {'@type': 'Organization', 'name': 'Brik', 'url': 'https://real-estate-georgia.com'}}
    ], ensure_ascii=False)
    head_band = ''
    if h1:
        head_band = (f'<section class="band pagehead"><div class="wrap">{crumb_html}<h1>{h1}</h1>'
                     + (f'<p class="lede">{lede}</p>' if lede else '') + f'<p class="updated">Обновлено: {UPDATED}</p></div></section>')
    foot_src = sources(srcs) if srcs else ''
    up = '../' * depth
    doc = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
{ROBOTS}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{DOMAIN}/{path}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&amp;family=Golos+Text:wght@400;600;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/site.css">
<script type="application/ld+json">{ld}</script>{head_extra}
</head>
<body>
<div class="draft">Черновик сайта для согласования. Примеры объявлений демонстрационные, остальные данные — с источниками.</div>
<header class="top"><div class="wrap"><a class="logo" href="{L("")}">Тбилиси<span>·</span>квартиры</a><nav class="scroll" aria-label="Разделы">{nav}</nav></div></header>
<main>
{head_band}
{body.replace('@/', up)}
{foot_src}
</main>
<footer class="band"><div class="wrap"><div class="cols">
<div><p><b>Тбилиси·квартиры</b> — справочник для тех, кто покупает жильё в столице Грузии. Проект <a href="{brik('footer')}">Brik</a>.</p><p>Это справочная информация, а не юридическая или налоговая консультация.</p></div>
<div><p><b>Районы</b></p><ul>{''.join(f'<li><a href="{L("rajony/" + d["slug"] + "/")}">{d["name"]}</a></li>' for d in D)}</ul></div>
<div><p><b>Покупка</b></p><ul><li><a href="{L("kak-kupit/")}">Как купить</a></li><li><a href="{L("staryj-fond-ili-novostrojka/")}">Старый фонд или новостройка</a></li><li><a href="{L("dlya-zhizni-ili-sdachi/")}">Для жизни или сдачи</a></li><li><a href="{L("rashody-i-nalogi/")}">Расходы и налоги</a></li><li><a href="{L("vnzh-za-nedvizhimost/")}">ВНЖ</a></li><li><a href="{L("ceny/")}">Цены</a></li></ul></div>
<div><p><b>Проект</b></p><ul><li><a href="{L("o-nas/")}">О нас</a></li><li><a href="{L("kontakty/")}">Контакты</a></li><li><a href="{L("privacy/")}">Конфиденциальность</a></li><li><a href="{L("faq/")}">Вопросы и ответы</a></li></ul></div>
</div></div></footer>
<script src="{up}assets/site.js"></script>
</body>
</html>
'''
    dest = os.path.join(OUT, path, 'index.html')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(doc)

def cta(content, title='Квартиры в Тбилиси на Brik', text='Объявления застройщиков, агентств и собственников с фильтрами по району, цене и площади.'):
    return (f'<section class="band" style="padding-top:0"><div class="wrap"><div class="cta"><div><h2>{title}</h2><p>{text}</p></div>'
            f'<a class="btn" href="{brik(content)}">Открыть каталог</a></div></div></section>')

def related(items):
    return '<div class="related">' + ''.join(a(t, n) for t, n in items) + '</div>'

def geo_rows(highlight=None):
    mx = 7400
    slug_of = {'Мтацминда': 'mtacminda-sololaki', 'Ваке': 'vake', 'Крцаниси': 'krcanisi', 'Сабуртало': 'saburtalo',
               'Дидубе': 'didube', 'Исани': 'isani', 'Глдани': 'gldani'}
    out = []
    for name, v in GEO:
        slug = slug_of.get(name)
        cls = 'row hl' if slug and slug == highlight else 'row'
        inner = (f'<div class="nm"><b>{name}</b><span>медиана предложения в новостройках</span></div>'
                 f'<div class="bar" aria-hidden="true"><i data-w="{v / mx * 100:.1f}"></i></div><div class="v">{fmt(v)} ₾/м²</div>')
        out.append(f'<a class="{cls}" href="@/rajony/{slug}/index.html">{inner}</a>' if slug else f'<div class="{cls}">{inner}</div>')
    return '<div class="rows">' + ''.join(out) + '</div>'

def lead_form(extra=''):
    opts = ''.join(f'<option>{d["name"]}</option>' for d in D)
    return f'''<form data-draft novalidate>
  <label>Как к вам обращаться<input name="name" autocomplete="name" required></label>
  <label>Telegram, WhatsApp или e-mail<input name="contact" required></label>
  <label>Бюджет<select name="budget"><option>до $70 000</option><option>$70 000–150 000</option><option>$150 000–300 000</option><option>больше $300 000</option></select></label>
  <label>Район<select name="area"><option>Ещё выбираю</option>{opts}</select></label>
  <label>Цель<select name="goal"><option>Для жизни</option><option>Для сдачи</option><option>Для ВНЖ</option></select></label>{extra}
  <button class="btn" type="submit">Получить подборку</button>
  <div class="ok" role="status">Черновик: форма ещё не подключена, заявка не отправлена.</div>
</form>'''

SCENE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scene.svg'), encoding='utf-8').read()

# ======================= PAGES =======================
def home():
    sample = [('Новостройка, белый каркас', 'Сабуртало', '2 комнаты', 58, 1750), ('Новостройка, с ремонтом', 'Ваке', '2 комнаты', 72, 3200),
              ('Старый фонд, после ремонта', 'Сололаки', '3 комнаты', 85, 2100), ('Новостройка, чёрный каркас', 'Диди Дигоми', '1 комната', 42, 1100),
              ('Строящийся дом', 'Крцаниси', '2 комнаты', 64, 1650), ('Вторичный рынок', 'Дидубе', '2 комнаты', 55, 1300)]
    hues = ['#f3e4e8', '#efe6dc', '#e9e3ef', '#f6ecd9', '#e6ece4', '#f1e1dc']
    def card(i, c):
        t, dn, r, ar, pm = c
        wins = ''.join(f'<rect x="{50 + x * 16}" y="{34 + y * 16}" width="8" height="10" rx="4"/>' for y in range(4) for x in range(4))
        return (f'<article class="card"><svg class="ph" viewBox="0 0 160 100" aria-hidden="true"><rect width="160" height="100" fill="{hues[i]}"/>'
                f'<rect x="42" y="24" width="76" height="76" fill="#fff"/><path d="M36 26 L80 6 L124 26Z" fill="#b5523b" opacity=".8"/><g fill="#8a2a47" opacity=".55">{wins}</g></svg>'
                f'<div class="bd"><span class="tag">Пример</span><div class="pr">${fmt(round(ar * pm / 1000) * 1000)}</div>'
                f'<div class="meta">{r}, {ar} м² · {dn}</div><div class="meta">{t}</div></div></article>')
    body = f'''
<section class="hero band"><div class="wrap">
  <div>
    <h1>Купить квартиру в Тбилиси: районы, цены и порядок сделки</h1>
    <p class="lede">Средняя цена квартиры в Тбилиси в сентябре 2026 года — $1 373 за м² по данным TBC Capital. Разница между районами почти трёхкратная: от доступных Глдани и Диди Дигоми до премиальных Ваке и Мтацминды.</p>
    <div class="ctas"><a class="btn" href="#listings">Квартиры в продаже</a>{a("rajony/", "Сравнить районы", "btn ghost")}</div>
  </div>
  {SCENE}
</div></section>
<section class="facts band" aria-label="Тбилиси в цифрах"><div class="wrap">
  <div class="fact"><b>$1 373</b><span>средняя цена м², все сделки</span><small>сентябрь 2026, TBC Capital</small></div>
  <div class="fact"><b>4 245</b><span>сделок с квартирами за месяц, +6,4% за год</span><small>сентябрь 2026, Colliers</small></div>
  <div class="fact"><b>8,3%</b><span>валовая доходность аренды</span><small>август 2026, TBC Capital</small></div>
  <div class="fact"><b>12%</b><span>сделок — с иностранными покупателями</span><small>сентябрь 2026, Colliers</small></div>
</div></section>
<section class="band" id="listings"><div class="wrap">
  <h2>Квартиры в Тбилиси сейчас в продаже</h2>
  <p>Подборка из каталога Brik. Все объявления с фильтрами по району и бюджету — на основном сайте.</p>
  <p class="sub">Демонстрационные карточки: после подключения здесь будут 6 актуальных объявлений.</p>
  <div class="grid">{''.join(card(i, c) for i, c in enumerate(sample))}</div>
  <a class="btn" href="{brik('home-listings')}">Все квартиры в Тбилиси на Brik</a>
</div></section>
<section class="band alt"><div class="wrap">
  <h2>Где дороже всего: медианная цена по районам</h2>
  <p>Медианная цена предложения в новостройках, III квартал 2026, Geostat. В Мтацминде и Ваке метр стоит больше 6 000 лари, в Глдани и Самгори — меньше 4 000.</p>
  {geo_rows()}
  <p class="sub" style="margin-top:14px">{a("rajony/", "Все районы и их особенности")} · {a("ceny/", "Цены в долларах и динамика")}</p>
</div></section>
<section class="band"><div class="wrap two">
  <div><h2>Старый фонд или новостройка</h2><p>Большая часть сделок в Тбилиси — вторичный рынок, где много советских панельных домов. Новостройки продают в чёрном, белом или зелёном каркасе. От выбора зависят бюджет на ремонт, сроки и проверки дома.</p>{related([("staryj-fond-ili-novostrojka/", "Сравнить варианты")])}</div>
  <div><h2>Для жизни или для сдачи</h2><p>Аренда в Ваке почти вдвое дороже, чем в Глдани: $15,1 против $8,6 за м² в месяц. Район, удобный для жизни, не всегда даёт лучшую доходность.</p>{related([("dlya-zhizni-ili-sdachi/", "Как выбрать цель покупки")])}</div>
</div></section>
<section class="band alt"><div class="wrap">
  <h2>Покупка в пять этапов</h2>
  <ol class="steps">
    <li><h3>Район и бюджет</h3><p>Определите цель и сравните районы по цене и аренде. {a("rajony/", "Районы")}</p></li>
    <li><h3>Проверка объекта</h3><p>Выписка из Публичного реестра: собственник, ипотека, арест. Для старого дома — его состояние.</p></li>
    <li><h3>Договор и задаток</h3><p>Предварительный договор с суммой задатка и условиями возврата.</p></li>
    <li><h3>Оплата и подписание</h3><p>Расчёт через банк, подписание у нотариуса или в Доме юстиции.</p></li>
    <li><h3>Регистрация</h3><p>Агентство публичного реестра вносит запись о новом собственнике. {a("kak-kupit/", "Подробно о сделке")}</p></li>
  </ol>
</div></section>
<section class="band" id="lead"><div class="wrap two">
  <div><h2>Подберём квартиру под вашу задачу</h2><p>Укажите бюджет, район и цель — специалист агентства Brik пришлёт варианты. Заявку получает команда Brik; подробнее в {a("privacy/", "политике конфиденциальности")}.</p><p class="sub">Материалы сайта проверяют партнёры Brik в Грузии. {a("o-nas/", "О проекте")}</p></div>
  {lead_form()}
</div></section>'''
    page('', 'Купить квартиру в Тбилиси — районы, цены, порядок сделки',
         'Где купить квартиру в Тбилиси: цены по районам, старый фонд или новостройка, налоги, ВНЖ и порядок сделки для иностранцев. Данные 2026 года с источниками.',
         None, body, srcs=['tbc_sep', 'ii_2026', 'geostat_q3', 'madloba_buy'])

DT = {
 'vake': dict(
   lede='Ваке — престижный район с парками, кафе и международными сервисами. По данным TBC Capital, новостройки премиум-класса здесь стоили в среднем $3 180 за м² в июле 2026 года — дороже, чем где-либо в городе.',
   facts=[('$3 180', 'м² в новостройках премиум-класса, белый каркас', 'июль 2026, TBC Capital'), ('6 046 ₾', 'медиана предложения в новостройках за м²', 'III кв. 2026, Geostat'), ('$15,1', 'аренда за м² в месяц, самая высокая в городе', 'июль 2026, TBC Capital')],
   about='<p>Ваке выбирают те, кому важны зелень, рестораны, международные школы и сервисы и престижная жилая среда. Это самый дорогой арендный рынок Тбилиси.</p><p>За январь–июль 2026 года в районе прошло 884 сделки — немного по сравнению с Сабуртало и Диди Дигоми, потому что предложение здесь ограничено и дорого.</p>',
   who='<ul class="txt"><li>Семьям и экспатам, которые хотят жить в лучшей городской среде.</li><li>Покупателям, для которых важны ликвидность и статус района больше, чем цена метра.</li></ul>',
   watch='<ul class="txt"><li>Высокая цена входа снижает доходность от аренды.</li><li>Во вторичном фонде много советских домов — проверяйте их состояние.</li></ul>',
   srcs=['ii_2026', 'geostat_q3', 'rent_guide']),
 'mtacminda-sololaki': dict(
   lede='Мтацминда со Сололаки — исторический центр у подножия горы Мтацминда. Здесь самая высокая медианная цена предложения в новостройках Тбилиси: 7 004 лари за м² в III квартале 2026 года (Geostat).',
   facts=[('7 004 ₾', 'медиана предложения в новостройках за м², первое место в городе', 'III кв. 2026, Geostat'), ('$13', 'аренда за м² в месяц', 'июль 2026, TBC Capital'), ('441', 'сделка за январь–июль 2026', 'International Investment')],
   about='<p>Район объединяет старые кварталы Сололаки и улицы под горой Мтацминда. Многие жилые дома здесь построены в конце XIX — начале XX века, и часть из них в плохом состоянии.</p><p>Мэрия Тбилиси распространила программу замены аварийных жилых домов на исторические районы с отдельным подходом, который сохраняет архитектуру Старого Тбилиси.</p>',
   who='<ul class="txt"><li>Тем, кто хочет жить в историческом центре в пешей доступности от главных мест города.</li><li>Покупателям под краткосрочную аренду туристам.</li></ul>',
   watch='<ul class="txt"><li>В старых домах закажите обследование конструкций и коммуникаций до задатка.</li><li>Для исторических зданий могут действовать ограничения на перепланировку и фасад.</li><li>Новостроек мало, цены высокие.</li></ul>',
   srcs=['geostat_q3', 'ii_2026', 'oldtbilisi']),
 'saburtalo': dict(
   lede='Сабуртало — один из самых активных рынков Тбилиси: 4 926 сделок за первые семь месяцев 2026 года. Новостройки бизнес-класса стоили в среднем $1 732 за м² в июле 2026-го (TBC Capital).',
   facts=[('$1 732', 'м² в новостройках бизнес-класса, белый каркас', 'июль 2026, TBC Capital'), ('4 926', 'сделок за январь–июль 2026', 'International Investment'), ('$11,4', 'аренда за м² в месяц', 'июль 2026, TBC Capital')],
   about='<p>Большой жилой район, где советские хрущёвки и брежневки стоят рядом с новыми жилыми комплексами. Сабуртало стабильно в лидерах по числу сделок.</p><p>Аренда здесь дешевле, чем в Ваке и Мтацминде, но дороже средней по городу ($10,3 за м² в августе 2026).</p>',
   who='<ul class="txt"><li>Тем, кто ищет баланс между ценой, инфраструктурой и близостью к центру.</li><li>Инвесторам под долгосрочную аренду: спрос стабильный.</li></ul>',
   watch='<ul class="txt"><li>Большой разброс по качеству: от советских панелек до новых комплексов.</li><li>Много нового предложения — сравнивайте застройщиков и сроки сдачи.</li></ul>',
   srcs=['ii_2026', 'khrushchevka']),
 'krcanisi': dict(
   lede='Крцаниси — спокойный зелёный район на юге города. Новостройки бизнес-класса здесь стоили в среднем $1 671 за м² в июле 2026 года, а медиана предложения по Geostat — 4 635 лари, третье место в городе.',
   facts=[('$1 671', 'м² в новостройках бизнес-класса', 'июль 2026, TBC Capital'), ('4 635 ₾', 'медиана предложения в новостройках за м²', 'III кв. 2026, Geostat'), ('590 га', 'проект Eagle Hills в Крцаниси', 'анонс 2025, Civil.ge')],
   about='<p>Крцаниси всё чаще описывают как экологичную и уединённую премиальную зону. По медиане предложения Geostat он уступает только Мтацминде и Ваке.</p><p>В 2025 году эмиратская компания Eagle Hills объявила о проекте на 590 гектарах в Крцаниси. Если он будет реализован, предложение в районе заметно изменится.</p>',
   who='<ul class="txt"><li>Тем, кому важны тишина и зелень при сохранении городской прописки.</li><li>Покупателям загородного по ощущениям жилья с выездом в центр на машине.</li></ul>',
   watch='<ul class="txt"><li>Сделок здесь меньше, чем в крупных районах — перепродажа может занять больше времени.</li><li>Следите за крупными проектами: новое предложение влияет на цены.</li></ul>',
   srcs=['ii_2026', 'geostat_q3', 'myhome', 'civil']),
 'didube': dict(
   lede='Дидубе — район среднего сегмента недалеко от центра. Новостройки бизнес-класса стоили здесь в среднем $1 425 за м² в июле 2026 года по данным TBC Capital.',
   facts=[('$1 425', 'м² в новостройках бизнес-класса', 'июль 2026, TBC Capital'), ('4 168 ₾', 'медиана предложения в новостройках за м²', 'III кв. 2026, Geostat'), ('5-е место', 'по медиане Geostat среди 10 районов', 'III кв. 2026')],
   about='<p>Дидубе занимает середину рейтинга цен: дешевле Сабуртало и Крцаниси, дороже Исани, Глдани и Самгори. Здесь сочетаются советская застройка и новые жилые комплексы.</p>',
   who='<ul class="txt"><li>Тем, кому нужна квартира в черте города по цене ниже Сабуртало.</li><li>Покупателям под долгосрочную аренду в среднем сегменте.</li></ul>',
   watch='<ul class="txt"><li>Качество домов сильно различается — смотрите конкретный дом, а не только район.</li><li>Уточните транспорт до места работы или учёбы.</li></ul>',
   srcs=['ii_2026', 'geostat_q3']),
 'isani': dict(
   lede='Исани — район среднего сегмента на левом берегу Куры. Новостройки бизнес-класса стоили в среднем $1 407 за м² в июле 2026 года (TBC Capital).',
   facts=[('$1 407', 'м² в новостройках бизнес-класса', 'июль 2026, TBC Capital'), ('4 032 ₾', 'медиана предложения в новостройках за м²', 'III кв. 2026, Geostat'), ('−10%', 'площадь новых разрешений в Тбилиси за 9 мес. 2026; снижение во многом из-за Исани, Глдани и Диди Дигоми', 'TBC Capital')],
   about='<p>По цене Исани близок к Дидубе и заметно дешевле центральных районов. В первые девять месяцев 2026 года в Тбилиси выдали на 10% меньше разрешений на жильё, и одной из причин назван именно Исани — нового предложения здесь станет меньше.</p>',
   who='<ul class="txt"><li>Тем, кто ищет новостройку по средней для города цене.</li><li>Покупателям, которым удобен левый берег.</li></ul>',
   watch='<ul class="txt"><li>В старой застройке много советских домов — проверяйте их состояние.</li><li>Сравните цену с Дидубе и Самгори: разница может быть небольшой.</li></ul>',
   srcs=['ii_2026', 'geostat_q3', 'tbc_sep']),
 'didi-digomi': dict(
   lede='Диди Дигоми — район с самым большим числом сделок в Тбилиси: 5 740 за январь–июль 2026 года. Новостройки доступного сегмента стоили в среднем $1 148 за м² (TBC Capital, июль 2026).',
   facts=[('$1 148', 'м² в доступных новостройках, белый каркас', 'июль 2026, TBC Capital'), ('5 740', 'сделок за январь–июль 2026, первое место', 'International Investment'), ('$8,7', 'аренда за м² в месяц', 'июль 2026, TBC Capital')],
   about='<p>Диди Дигоми — район массового нового строительства. В сентябре 2026 года он снова лидировал по числу сделок: 988 квартир за месяц.</p><p>Аренда здесь одна из самых низких в городе, но и цена входа минимальная.</p>',
   who='<ul class="txt"><li>Покупателям с ограниченным бюджетом, которым нужна новостройка.</li><li>Тем, кто покупает для себя и готов ездить в центр.</li></ul>',
   watch='<ul class="txt"><li>Много однотипного предложения — сдавать и перепродавать сложнее из-за конкуренции.</li><li>Проверяйте застройщика и сроки сдачи особенно внимательно.</li></ul>',
   srcs=['ii_2026', 'tbc_sep']),
 'gldani': dict(
   lede='Глдани — доступный спальный район на севере Тбилиси. Новостройки здесь стоили в среднем $1 146 за м² в июле 2026 года, одна из самых низких цен в городе (TBC Capital).',
   facts=[('$1 146', 'м² в доступных новостройках', 'июль 2026, TBC Capital'), ('3 830 ₾', 'медиана предложения в новостройках за м²', 'III кв. 2026, Geostat'), ('$8,6', 'аренда за м² в месяц', 'апрель 2026, Galt &amp; Taggart')],
   about='<p>Глдани — крупный спальный район с большим количеством советской застройки и новыми комплексами. По медиане Geostat дешевле только Самгори.</p>',
   who='<ul class="txt"><li>Тем, кто ищет самое доступное жильё в черте Тбилиси.</li><li>Семьям, которым нужна большая площадь за ограниченный бюджет.</li></ul>',
   watch='<ul class="txt"><li>Дорога до центра занимает больше времени.</li><li>Арендная ставка низкая, поэтому доходность зависит от цены покупки.</li></ul>',
   srcs=['ii_2026', 'geostat_q3', 'rent_apr']),
}

def district(d):
    t = DT[d['slug']]
    facts = ''.join(f'<div class="fact"><b>{b}</b><span>{s}</span><small>{m}</small></div>' for b, s, m in t['facts'])
    others = [(f'rajony/{o["slug"]}/', o['name']) for o in D if o['slug'] != d['slug']]
    body = f'''
<section class="facts three band" aria-label="Цифры района"><div class="wrap">{facts}</div></section>
<section class="band"><div class="wrap two">
  <div class="prose"><h2>Что за район</h2>{t['about']}</div>
  <div class="prose"><h2>Кому подойдёт</h2>{t['who']}<h2>На что обратить внимание</h2>{t['watch']}</div>
</div></section>
<section class="band alt"><div class="wrap">
  <h2>{d['name']} на карте цен</h2>
  <p>Медианная цена предложения в новостройках, III квартал 2026, Geostat. Районы без отдельной страницы показаны без ссылки.</p>
  {geo_rows(highlight=d['slug'])}
</div></section>
{cta('district-' + d['slug'], title=f'Квартиры в районе {d["name"]}', text='Свежие объявления в районе с планировками и ценами — в каталоге Brik.')}
<section class="band" style="padding-top:0"><div class="wrap"><h2 style="font-size:22px">Другие районы</h2>{related(others)}
<h2 style="font-size:22px;margin-top:24px">Перед покупкой</h2>{related([("kak-kupit/", "Порядок сделки"), ("staryj-fond-ili-novostrojka/", "Старый фонд или новостройка"), ("rashody-i-nalogi/", "Налоги")])}</div></section>'''
    page(f'rajony/{d["slug"]}/', f'{d["name"]}: квартиры, цены и особенности района | Тбилиси',
         f'{d["name"]} в Тбилиси: цена м², аренда, число сделок, кому подходит район и что проверить. Данные 2026 года.',
         [('rajony/', 'Районы'), (f'rajony/{d["slug"]}/', d['name'])], body,
         h1=f'Квартира в районе {d["name"]}', lede=t['lede'], srcs=t['srcs'])

def rajony_hub():
    rows = ''.join(
        f'<tr><td>{a("rajony/" + d["slug"] + "/", d["name"])}</td><td>{d["cls"]}</td><td class="n">{("$" + fmt(d["usd"])) if d["usd"] else "—"}</td>'
        f'<td class="n">{("$" + str(d["rent"]).replace(".", ",")) if d["rent"] else "—"}</td><td class="n">{d["sales"] or "—"}</td></tr>' for d in D)
    body = f'''
<section class="band"><div class="wrap">
  <h2>Сравнение районов</h2>
  <p>Цена м² в новостройках (белый каркас) и аренда — TBC Capital, июль 2026; аренда в Глдани — Galt &amp; Taggart, апрель 2026; сделки — январь–июль 2026. Прочерк — показатель по району не опубликован. Для Мтацминды TBC Capital не публикует цену в долларах; по Geostat это самый дорогой район.</p>
  <div><table class="stack"><thead><tr><th>Район</th><th>Сегмент</th><th class="n">Цена, $/м²</th><th class="n">Аренда, $/м²</th><th class="n">Сделок</th></tr></thead><tbody>{rows}
  <tr><td>Самгори</td><td>доступное</td><td class="n">$1&nbsp;178</td><td class="n">—</td><td class="n">—</td></tr>
  <tr><td>Ваштлиджвари</td><td>доступное</td><td class="n">$1&nbsp;094</td><td class="n">—</td><td class="n">—</td></tr></tbody></table></div>
</div></section>
<section class="band alt"><div class="wrap">
  <h2>Медианная цена по всем районам</h2>
  <p>Один источник для всех десяти административных районов: медиана цены предложения в новостройках, III квартал 2026, Geostat.</p>
  {geo_rows()}
</div></section>
<section class="band"><div class="wrap">
  <h2>Как выбрать</h2>
  <ul class="txt">
    <li><b>Премиум и городская среда:</b> Ваке, Мтацминда и Сололаки.</li>
    <li><b>Баланс цены и инфраструктуры:</b> Сабуртало, Дидубе, Крцаниси.</li>
    <li><b>Минимальный бюджет:</b> Диди Дигоми, Глдани, Самгори.</li>
    <li><b>Под сдачу:</b> сравните аренду с ценой покупки — {a("dlya-zhizni-ili-sdachi/", "как посчитать")}.</li>
  </ul>
</div></section>
{cta('rajony')}'''
    page('rajony/', 'Районы Тбилиси для покупки квартиры — сравнение цен и аренды',
         'Сравнение районов Тбилиси: цена м² в новостройках, аренда и число сделок. Ваке, Мтацминда, Сабуртало, Крцаниси, Дидубе, Исани, Диди Дигоми, Глдани.',
         [('rajony/', 'Районы')], body, h1='Районы Тбилиси: где покупать квартиру',
         lede='Медианная цена предложения в новостройках различается почти вдвое: от 3 657 лари за м² в Самгори до 7 004 в Мтацминде (Geostat, III квартал 2026). Ниже — сравнение и ссылки на страницы районов.',
         srcs=['ii_2026', 'geostat_q3', 'rent_apr'])

def ceny():
    growth = [('2023', 20.2), ('2024', 11.6), ('2025', 4.0)]
    grows = ''.join(f'<div class="row"><div class="nm"><b>{y}</b><span>рост средней цены на первичном рынке</span></div><div class="bar" aria-hidden="true"><i data-w="{v / 22 * 100:.1f}"></i></div><div class="v">+{str(v).replace(".", ",")}%</div></div>' for y, v in growth)
    grows += '<div class="row hl"><div class="nm"><b>2026, прогноз</b><span>TBC Capital, все сделки</span></div><div class="bar" aria-hidden="true"><i data-w="14.5"></i></div><div class="v">+3,2%</div></div>'
    body = f'''
<section class="band"><div class="wrap">
  <h2>Рост цен замедлился</h2>
  <p>По данным Galt &amp; Taggart, средняя цена на первичном рынке Тбилиси выросла на 20,2% в 2023 году, на 11,6% в 2024-м и на 4,0% в 2025-м. TBC Capital ожидает в 2026 году роста примерно на 3,2%.</p>
  <div class="rows">{grows}</div>
</div></section>
<section class="band alt"><div class="wrap">
  <h2>Средние цены: последние данные</h2>
  <table class="stack"><thead><tr><th>Показатель</th><th class="n">Значение</th><th>Период и источник</th></tr></thead><tbody>
    <tr><td>Средняя цена, все сделки</td><td class="n">$1 373/м²</td><td>сентябрь 2026, TBC Capital</td></tr>
    <tr><td>Новостройки, средняя цена</td><td class="n">$1 426/м²</td><td>июль 2026</td></tr>
    <tr><td>Средняя цена за 2025 год</td><td class="n">$1 312/м²</td><td>TBC Capital, +4,1% за год</td></tr>
    <tr><td>Сделок с квартирами за 2025 год</td><td class="n">42 388</td><td>Galt &amp; Taggart</td></tr>
    <tr><td>Новостройки в центре</td><td class="n">+12,3% за год</td><td>сентябрь 2026, Colliers</td></tr>
  </tbody></table>
</div></section>
<section class="band"><div class="wrap">
  <h2>Цены по районам</h2>
  <p>Медианная цена предложения в новостройках, III квартал 2026, Geostat, лари за м².</p>
  {geo_rows()}
  <p style="margin-top:18px">В долларах, по данным TBC Capital за июль 2026 года: Ваке — $3 180 за м², Сабуртало — $1 732, Крцаниси — $1 671, Дидубе — $1 425, Исани — $1 407, Самгори — $1 178, Диди Дигоми — $1 148, Глдани — $1 146.</p>
</div></section>
{cta('ceny')}'''
    page('ceny/', 'Цены на квартиры в Тбилиси в 2026 году — по районам',
         'Средняя цена м² в Тбилиси в 2026 году, цены по районам в лари и долларах, рост цен 2023–2025 и прогноз. Данные TBC Capital, Galt & Taggart, Geostat.',
         [('ceny/', 'Цены')], body, h1='Цены на квартиры в Тбилиси',
         lede='В сентябре 2026 года средняя цена квартиры в Тбилиси составила $1 373 за м² (TBC Capital). После быстрого роста в 2023–2024 годах цены растут медленнее: в 2026-м ожидают около +3,2%.',
         srcs=['tbc_sep', 'ii_2026', 'tbc_2025', 'gt_2025', 'gt_sales', 'geostat_q3'])

def staryj_fond():
    body = f'''
<section class="band"><div class="wrap two">
  <div class="prose">
    <h2>Старый фонд</h2>
    <p>В Тбилиси много советских домов: хрущёвок и брежневок, часто пятиэтажных панельных. В исторических районах встречаются дома конца XIX — начала XX века.</p>
    <ul class="txt"><li><b>Плюсы:</b> обжитые районы, можно сразу посмотреть дом и соседей, часто ниже цена за метр.</li><li><b>Минусы:</b> изношенные коммуникации, устаревшие планировки, риски по состоянию конструкций.</li></ul>
    <p>С 2022 года мэрия Тбилиси ведёт программу замены аварийных многоквартирных домов, а теперь распространила её и на Старый Тбилиси.</p>
  </div>
  <div class="prose">
    <h2>Новостройка</h2>
    <p>Новые дома в Тбилиси продают в разной степени готовности. Цена за метр сильно зависит от этого.</p>
    <table class="stack"><thead><tr><th>Состояние</th><th>Что получаете</th></tr></thead><tbody>
      <tr><td class="k">Чёрный каркас</td><td>Стены, перегородки, окна и входная дверь; без коммуникаций и отделки.</td></tr>
      <tr><td class="k">Белый каркас</td><td>Подведены коммуникации, стены оштукатурены, черновая стяжка.</td></tr>
      <tr><td class="k">Зелёный каркас</td><td>Готово под косметическую отделку — меньше работы на старте.</td></tr>
      <tr><td class="k">С ремонтом</td><td>Часто с мебелью и техникой; цена за метр заметно выше.</td></tr>
    </tbody></table>
  </div>
</div></section>
<section class="band alt"><div class="wrap two">
  <div class="prose">
    <h2>Что проверить в старом доме</h2>
    <ul class="check">
      <li>Год постройки и тип дома.</li>
      <li>Состояние несущих стен, перекрытий, крыши и подвала — лучше с инженером.</li>
      <li>Электрика, водопровод и канализация в доме, а не только в квартире.</li>
      <li>Узаконены ли перепланировки и пристройки, совпадает ли площадь с выпиской.</li>
      <li>Не включён ли дом в программу замены аварийного жилья.</li>
    </ul>
  </div>
  <div class="prose">
    <h2>Что проверить в новостройке</h2>
    <ul class="check">
      <li>Земля принадлежит застройщику и не заложена.</li>
      <li>Разрешение на строительство соответствует проекту, который вам показывают.</li>
      <li>У застройщика есть сданные дома.</li>
      <li>Что именно входит в «белый» или «зелёный» каркас по договору.</li>
      <li>Срок сдачи, штраф за задержку и график платежей.</li>
    </ul>
  </div>
</div></section>
<section class="band"><div class="wrap"><div class="note">Тбилиси находится в сейсмически активном регионе. Перед покупкой квартиры в старом доме имеет смысл заказать техническое обследование, а в новостройке — спросить у застройщика о расчёте на сейсмические нагрузки.</div>{related([("kak-kupit/", "Порядок сделки"), ("rashody-i-nalogi/", "Расходы"), ("rajony/saburtalo/", "Сабуртало"), ("rajony/mtacminda-sololaki/", "Мтацминда и Сололаки")])}</div></section>
{cta('staryj-fond', title='Новостройки и вторичный рынок Тбилиси', text='Сравните варианты в каталоге Brik.')}'''
    page('staryj-fond-ili-novostrojka/', 'Старый фонд или новостройка в Тбилиси — что выбрать',
         'Хрущёвки, исторические дома и новостройки в Тбилиси: плюсы и минусы, что такое чёрный, белый и зелёный каркас, что проверить перед покупкой.',
         [('staryj-fond-ili-novostrojka/', 'Старый фонд или новостройка')], body, h1='Старый фонд или новостройка',
         lede='Вторичный рынок Тбилиси — это во многом советские дома и старые кварталы, новостройки продают в каркасе разной степени готовности. От выбора зависят бюджет на ремонт, риски и то, что нужно проверить до задатка.',
         srcs=['khrushchevka', 'dilapidated', 'oldtbilisi', 'korter_frames', 'myhome', 'safebuy', 'cappuccino'])

def zhizn_sdacha():
    rent = [('Ваке', 15.1), ('Мтацминда', 13.0), ('Сабуртало', 11.4), ('Средняя по городу', 10.3), ('Диди Дигоми', 8.7), ('Глдани', 8.6), ('Самгори', 8.2)]
    rows = ''.join(f'<div class="row{" hl" if n.startswith("Средняя") else ""}"><div class="nm"><b>{n}</b><span>аренда, $ за м² в месяц</span></div><div class="bar" aria-hidden="true"><i data-w="{v / 16 * 100:.1f}"></i></div><div class="v">${str(v).replace(".", ",")}</div></div>' for n, v in rent)
    body = f'''
<section class="band"><div class="wrap">
  <h2>Аренда по районам</h2>
  <p>Ваке, Мтацминда, Сабуртало, Диди Дигоми и средняя по городу — TBC Capital, июль–август 2026; Глдани и Самгори — Galt &amp; Taggart, апрель 2026.</p>
  <div class="rows">{rows}</div>
</div></section>
<section class="band alt"><div class="wrap two">
  <div class="prose">
    <h2>Если покупаете для жизни</h2>
    <ul class="txt"><li>Решают транспорт, школы, парки и шум — съездите в район вечером и в выходной.</li><li>Ваке и Мтацминда дают лучшую городскую среду, Сабуртало и Дидубе — баланс цены и удобства.</li><li>При покупке в старом доме заложите бюджет на ремонт коммуникаций.</li></ul>
  </div>
  <div class="prose">
    <h2>Если покупаете для сдачи</h2>
    <ul class="txt"><li>Валовая доходность в Тбилиси — 8,3% (август 2026, TBC Capital), до расходов и налогов.</li><li>Краткосрочная аренда: средняя цена ночи $57 при загрузке 38,9% (AirROI, август 2025 — июль 2026).</li><li>С дохода от сдачи жилья для проживания физлицо платит 5%.</li></ul>
  </div>
</div></section>
<section class="band"><div class="wrap">
  <h2>Как посчитать доходность</h2>
  <p>Пример на средних цифрах: квартира 50 м² по $1 400 за м² стоит $70 000. При аренде $10,3 за м² она приносит $515 в месяц, или $6 180 в год — 8,8% до расходов. После налога 5% ($309), простоя и обслуживания чистая доходность будет ниже.</p>
  <p>В дорогих районах аренда выше, но цена покупки растёт быстрее, поэтому доходность там обычно ниже, чем в среднем по городу.</p>
  <div class="note">Пример иллюстративный: реальная доходность зависит от конкретной квартиры, ремонта и загрузки.</div>
  {related([("rashody-i-nalogi/", "Налоги на аренду"), ("rajony/", "Сравнить районы")])}
</div></section>
{cta('zhizn-sdacha')}'''
    page('dlya-zhizni-ili-sdachi/', 'Квартира в Тбилиси для жизни или для сдачи — аренда и доходность',
         'Аренда по районам Тбилиси, валовая доходность 8,3%, краткосрочная аренда и пример расчёта. Как выбрать квартиру для жизни или для сдачи.',
         [('dlya-zhizni-ili-sdachi/', 'Для жизни или сдачи')], body, h1='Для жизни или для сдачи',
         lede='Средняя аренда в Тбилиси — $10,3 за м² в месяц, валовая доходность — 8,3% (TBC Capital, август 2026). Но районы, удобные для жизни, и районы с лучшей доходностью часто разные.',
         srcs=['ii_2026', 'rent_apr', 'madloba_rent'])

def kak_kupit():
    body = f'''
<section class="band"><div class="wrap two">
  <div class="prose">
    <h2>Кто может купить</h2>
    <p>Квартиры, дома и коммерческую недвижимость в Грузии иностранцы покупают наравне с гражданами. Ни виза, ни ВНЖ для сделки не нужны. Исключение — сельскохозяйственная земля: её могут иметь только государство, муниципалитеты и граждане Грузии.</p>
    <h2>Документы</h2>
    <ul class="txt"><li>Загранпаспорт покупателя.</li><li>Договор купли-продажи на грузинском языке, часто с переводом.</li><li>Квитанция об оплате регистрационного сбора (тариф — на napr.gov.ge).</li><li>Доверенность с нотариальным переводом, если сделку проводит представитель.</li></ul>
  </div>
  <div class="prose">
    <h2>Ипотека для иностранцев</h2>
    <p>Некоторые банки кредитуют иностранцев. Например, у TBC Bank есть упрощённая программа: первый взнос от 20%, сумма от $3 000 до $300 000 в эквиваленте, в лари или евро. На 26 октября 2026 года номинальная ставка — от 9,9%, эффективная — от 11,35%. Условия банк определяет при одобрении.</p>
    <p class="sub">Условия ипотеки меняются — уточняйте их в банке перед сделкой.</p>
  </div>
</div></section>
<section class="band alt"><div class="wrap">
  <h2>Сделка по шагам</h2>
  <ol class="steps">
    <li><h3>Проверьте объект</h3><p>На napr.gov.ge — собственник, площадь, ипотека и аресты. Для старого дома — его состояние, для новостройки — права застройщика на землю.</p></li>
    <li><h3>Подпишите предварительный договор</h3><p>Цена, сроки, сумма задатка и условия его возврата. Покажите договор юристу.</p></li>
    <li><h3>Откройте счёт</h3><p>Расчёт обычно идёт через грузинский банк. Он может спросить о происхождении средств — подготовьте документы заранее.</p></li>
    <li><h3>Подпишите основной договор</h3><p>У нотариуса или в Доме юстиции; деньги переводятся на счёт продавца.</p></li>
    <li><h3>Зарегистрируйте право</h3><p>Агентство публичного реестра регистрирует сделку за один или несколько рабочих дней. Право собственности возникает с момента регистрации.</p></li>
    <li><h3>Оформите коммунальные счета</h3><p>Переведите электричество, воду и газ на себя и сохраните документы для налоговой.</p></li>
  </ol>
</div></section>
<section class="band"><div class="wrap">
  <h2>Покупка на расстоянии</h2>
  <p>Если вы не можете приехать, сделку проводит представитель по доверенности. Её оформляют у нотариуса в своей стране и переводят на грузинский с нотариальным заверением. Для доверенностей из России апостиль не требуется — обе страны участвуют в Минской конвенции. Из большинства других стран нужен апостиль.</p>
  {related([("staryj-fond-ili-novostrojka/", "Что проверить в доме"), ("rashody-i-nalogi/", "Расходы"), ("vnzh-za-nedvizhimost/", "ВНЖ"), ("faq/", "Вопросы")])}
</div></section>
{cta('kak-kupit')}'''
    page('kak-kupit/', 'Как купить квартиру в Тбилиси иностранцу — пошагово',
         'Порядок покупки квартиры в Тбилиси для иностранцев: документы, проверка в реестре, оплата, регистрация, ипотека и сделка по доверенности.',
         [('kak-kupit/', 'Как купить')], body, h1='Как купить квартиру в Тбилиси',
         lede='Иностранцу для покупки квартиры в Тбилиси нужен только загранпаспорт. Регистрация права собственности занимает от одного до нескольких рабочих дней, а сделку можно провести и без приезда — по доверенности.',
         srcs=['madloba_buy', 'chambers', 'ii_2026', 'madloba_poa', 'napr'])

def rashody():
    body = f'''
<section class="band"><div class="wrap">
  <h2>Разовые расходы покупателя</h2>
  <table class="stack"><thead><tr><th>Статья</th><th>Сумма</th><th>Комментарий</th></tr></thead><tbody>
    <tr><td>Налог на покупку</td><td class="k">нет</td><td>Отдельного налога на переход права собственности нет.</td></tr>
    <tr><td>Регистрация в реестре</td><td class="k">по тарифу</td><td>Зависит от срочности; актуальная сумма на napr.gov.ge.</td></tr>
    <tr><td>Нотариус, перевод</td><td class="k">по тарифу</td><td>Если договор или доверенность заверяют у нотариуса.</td></tr>
    <tr><td>Агентство</td><td class="k">обычно 3–5%</td><td>Чаще всего платит продавец; зависит от договора.</td></tr>
    <tr><td>Итого для покупателя</td><td class="k">0,6–1,1%</td><td>Типичная оценка Global Property Guide.</td></tr>
  </tbody></table>
</div></section>
<section class="band alt"><div class="wrap">
  <h2>Налоги владельца в 2026 году</h2>
  <table class="stack"><thead><tr><th>Налог</th><th>Ставка</th><th>Когда</th></tr></thead><tbody>
    <tr><td>На имущество</td><td class="k">0% / 0,8–1%</td><td>С 1 октября 2026 года не платится, если доход семьи за прошлый год не выше 100 000 лари. Выше порога — 0,8–1% рыночной стоимости. Промежуточная ставка 0,05–0,2% отменена.</td></tr>
    <tr><td>С аренды жилья</td><td class="k">5%</td><td>С поступлений, без вычета расходов, если жильё сдаётся для проживания.</td></tr>
    <tr><td>С продажи</td><td class="k">0% или 5%</td><td>Без налога при владении больше двух лет; иначе 5% с прироста стоимости.</td></tr>
    <tr><td>Посуточная сдача через ИП</td><td class="k">1% с оборота</td><td>При статусе малого бизнеса и обороте до 500 000 лари в год. Применимость к вашему случаю уточните в Службе доходов.</td></tr>
  </tbody></table>
  <div class="note">Многие сайты до сих пор пишут о пороге налога на имущество в 40 000 лари — он изменён с 1 октября 2026 года. Перед сделкой уточняйте правила на rs.ge или у налогового консультанта.</div>
</div></section>
<section class="band"><div class="wrap">{related([("dlya-zhizni-ili-sdachi/", "Доходность аренды"), ("kak-kupit/", "Порядок сделки"), ("vnzh-za-nedvizhimost/", "ВНЖ")])}</div></section>
{cta('rashody')}'''
    page('rashody-i-nalogi/', 'Расходы и налоги при покупке квартиры в Тбилиси — 2026',
         'Расходы на покупку квартиры в Тбилиси и налоги владельца в 2026 году: налог на имущество с порогом 100 000 лари, 5% с аренды, продажа после двух лет.',
         [('rashody-i-nalogi/', 'Расходы и налоги')], body, h1='Расходы и налоги',
         lede='Налога на покупку в Грузии нет, разовые расходы покупателя — обычно 0,6–1,1% цены. С 1 октября 2026 года налог на имущество платят только семьи с годовым доходом выше 100 000 лари.',
         srcs=['ii_2026', 'gpg_buy', 'sova', 'madloba_rent', 'andersen', 'madloba_tax', 'rs'])

def vnzh():
    rows = ''.join(f'<tr><td>{a("rajony/" + d["slug"] + "/", d["name"])}</td><td class="n">{fmt(d["usd"])}</td><td class="n">от {-(-150000 // d["usd"])} м²</td></tr>' for d in D if d['usd'])
    body = f'''
<section class="facts three band" aria-label="Условия ВНЖ"><div class="wrap">
  <div class="fact"><b>$150 000</b><span>рыночная стоимость недвижимости, не меньше</span><small>с 1 марта 2026</small></div>
  <div class="fact"><b>Семья</b><span>супруг и дети получают ВНЖ вместе с владельцем</span><small>EIG Law</small></div>
  <div class="fact"><b>Ежегодно</b><span>продление при сохранении права собственности</span><small>EIG Law</small></div>
</div></section>
<section class="band"><div class="wrap two">
  <div class="prose">
    <h2>Кто может получить</h2>
    <p>Владелец несельскохозяйственной недвижимости в Грузии, рыночная стоимость которой не меньше $150 000. Стоимость подтверждает оценка, а не сумма в договоре; несколько объектов можно сложить. Порог действует с 1 марта 2026 года, раньше он был $100 000.</p>
    <p>Заявление рассматривает Агентство развития государственных услуг — обычно до 30 дней, быстрее за дополнительную плату. Решение не автоматическое.</p>
  </div>
  <div class="prose">
    <h2>Ограничения</h2>
    <ul class="txt"><li>Этот ВНЖ краткосрочный и не ведёт к постоянному виду на жительство.</li><li>Получившие ВНЖ по старому порогу могут продлевать его на прежних условиях, пока владеют той же недвижимостью.</li><li>Инвестиционный ВНЖ — отдельный вид, он требует вложений от $300 000.</li><li>Размер госпошлины зависит от срока рассмотрения; смотрите на sda.gov.ge.</li></ul>
  </div>
</div></section>
<section class="band alt"><div class="wrap">
  <h2>Площадь, нужная для ВНЖ, по районам</h2>
  <p>Ориентир по средней цене новостроек в белом каркасе (TBC Capital, июль 2026). С ремонтом метр дороже, поэтому нужная площадь будет меньше; решает оценка конкретной квартиры.</p>
  <table><thead><tr><th>Район</th><th class="n">$/м²</th><th class="n">Площадь</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>
{cta('vnzh', title='Квартиры от $150 000 в Тбилиси', text='Объекты, стоимость которых может подойти для ВНЖ.')}'''
    page('vnzh-za-nedvizhimost/', 'ВНЖ в Грузии за покупку квартиры в Тбилиси — порог $150 000',
         'ВНЖ в Грузии для владельцев недвижимости с 1 марта 2026 года: порог $150 000, оценка, семья, сроки и какая площадь нужна в районах Тбилиси.',
         [('vnzh-za-nedvizhimost/', 'ВНЖ')], body, h1='ВНЖ за покупку недвижимости',
         lede='С 1 марта 2026 года краткосрочный ВНЖ дают владельцам недвижимости в Грузии рыночной стоимостью от $150 000. В Тбилиси это от 48 м² в Ваке до 131 м² в Глдани по средним ценам новостроек.',
         srcs=['eig', 'madloba_rp', 'visaatlas', 'sda', 'ii_2026'])

FAQ = [
 ('Может ли иностранец купить квартиру в Тбилиси?', 'Да, на тех же условиях, что и граждане Грузии. Ограничение есть только для сельскохозяйственной земли.', 'kak-kupit/'),
 ('Сколько стоит квартира в Тбилиси?', 'Средняя цена в сентябре 2026 года — $1 373 за м² (TBC Capital). В новостройках Ваке — около $3 180, в Диди Дигоми и Глдани — около $1 150.', 'ceny/'),
 ('Какой район самый дорогой?', 'По медиане Geostat — Мтацминда (7 004 лари за м²), затем Ваке. По данным TBC Capital в долларах — Ваке.', 'rajony/'),
 ('Где больше всего сделок?', 'В Диди Дигоми и Сабуртало: 5 740 и 4 926 сделок за январь–июль 2026 года.', 'rajony/didi-digomi/'),
 ('Можно ли взять ипотеку иностранцу?', 'Да, в некоторых банках. Например, у TBC Bank первый взнос от 20%, ставка от 9,9% номинальная на конец октября 2026 года.', 'kak-kupit/'),
 ('Стоит ли покупать хрущёвку?', 'Это дешевле, но дом нужно проверить: возраст, конструкции, коммуникации, планы мэрии по аварийному жилью.', 'staryj-fond-ili-novostrojka/'),
 ('Какая доходность у аренды?', 'Около 8,3% валовых в год по данным TBC Capital за август 2026 года, до налогов и расходов.', 'dlya-zhizni-ili-sdachi/'),
 ('Какие налоги платит владелец?', '5% с дохода от сдачи жилья; при продаже после двух лет владения — 0%; налог на имущество — только при доходе семьи выше 100 000 лари.', 'rashody-i-nalogi/'),
 ('Дадут ли ВНЖ за квартиру?', 'Можно подать заявление, если рыночная стоимость вашей недвижимости в Грузии от $150 000. Решение принимает Агентство развития государственных услуг.', 'vnzh-za-nedvizhimost/'),
 ('Можно ли купить, не приезжая?', 'Да, по нотариальной доверенности с переводом на грузинский. Для российских доверенностей апостиль не нужен.', 'kak-kupit/'),
]

def faq():
    items = ''.join(f'<details><summary>{q}</summary><p>{ans} {a(t, "Подробнее")}</p></details>' for q, ans, t in FAQ)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ans}} for q, ans, _ in FAQ]}, ensure_ascii=False)
    page('faq/', 'Вопросы о покупке квартиры в Тбилиси',
         'Ответы на частые вопросы о покупке квартиры в Тбилиси: цены, районы, ипотека, налоги, ВНЖ и сделка без приезда.',
         [('faq/', 'Вопросы')], f'<section class="band"><div class="wrap">{items}</div></section>{cta("faq")}',
         h1='Вопросы и ответы', lede='Короткие ответы со ссылками на подробные страницы. Данные на ноябрь 2026 года.',
         srcs=['tbc_sep', 'ii_2026', 'geostat_q3', 'eig', 'madloba_poa'], head_extra=f'\n<script type="application/ld+json">{ld}</script>')

def o_nas():
    body = f'''
<section class="band"><div class="wrap two">
  <div class="prose">
    <h2>О проекте</h2>
    <p>Тбилиси·квартиры — справочник для покупателей жилья в столице Грузии: районы, цены, налоги и порядок сделки в одном месте.</p>
    <p>Сайт входит в проект <a href="{brik('o-nas')}">Brik</a> — площадку объявлений о недвижимости в Грузии. Подборки объявлений и заявки ведут в каталог и агентство Brik.</p>
    <h2>Наши правила</h2>
    <ul class="txt"><li>У каждой цифры есть источник и период.</li><li>Цены из разных исследований не смешиваем в одном сравнении.</li><li>Правовые и налоговые разделы проверяют партнёры проекта в Грузии.</li><li>Мы не даём юридических консультаций и советуем проверять сделку с юристом.</li></ul>
  </div>
  <div class="prose">
    <h2>Авторы</h2>
    <div class="note">Черновик: здесь будут имена, фото и опыт авторов и проверяющих.</div>
    <h2>Нашли неточность?</h2>
    <p>Напишите через {a("kontakty/", "форму на странице контактов")} — мы проверим и обновим данные.</p>
  </div>
</div></section>'''
    page('o-nas/', 'О проекте Тбилиси·квартиры', 'Кто готовит материалы сайта, откуда данные и как сайт связан с площадкой Brik.',
         [('o-nas/', 'О нас')], body, h1='О проекте', lede='Тбилиси·квартиры — справочник по покупке жилья в Тбилиси, часть проекта Brik.')

def kontakty():
    body = f'''
<section class="band"><div class="wrap two">
  <div class="prose"><h2>Напишите нам</h2><p>Специалист агентства Brik ответит на вопросы о районах, конкретных квартирах и порядке сделки и пришлёт подборку.</p>
  <div class="note">Черновик: телефон, мессенджеры, e-mail и адрес будут добавлены перед запуском.</div></div>
  {lead_form('<label>Ваш вопрос<textarea name="question"></textarea></label>')}
</div></section>'''
    page('kontakty/', 'Контакты — Тбилиси·квартиры', 'Связаться с командой Brik: подбор квартиры в Тбилиси и вопросы по сделке.',
         [('kontakty/', 'Контакты')], body, h1='Контакты', lede='Задайте вопрос или получите подборку квартир в Тбилиси.')

def privacy():
    body = '''
<section class="band"><div class="wrap prose">
  <div class="note">Черновик для юридической проверки: юрлицо, адрес и контакт для обращений будут указаны перед запуском.</div>
  <h2>Что мы получаем</h2><p>Данные из формы заявки: имя, контакт для связи, бюджет, район, цель покупки и текст вопроса.</p>
  <h2>Для чего</h2><p>Чтобы специалист агентства Brik связался с вами и прислал подборку. Для других целей без вашего согласия данные не используются.</p>
  <h2>Кто видит данные</h2><p>Команда Brik. Мы не продаём данные и не передаём их третьим лицам, если этого не требует закон.</p>
  <h2>Как долго храним</h2><p>Пока это нужно для ответа и сопровождения сделки или пока вы не попросите удалить данные.</p>
  <h2>Ваши права</h2><p>Вы можете запросить, исправить или удалить свои данные. У основного сайта Brik своя политика конфиденциальности.</p>
  <h2>Аналитика</h2><p>Мы можем использовать веб-аналитику. Ссылки на Brik содержат метки, по которым видно, что переход был с этого сайта.</p>
</div></section>'''
    page('privacy/', 'Политика конфиденциальности — Тбилиси·квартиры', 'Какие данные собирает сайт и как они используются.',
         [('privacy/', 'Конфиденциальность')], body, h1='Политика конфиденциальности', lede='Как мы обрабатываем данные из формы заявки.')

if __name__ == '__main__':
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'assets'))
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(os.path.join(here, 'site.css'), os.path.join(OUT, 'assets', 'site.css'))
    shutil.copy(os.path.join(here, 'site.js'), os.path.join(OUT, 'assets', 'site.js'))
    home(); rajony_hub()
    for d in D: district(d)
    ceny(); staryj_fond(); zhizn_sdacha(); kak_kupit(); rashody(); vnzh(); faq(); o_nas(); kontakty(); privacy()
    print('pages:', sum(1 for r, _, fs in os.walk(OUT) for f in fs if f == 'index.html'))
