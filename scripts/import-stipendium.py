"""Import the author's full scholarship research, with explicit editorial corrections."""
from pathlib import Path
import re, html, json
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
reader=PdfReader(r'C:/Users/PC/Downloads/STIPENDIUM HUNGARICUM SCHOLARSHIP.pdf')
sources={
 'about':('О программе и финансовом пакете','https://stipendiumhungaricum.hu/about/'),
 'apply':('Официальный маршрут подачи 2026/27','https://stipendiumhungaricum.hu/apply/'),
 'call':('Call for Applications: BA, MA, one-tier, 2026/27','https://stipendiumhungaricum.hu/wp-content/uploads/2025/10/BA_MA_OTM_Call_for_Applications_2026_27.pdf'),
 'partners':('Sending Partners: Kazakhstan','https://stipendiumhungaricum.hu/partners/'),
 'kz':('Центр международных программ Казахстана','https://bolashak.gov.kz/ru'),
 'oldquota':('Объявление Казахстана для 2025/26 (исторический контекст)','https://www.gov.kz/memleket/entities/sci/documents/details/750764?lang=ru'),
 'rules':('Operational Regulations от 31.08.2026','https://stipendiumhungaricum.hu/documents/stipendium_hungaricum/OR/SH_OR.pdf'),
 'work':('OIF: пребывание и работа студентов','https://www.oif.gov.hu/factsheets/residence-of-the-student-pupil'),
 'stats':('Официальная статистика заявок 2026/27','https://stipendiumhungaricum.hu/news/more-applicants-than-ever-in-the-2026-27-application-period/'),
 'biology':('University of Debrecen: Biology BSc','https://edu.unideb.hu/p/biology-bsc'),
 'exam':('University of Debrecen: FAQ по SH','https://edu.unideb.hu/p/faq-stipendium-hungaricum-scholarship'),
 'catalog':('Каталог программ DreamApply','https://apply.stipendiumhungaricum.hu/'),
 'holders':('Материалы для стипендиатов','https://stipendiumhungaricum.hu/scholarship-holders/'),
 'phd':('Отдельный конкурс PhD, 2026/27','https://stipendiumhungaricum.hu/wp-content/uploads/2025/10/PhD_Call_for_Applications_2026_27.pdf'),
}
def esc(s):return html.escape(s,quote=False).replace('{','&#123;').replace('}','&#125;')
def blk(kind,text,key=None,label=None):
    link=f' <Src href="{sources[key][1]}">{sources[key][0]}</Src>' if key else ''
    attr=f' label="{label}"' if label else ''
    return f'<{kind}{attr}><p>{esc(text)}{link}</p></{kind}>'
def checked(text,key):return blk('Fact',text,key,'Проверено')
sections=[('identity','Идентичность программы',1,5),('academics','Что ты будешь изучать',6,10),('research','Исследования',11,14),('life','Жизнь в Венгрии',15,19),('admissions','Поступление из Казахстана',20,24),('money','Деньги и личный бюджет',25,29),('outcomes','Карьера и выпускники',30,34),('criticism','Критика и риски',35,39),('you','Ты × программа',40,43),('verdict','Итоговый вердикт',44,47)]
heading_map={
 'Identity':'О программе','История':'История','Философия и миссия':'Философия и миссия','Что программа пытается построить':'Что программа пытается построить','Реальные ценности':'Реальные ценности',
 'Academic structure':'Структура обучения','Curriculum':'Учебная программа','Flexibility':'Гибкость','Major (для biomedical sciences)':'Направления для биомедицины','Core':'Обязательная подготовка','Electives':'Курсы по выбору','Global opportunities':'Международные возможности',
 'Research philosophy':'Подход к исследованиям','Labs & centers':'Лаборатории и центры','Undergraduate research':'Исследования на бакалавриате','Professors':'Преподаватели','Research opportunities':'Исследовательские возможности',
 'Campus':'Города и кампусы','Residential life':'Проживание','Clubs':'Клубы','Traditions':'Традиции','Culture':'Культура','Community':'Сообщество',
 'Employment':'Трудоустройство','Graduate school':'Продолжение образования','Alumni':'Выпускники','Network':'Профессиональные связи','Career Support':'Карьерная поддержка',
 'What can be bad?':'Что может не подойти','Student complaints':'Вопросы к студенческому опыту','Structural problems':'Структурные ограничения','Cultural problems':'Культурная адаптация','Financial Sustainability':'Финансовая устойчивость','Additional Risks':'Дополнительные риски',
 'Why you fit':'Кому подходит','Where you don\'t fit':'Кому может не подойти','What you could do there':'Что можно делать во время учёбы','What you would miss':'Чего может не хватать'}
