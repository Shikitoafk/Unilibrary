from pathlib import Path
import re, html, json
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
INPUT = Path(r'C:/Users/PC/Downloads/Yonsei University.pdf')
reader = PdfReader(str(INPUT))

official = {
    'history': 'https://www.yonsei.ac.kr/en_sc/1771/subview.do',
    'admissions': 'https://uic.yonsei.ac.kr/admission.php?mid=m04_02_02',
    'fees': 'https://uic.yonsei.ac.kr/admission.php?mid=m04_03',
    'faq': 'https://uic.yonsei.ac.kr/admission.php?mid=m04_05',
    'lsbt': 'https://uic.yonsei.ac.kr/undergraduate.php?mid=m02_01_05',
    'ised': 'https://uic.yonsei.ac.kr/undergraduate.php?mid=m02_03_03',
    'core': 'https://uic.yonsei.ac.kr/undergraduate.php?mid=m02_04',
    'research': 'https://uic.yonsei.ac.kr/undergraduate.php?mid=m02_08_04',
    'exchange': 'https://uic.yonsei.ac.kr/undergraduate.php?mid=m02_08_08',
    'career': 'https://uic.yonsei.ac.kr/career.php?mid=m06_01_01',
    'counsel': 'https://uic.yonsei.ac.kr/student.php?mid=m05_05_03',
    'housing': 'https://gosc.yonsei.ac.kr/gosc/life/oncampus01.do',
    'monet': 'https://uic.yonsei.ac.kr/news.php?act=view&cmid=m06_01_03&mid=m07_01_03&uid=13935',
    'gks': 'https://www.studyinkorea.go.kr/ko/plan/gksNoticeRead.do?bbsId=BBSMSTR_000000000461&nttId=4522',
    'campuses': 'https://uic.yonsei.ac.kr/main/about.php?mid=m01_03',
    'traditions': 'https://www.yonsei.ac.kr/bbs/en_sc/260/937348/artclView.do',
}

meta = '''---
name: Yonsei University
city: "Сеул / Инчхон"
country: "Южная Корея"
countryCode: KR
founded: 1885
thesis: "Англоязычный колледж внутри большого корейского университета: биология, междисциплинарные программы и медицинская исследовательская среда. Твой опыт зависит от маршрута, кампуса и готовности учить корейский."
accent: '#153E76'
accentDark: '#91B8EF'
profile: "биомедицина / STEM, абитуриент из Казахстана, нужна финансовая помощь"
updated: 2026-09-13
acceptanceRate: null
acceptanceNote: "Сопоставимая статистика international undergraduate admissions не подтверждена."
satRange: null
actRange: null
testPolicy: optional
separateCollegeAdmission: true
costOfAttendance: null
meetsFullNeed: false
aidForInternationals: true
avgGrant: null
avgPackage: null
meritAid: true
needBlind: false
strengths: [биология, биотехнологии, Bio-Convergence, экономика, международные отношения]
campusType: big city
climate: "Холодная зима, жаркое влажное лето; Songdo и Sinchon дают разный городской опыт."
fit:
  academic: {score: 3, note: "сильный вариант для LSBT / Bio-Convergence"}
  research: {score: 3, note: "возможности есть; место в лаборатории нужно искать"}
  intellectual: {score: 3, note: "наука вместе с liberal arts"}
  culture: {score: 2, note: "зависит от кампуса и интереса к Корее"}
  financial: {score: 2, note: "считать после scholarship offer"}
  admissions: {score: 3, note: "конкурс; вероятность по исходнику не оценить"}
sources:
  official:
    - {label: "История Yonsei", url: "''' + official['history'] + '''"}
    - {label: "UIC: международный приём и набор 2027", url: "''' + official['admissions'] + '''"}
    - {label: "UIC: стоимость и стипендии, 2026", url: "''' + official['fees'] + '''"}
    - {label: "UIC: FAQ по маршрутам", url: "''' + official['faq'] + '''"}
    - {label: "LSBT", url: "''' + official['lsbt'] + '''"}
    - {label: "Bio-Convergence / ISED", url: "''' + official['ised'] + '''"}
    - {label: "Common Curriculum", url: "''' + official['core'] + '''"}
    - {label: "UIC Research Projects", url: "''' + official['research'] + '''"}
    - {label: "UIC Exchange Program", url: "''' + official['exchange'] + '''"}
    - {label: "UIC Career Development Center", url: "''' + official['career'] + '''"}
    - {label: "UIC Counseling Center", url: "''' + official['counsel'] + '''"}
    - {label: "Общежития Yonsei", url: "''' + official['housing'] + '''"}
    - {label: "Monet Laboratory", url: "''' + official['monet'] + '''"}
    - {label: "GKS-U 2027", url: "''' + official['gks'] + '''"}
  data:
    - {label: "Авторский исходник: Yonsei University.pdf, 47 страниц; полная редакция с дополнениями от 13.09.2026."}
  reviews:
    - {label: "The Yonsei Annals: развитие Songdo", url: "https://annals.yonsei.ac.kr/news/articleView.html?idxno=11100"}
  news:
    - {label: "Yonsei: университетские традиции", url: "''' + official['traditions'] + '''"}
sourceCaveat: "Полная редакция авторского исследования: сохранены исходные темы и вопросы, повторы слегка объединены. Ключевые правила UIC, тарифы 2026, условия набора 2027, research, career и counseling сверены 13.09.2026. Для regular colleges, GLC и других наборов действуют отдельные правила. Graduate school и GKS не следует автоматически считать условиями бакалавриата. Прочерк в COA означает отсутствие проверенного полного бюджета. Оценки соответствия — редакционное суждение, не статистика."
---
'''

sections = [
    ('identity', 'Идентичность', 1, 6),
    ('academics', 'Академика', 7, 14),
    ('research', 'Исследования', 15, 18),
    ('life', 'Жизнь на кампусе', 19, 22),
    ('admissions', 'Поступление', 23, 26),
    ('money', 'Деньги', 27, 30),
    ('outcomes', 'Карьера и выпускники', 31, 34),
    ('criticism', 'Критика и риски', 35, 38),
    ('you', 'Ты × университет', 39, 42),
    ('verdict', 'Итоговый вердикт', 43, 47),
]

headings = {
    'История':'История', 'Философия и миссия':'Философия и миссия', 'Что университет пытается построить':'Что университет пытается построить',
    'Реальные ценности':'Реальные ценности', 'Главный identity trade-off':'Главный компромисс', 'Academic structure':'Структура обучения',
    'Curriculum':'Учебная программа', 'Flexibility':'Гибкость', 'Majors':'Направления', 'Core':'Общая подготовка', 'Electives':'Курсы по выбору',
    'English vs Korean':'Английский и корейский', 'Global opportunities':'Международные возможности', 'Academic reality: UIC vs KAIST':'UIC и KAIST',
    'Research philosophy':'Подход к исследованиям', 'Labs & centers':'Лаборатории и центры', 'Undergraduate research':'Исследования на бакалавриате',
    'Professors':'Преподаватели', 'Research opportunities':'Исследовательские возможности', 'Campus':'Кампус', 'Residential life':'Проживание',
    'Clubs':'Клубы', 'Traditions':'Традиции', 'Culture':'Культура', 'Community':'Сообщество', 'Who are they looking for?':'Кого ищет университет',
    'Academic profile':'Академический профиль', 'Essays':'Эссе', 'ECs (Extracurriculars)':'Внеклассные занятия', 'Interview':'Интервью',
    'Demonstrated interest':'Проявленный интерес', 'Application Process':'Подача заявки', 'Cost':'Стоимость', 'Financial aid':'Финансовая помощь',
    'Full ride':'Полное финансирование', 'Merit':'Стипендии за достижения', 'International students':'Иностранные студенты',
    'Additional Financial Information':'Дополнительная финансовая информация', 'Employment':'Трудоустройство', 'Graduate school':'Продолжение образования',
    'Alumni':'Выпускники', 'Network':'Профессиональные связи', 'Career Support':'Карьерная поддержка', 'What can be bad?':'Что может не подойти',
    'Student complaints':'Отзывы и вопросы студентов', 'Structural problems':'Структурные ограничения', 'Cultural problems':'Культурные особенности',
    'Academic Pressure':'Учебное давление', 'Additional Risks':'Дополнительные риски', 'Why you fit':'Кому подходит', "Where you don't fit":'Кому может не подойти',
    'What you could do there':'Что можно делать в университете', 'What you would miss':'Чего может не хватать', 'Final Verdict':'Финальный вердикт',
    'Academic fit':'Академическое соответствие', 'Research fit':'Исследовательское соответствие', 'Intellectual fit':'Интеллектуальное соответствие',
    'Culture fit':'Культурное соответствие', 'Financial fit':'Финансовое соответствие', 'Admissions fit':'Сложность поступления', 'Overall fit':'Общий вывод',
}