noise=r'(?:stipendiumhungaricum|opportunitiesforyouth|guides\.scholarshipunion|itk\.ppke|persmind|applykite|world-study|leapscholar|learnviahub|europescholarships|cscpath|visanil|note)'
def clean(s):
    s=re.sub(noise+r'(?:\+\d+)?','',s,flags=re.I)
    s=re.sub(r'\s+',' ',s).strip()
    s=s.replace('st ипенди','стипенди').replace('  ',' ').replace(' .','.')
    return s
def revise(s,kind):
    # Correct at paragraph/list-item level so unrelated source detail is preserved.
    if 'исторического документа' in s:return ('Происхождение названия от документа «Hungaricum» из исходника не подтверждено официальной историей программы; этот тезис не используется.', 'Unknown')
    if re.search(r'acceptance rate|\b(?:17\.8|22–25|22-25|25|22):1|~5,000|4\.4–5\.6|4\.4%|5\.6%',s,re.I):return ('Конкурс высокий, но отношение общего числа заявок к предположительному числу грантов не является подтверждённой вероятностью поступления. Для Казахстана и конкретного направления нужны отдельные данные.', 'Interp')
    if re.search(r'Казахстан.*(?:partner country|проверить|списке|если)|Kazakhstan.*(?:partner country|проверить|eligible)',s,re.I):return ('Казахстан включён в Sending Partners. Участие страны подтверждено; требования национального отбора и квоту своего набора проверяй у Центра международных программ.', 'Interp')
    if re.search(r'24\s*(?:hours|час)|full-time во время каникул',s,re.I):return ('Для студенческого ВНЖ действуют пределы работы: до 30 часов в неделю в учебный период и полный день максимум 90 дней в году вне учебного периода. Возможность найти работу не гарантирована.', 'Interp')
    if 'EUR 5–8/hour' in s or 'EUR 5–8' in s:return ('Достоверная единая ставка студенческой подработки не установлена. Доход зависит от вакансии, языка, графика и налогов; будущую зарплату нельзя считать гарантированным финансированием.', 'Unknown')
    if re.search(r'Erasmus\+|Erasmus \+',s):return ('Международные поездки и обмены требуют проверки совместимости с SH и разрешения университета. Обычный семестр Erasmus+ с сохранением выплат не следует считать гарантированной частью пакета; см. раздел о международных возможностях.', 'Interp')
    if re.search(r'EUR 210|EUR 110|EUR 100|USD 120|USD 220',s):return ('Финансовый пакет нужно считать в HUF: выплата на жизнь для BA/MA/one-tier составляет 43 700 в месяц; жильё предоставляется в общежитии либо компенсируется отдельной выплатой 40 000. Полный личный бюджет может быть выше.', 'Interp')
    if 'признаётся globally' in s or 'European degree' in s and 'globally' in s:return ('Диплом может использоваться для дальнейшей учёбы или карьеры за рубежом, но решение принимает конкретный вуз, работодатель или орган признания. Для регулируемых профессий действуют отдельные процедуры.', 'Interp')
    if 'не related' in s or 'не Indo-European' in s:return ('Венгерский относится к уральской языковой семье. Он отличается от русского и английского; повседневное освоение языка стоит включить в план адаптации.', 'Interp')
    if 'не могут apply напрямую' in s:return ('Для обычного маршрута из Казахстана необходимо выполнить национальный этап: подача в DreamApply не заменяет номинацию Sending Partner.', 'Interp')
    if 'полностью финансируем' in s.lower() or 'fully funded' in s.lower():
        s=re.sub(r'полностью финансируемая программа','программа с покрытием обучения и поддержкой расходов на жизнь',s,flags=re.I)
        s=re.sub(r'полностью финансируемые возможности обучения','возможности обучения с покрытием tuition и поддержкой расходов на жизнь',s,flags=re.I)
        s=re.sub(r'полностью финансируемая возможность','возможность учиться с покрытием tuition и поддержкой расходов на жизнь',s,flags=re.I)
        s=re.sub(r'fully funded','tuition + living support',s,flags=re.I)
        kind='Interp'
    s=s.replace('28 венгерских университетов','Венгерские университеты').replace('28 университетов','Университеты')
    s=s.replace('28 венгерских университетах','венгерских университетах').replace('28 венгерскими университетами','венгерскими университетами')
    if '18 credits' in s:return ('Для BA/MA/one-tier действует минимум в среднем 18 кредитов за последние два активных семестра; более строгие условия могут быть установлены вузом. Докторские программы имеют отдельные требования.', 'Interp')
    if '5,000+' in s or '80,000' in s or '4,500' in s:return ('Масштаб программы вырос с момента запуска. Число заявок, новых стипендиатов, действующих студентов и выпускников — разные показатели; смешивать их при оценке сообщества нельзя.', 'Interp')
    if 'многие программы только на венгерском' in s or 'многие программы только на Hungarian' in s:
        s=re.sub(r'многие программы только на венгерском[^.]*','язык конкретной программы необходимо проверить в каталоге',s,flags=re.I);kind='Interp'
    if any(w in s.lower() for w in ['mixed reviews','жалуют','less open','slow','quality variation','могут быть','очень сложен','недостаточно','нельзя apply','не могут apply','не могут напрямую']):kind='Interp'
    s=s.replace('на трёх уровнях','на нескольких уровнях').replace('PhD (Doctoral): 3–4 года','PhD (Doctoral): отдельный докторский трек')
    return s,kind