def esc(s):
    s = re.sub(r'\s+', ' ', s).strip()
    s = s.replace('{','&#123;').replace('}','&#125;')
    s = s.replace('<','&lt;').replace('>','&gt;')
    return s.replace('~','≈')

def verify(text, url):
    return f'<Fact label="Проверено"><p>{esc(text)} <Src href="{url}">Официальный источник</Src></p></Fact>'

notes = {
 'identity': verify('История Yonsei начинается с Gwanghyewon в 1885 году; Yonhi University и Severance Medical College объединились в 1957-м. 1885 — исторические корни, 1957 — современное объединение.', official['history']) + '\n' + verify('UIC и GLC — разные маршруты: UIC проводит курсы на английском, GLC в основном на корейском. Exchange и Summer School не являются полным бакалавриатом.', official['faq']),
 'academics': verify('UIC в актуальном обзоре включает 16 majors в трёх divisions: UD, HASSD и ISED. Для biomedical профиля важны LSBT и Bio-Convergence; старое название ASD заменено на ISED.', 'https://about.yonsei.ac.kr/eng/') + '\n' + verify('LSBT связан с Underwood Division, а Bio-Convergence — с ISED. Оба маршрута не являются автоматически медицинским образованием врача.', official['lsbt']),
 'research': verify('Monet Laboratory при College of Medicine объявлял набор бакалавров и graduate students в 2025 году для исследований brain imaging, computational neuroscience, brain disorders и AI. Объявление описывало стажировку как неоплачиваемую, с возможным небольшим вознаграждением при долгом участии.', official['monet']) + '\n' + verify('UIC Research Projects имеет летний URP-Global и зимний URP-Korea; это формальная undergraduate research-программа, но не гарантия места в biomedical lab.', official['research']),
 'life': verify('Все первокурсники Yonsei обычно участвуют в Residential College и подают на общежитие Songdo; для UIC UD официальный маршрут описывает переход в Sinchon со второго года. Для ISED и отдельных majors кампус нужно уточнять по учебному плану.', official['housing']) + '\n' + verify('UIC публикует англоязычную поддержку Career и Counseling Center; консультации описаны как бесплатные и конфиденциальные.', official['counsel']),
 'admissions': verify('Для UIC International Students Track с набора 2027 нужно подтверждение английского или допустимый эквивалент; общего обязательного IELTS 8.0 нет. Документы оцениваются в 200 баллов, интервью — в 100. Для Spring 2027 указаны дедлайн заявки 22.09.2026 и прибытие документов 02.10.2026.', official['admissions']),
 'money': verify('Для UIC international track тариф 2026 составляет 8 202 000 KRW за семестр, 8 416 000 KRW в первом семестре; отдельные сборы оплачиваются дополнительно. Личные расходы не включены.', official['fees']) + '\n' + verify('UIC Admissions Scholarship может покрывать tuition на четыре года; international applicants рассматриваются автоматически. Для продолжающих студентов опубликованы full, half и one-third tuition scholarships. Это не обещает оплату жилья и жизни.', official['fees']) + '\n' + verify('GKS-U 2027 опубликован NIIED как отдельный конкурс с отдельными списками университетов и программ.', official['gks']),
 'outcomes': '<Interp label="Граница данных"><p>Исходник хорошо показывает возможные траектории, но не содержит надёжной статистики employment rate, зарплат или доли UIC alumni в biomedical industry. Graduate school и известный бренд Yonsei нельзя превращать в обещание результата после бакалавриата.</p></Interp>',
 'criticism': '<Interp label="Как читать риски"><p>Язык, расстояние между кампусами, стоимость жизни и учебное давление действительно влияют на опыт. Но обобщения о «холодных корейских студентах» описывают отдельные впечатления, а не правило для всех. Сохраняю вопросы автора и добавляю конкретные точки проверки.</p></Interp>',
 'you': '<Interp label="Профиль читателя"><p>Ниже сохранён персональный разбор для biomedical/STEM абитуриента из Казахстана. Его выводы зависят от языка, бюджета, выбранного major и готовности самому искать research.</p></Interp>',
 'verdict': '<Interp label="Редакционное уточнение"><p>Acceptance rate, средний GPA и итоговые шансы не считаются подтверждёнными без сопоставимых данных для выбранного международного маршрута. Финальный verdict основан на учебном содержании, инфраструктуре, языке, бюджете и рисках.</p></Interp>',
}

def clean(text):
    text = re.sub(r'(?:uic\.)?yonsei\.ac(?:\+\d+)?', '', text, flags=re.I)
    text = re.sub(r'(?<=[.\w])(?:kstudytimes|gokoreastudy|collegesimplified|mystudy-korea|wikipedia|ielts|globaladmissions|libertify|educatly|universityworldnews|reddit|gokorea)(?:\+\d+)?\b', '', text, flags=re.I)
    # Citation debris must never remove university names or exam names in prose.
    text = re.sub(r'\b(?:yonsei|uic|kstudytimes|gokoreastudy|collegesimplified|mystudy-korea|wikipedia|ielts|globaladmissions|libertify|educatly|universityworldnews|reddit|gokorea)\+\d+', '', text, flags=re.I)
    text = re.sub(r'\.\.\.[A-Za-z0-9_-]+(?:\+\d+)?', '', text)
    text = re.sub(r'\.{2,}[A-Za-z0-9_-]+', '', text)
    text = re.sub(r'\s+([,.;:])', r'\1', text)
    text = text.replace('English-based', 'англоязычный').replace('English-taught', 'англоязычный').replace('highly competitive admissions','конкурсный приём')
    text = text.replace('Underwood International University','Underwood International College')
    text = text.replace('ASD (Applied Science and Engineering Division)', 'ISED (Integrated Science and Engineering Division)')
    text = text.replace('UIC ASD', 'UIC ISED')
    text = text.replace('1885+ years', 'история с 1885 года')
    text = text.replace('founded 1885', 'история с 1885 года')
    text = re.sub(r'English liberal arts foundation\+interdisciplinary major\+Korea / Asia context.*?English liberal arts foundation\+interdisciplinary major\+Korea / Asia context', 'англоязычная основа + междисциплинарный major + контекст Кореи и Азии', text, flags=re.S)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_section(sid, title, start, end, n):
    raw = '\n'.join(reader.pages[i].extract_text(extraction_mode='layout') or '' for i in range(start, end))
    lines = [re.sub(r'\s+', ' ', x).strip() for x in raw.splitlines()]
    raw = '\n'.join(lines)
    for h in sorted(headings, key=len, reverse=True):
        raw = re.sub(r'(?m)^'+re.escape(h)+r'\s*$', '\n@@'+h+'@@\n', raw)
    raw = re.sub(r'(?m)^UNKNOWN\s*$', 'UNKNOWN:', raw)
    raw = re.sub(r'(?m)^YONSEI UNIVERSITY.*$', '', raw)
    raw = re.sub(r'\s*(FACT:|INTERPRETATION:|UNKNOWN:|STUDENT EXPERIENCE:)\s*', r'\n\1 ', raw)
    tokens = re.split(r'(@@[^@]+@@|\bFACT:|\bINTERPRETATION:|\bUNKNOWN:|\bSTUDENT EXPERIENCE:)', raw)
    out = [f'<Section num="{n:02}" id="{sid}" title="{title}">', notes[sid]]
    mode = 'Interp' if sid == 'verdict' else 'Fact'
    for token in tokens:
        token = token.strip()
        if not token: continue
        if token.startswith('@@'):
            h = token[2:-2]
            if h in headings: out.append('<h3>'+esc(headings[h])+'</h3>')
            continue
        if token in ('FACT:','INTERPRETATION:','UNKNOWN:','STUDENT EXPERIENCE:'):
            mode = {'FACT:':'Fact','INTERPRETATION:':'Interp','UNKNOWN:':'Unknown','STUDENT EXPERIENCE:':'Interp'}[token]
            continue
        if not token or token.startswith('PAGE '): continue
        chunks = re.split(r'\n\s*\n|(?=[●•])|\n(?=\d+\.\s)', token)
        body=[]; inlist=False
        for chunk in chunks:
            chunk=clean(chunk)
            if not chunk: continue
            bullet = chunk.startswith(('●', '•', '- ')) or bool(re.match(r'^\d+\.\s', chunk))
            chunk = re.sub(r'^(?:[●•]|- |\d+\.\s)\s*', '', chunk).strip()
            if bullet and not inlist: body.append('<ul>'); inlist=True
            if not bullet and inlist: body.append('</ul>'); inlist=False
            body.append(('<li>' if bullet else '<p>')+esc(chunk)+('</li>' if bullet else '</p>'))
        if inlist: body.append('</ul>')
        if body:
            label = ' label="Из исследования"' if mode == 'Fact' else ''
            out.append(f'<{mode}{label}>'+''.join(body)+f'</{mode}>')
    out.append('</Section>')
    return '\n\n'.join(out)