notes={
'identity':[checked('Stipendium Hungaricum создана правительством Венгрии в 2013 году; программу координирует Tempus Public Foundation. Это финансирование обучения в разных вузах, а не самостоятельный университет.','about'),checked('Казахстан указан среди Sending Partners; ответственная организация — Center for International Programs «Bolashak».','partners'),checked('На 2026/27 поступило 113 806 заявок. Эта цифра характеризует общий спрос, но не индивидуальные шансы абитуриента.','stats')],
'academics':[checked('В официальном маршруте 2026/27 указаны около 30 вузов и более 900 программ, но в заявке допускаются только два выбора. Доступность зависит от страны и уровня обучения.','apply'),checked('Biology BSc в University of Debrecen сочетает естественно-научную подготовку с лабораторной работой. Это пример конкретной программы; участие выбранного направления в SH необходимо проверить отдельно.','biology'),blk('Interp','SH не устанавливает общего Core Curriculum для всех вузов. Списки дисциплин ниже — ориентиры из авторского исследования, а не единый обязательный учебный план.')],
'research':[blk('Interp','Наличие исследовательского центра в городе не означает доступ каждого бакалавра в его лабораторию. Стипендия финансирует обучение; вход в научную группу определяется руководителем и правилами вуза.'),blk('Interp','Названия лабораторий и тематик ниже сохранены как направления дальнейшего поиска. Перед выбором проверь актуальный состав группы, приём undergraduate студентов, язык работы и возможную оплату.')],
'life':[blk('Interp','У программы нет одного кампуса или единого студенческого опыта. Разница между конкретными общежитиями и факультетами может быть важнее, чем общая разница между городами.'),checked('В 2026/27 пакет жилья — место в общежитии либо вклад в аренду 40 000 HUF в месяц. Эти два варианта не суммируются.','about')],
'outcomes':[blk('Unknown','В исходнике нет сопоставимой статистики трудоустройства, зарплат и поступления в PhD по всем стипендиатам. Поэтому ниже описаны возможные направления карьеры, а не гарантированные результаты.'),blk('Interp','Если цель — врачебная практика, заранее уточни признание квалификации, язык и лицензирование в стране работы. Финансирование медицинского образования само по себе не создаёт права на практику в любой стране.')],
'criticism':[blk('Interp','Раздел помогает задавать вопросы до принятия предложения. Утверждения о «закрытых местных студентах» или «медленной администрации» нельзя переносить на всю Венгрию: конкретного репрезентативного исследования в исходнике нет.'),checked('По данным OIF обладатель студенческого ВНЖ может работать до 30 часов в неделю в учебный период и полный день максимум 90 дней в году вне него.','work')],
'you':[blk('Interp','Этот раздел написан для biomedical / STEM абитуриента из Казахстана. Сначала оцени программу и бюджет, затем название стипендии. Финальная доступность зависит от национальной номинации и решения венгерской стороны.')]
}