body = [parse_section(sid, title, start, end, n) for n,(sid,title,start,end) in enumerate(sections,1)]
result = meta + '\n\n' + '\n\n'.join(body)
# Editorial corrections apply to both the website and print edition.
result = re.sub(r'<Fact[^>]*><p>Yonsei (?:University generally requires:|требует:).*?</Fact>', verify('Для UIC нет универсального опубликованного порога GPA или SAT/ACT. Набор 2027 требует подтверждения английского либо допустимого эквивалента; IELTS 8.0 не является общим обязательным минимумом. Требования других колледжей необходимо читать отдельно.', official['admissions']), result, flags=re.S)
result = re.sub(r'<li>English proficiency \(TOEFL.*?</li>', '<li>Готовность учиться на английском; конкретные документы зависят от маршрута и года набора.</li>', result)
result = re.sub(r'<Interp><p>7/10 — Competitive,.*?</Interp>', '<Interp><p>Поступление конкурсное. Сопоставимых данных недостаточно, чтобы объявлять Yonsei более доступным, чем NYUAD, или обещать хорошие шансы по одним оценкам и английскому. Сначала выбирай конкретный маршрут UIC и проверяй его требования.</p></Interp>', result)
def replace_block(needle, replacement):
    global result
    result = re.sub(r'<(Fact|Interp)(?: [^>]*)?>.*?</\1>', lambda m: replacement if needle in m[0] else m[0], result, flags=re.S)
replace_block('Путь Основная идея', '<Fact label="Маршруты обучения"><p>Для международного абитуриента важно различать несколько программ:</p><ul><li><b>Regular International Undergraduate Track:</b> поступление в обычные колледжи Yonsei; язык и условия определяются программой.</li><li><b>Underwood International College (UIC):</b> англоязычный бакалавриат с моделью liberal arts.</li><li><b>Global Leaders College (GLC):</b> отдельный колледж, преимущественно с обучением на корейском.</li><li><b>Summer School / exchange:</b> временная мобильность, а не полный бакалавриат.</li></ul></Fact>')
replace_block('Division Примеры majors', '<Fact label="Структура UIC"><p>В актуальном меню UIC выделены три division:</p><ul><li><b>Underwood Division:</b> Comparative Literature and Culture, Economics, International Studies, Political Science and International Relations, Life Science and Biotechnology.</li><li><b>Humanities, Arts, and Social Sciences Division:</b> Asian Studies, Culture and Design Management, Information and Interaction Design, Creative Technology Management, Justice and Civil Leadership, Quantitative Risk Management, Science, Technology, and Policy, Sustainable Development and Cooperation.</li><li><b>Integrated Science and Engineering Division:</b> Nano Science and Engineering, Energy and Environmental Science and Engineering, Bio-Convergence.</li></ul><p><Src href="'+official['faq']+'">Официальная структура UIC</Src></p></Fact>')
replace_block('Компонент Что университет хочет дать', '<Interp><p>Модель Yonsei соединяет несколько преимуществ: городской контекст Сеула, корейскую сеть SKY, англоязычный UIC, медицинскую инфраструктуру Severance, большой выбор дисциплин и международную мобильность.</p><p>Главный компромисс: международный колледж существует внутри корейского университета. Это интересно человеку, который хочет связать обучение с Кореей или Восточной Азией; ожидание полностью англоязычной среды за пределами занятий может не оправдаться.</p></Interp>')
(ROOT/'src/content/universities/yonsei.mdx').write_text(result, encoding='utf-8')
print(f'Created yonsei.mdx: {len(body)} sections, {len(result)} characters')