def parse(sid,start,end):
    if sid in ('admissions','money','verdict'):
        return (ROOT/f'scripts/editions/stipendium-{sid}.mdx').read_text(encoding='utf-8')
    raw='\n'.join(reader.pages[i].extract_text(extraction_mode='layout') or '' for i in range(start,end))
    lines=[re.sub(r'\s+',' ',line).strip() for line in raw.splitlines()]
    raw='\n'.join(line for line in lines if not re.match(r'^STIPENDIUM HUNGARICUM.*Раздел',line))
    for title in sorted(heading_map,key=len,reverse=True):raw=re.sub(r'(?m)^'+re.escape(title)+r'\s*$', '\n@@'+title+'@@\n',raw)
    tokens=re.split(r'(@@[^@]+@@|FACT:|INTERPRETATION:|UNKNOWN:)',raw)
    out=list(notes.get(sid,[]));kind='Interp'
    for token in tokens:
        token=token.strip()
        if not token:continue
        if re.match(r'^\d+:\s*(Student Life|YOU|UNIVERSITY)',clean(token)):continue
        if token.startswith('@@'):
            title=heading_map[token[2:-2]]
            if title!='О программе':out.append('<h3>'+title+'</h3>')
            continue
        if token in ('FACT:','INTERPRETATION:','UNKNOWN:'):
            kind={'FACT:':'Fact','INTERPRETATION:':'Interp','UNKNOWN:':'Unknown'}[token];continue
        if sid=='identity' and token.startswith('Заявляемая'):
            out.append(blk('Interp','Основной компромисс программы: освобождение от платы за обучение расширяет доступ, но не снимает национальный конкурс и личные расходы. Международное сообщество создаёт связи, но качество преподавания и поддержки определяется вузом.'));continue
        chunks=re.split(r'\n\s*\n|(?=[●○•])|\n(?=\d+\.\s)',token)
        items=[];inlist=False;blockkind=kind
        for chunk in chunks:
            chunk=clean(chunk)
            if not chunk:continue
            bullet=bool(re.match(r'^[●○•]|^\d+\.\s',chunk))
            chunk=re.sub(r'^(?:[●○•]|\d+\.\s)\s*','',chunk)
            chunk,newkind=revise(chunk,kind)
            if newkind=='Interp' and blockkind=='Fact':blockkind='Interp'
            if newkind=='Unknown':blockkind='Unknown'
            if bullet and not inlist:items.append('<ul>');inlist=True
            if not bullet and inlist:items.append('</ul>');inlist=False
            items.append(('<li>' if bullet else '<p>')+esc(chunk)+('</li>' if bullet else '</p>'))
        if inlist:items.append('</ul>')
        if items:out.append(f'<{blockkind}'+(' label="Из исследования"' if blockkind=='Fact' else '')+'>'+''.join(items)+f'</{blockkind}>')
    if sid=='academics':
        out.extend(['<h3>Что важно для сохранения стипендии</h3>',checked('Для BA/MA/one-tier действует минимум в среднем 18 кредитов за два последних активных семестра; вуз может устанавливать более строгие требования. Для PhD этот минимум не применяется. В первый год предусмотрен обязательный курс венгерского языка и культуры.','rules'),checked('Регламент 31.08.2026 разрешает согласованные с вузом учебные поездки до 30 дней с сохранением выплат. Для более длительной мобильности действуют отдельные условия и исключения: обычный Erasmus-семестр не гарантирован.','rules')])
    return '\n\n'.join(out)

meta='''---
name: Stipendium Hungaricum
country: Венгрия
thesis: "Государственная стипендия с покрытием обучения и поддержкой расходов на жизнь. Как выбрать программу, пройти отбор из Казахстана и посчитать личный бюджет."
accent: '#245A4B'
accentDark: '#89BBA8'
profile: "биомедицина / STEM, абитуриент из Казахстана"
updated: 2026-09-14
cycle: "Проверены условия 2026/27; следующий конкурс отдельно"
pdf: /downloads/stipendium-hungaricum.pdf
sources:
'''
for label,url in sources.values():meta+='  - {label: '+json.dumps(label,ensure_ascii=False)+', url: '+json.dumps(url)+'}\n'
meta+='---\n\n'
parts=[]
for i,(sid,title,start,end) in enumerate(sections,1):parts.append(f'<Section num="{i:02d}" id="{sid}" title="{title}">\n\n'+parse(sid,start,end)+'\n\n</Section>')
target=ROOT/'src/content/scholarships/stipendium-hungaricum.mdx';target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(meta+'\n\n'.join(parts)+'\n',encoding='utf-8')
print('Imported 10 chapters:',target.stat().st_size,'bytes')
