from pathlib import Path
import re, json, html
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
reader=PdfReader(r'C:/Users/PC/Downloads/Westlake University .pdf')
brochure='https://ugadmissions.westlake.edu.cn/images/Admissions_download.pdf'
history='https://en.westlake.edu.cn/about/facts_history/'
news='https://en.westlake.edu.cn/news_events/westlakenews/UniversityNews/202308/t20230829_35900.html'
majors='https://en.westlake.edu.cn/news_events/westlakenews/Study_at_Westlake/202602/t20260212_64855.html'
meta=dict(name='Westlake University',city='Ханчжоу',country='Китай',countryCode='CN',founded=2018,
 thesis='Молодой исследовательский университет в Ханчжоу: ранняя работа в лабораториях, небольшие наборы и фундаментальная STEM-подготовка. Стипендии на обучение доступны, но расходы на четыре года нужно считать по личному предложению университета.',
 accent='#18626A',accentDark='#83C8C9',profile='biomedical / STEM, абитуриент из Казахстана, требуется финансовая помощь',updated='2026-09-12',
 acceptanceRate=None,acceptanceNote='Подтверждённой статистики приёма иностранных бакалавров в исходнике нет.',satRange=None,actRange=None,testPolicy='optional',separateCollegeAdmission=False,
 costOfAttendance=None,meetsFullNeed=False,aidForInternationals=True,avgGrant=None,avgPackage=None,meritAid=True,needBlind=True,
 strengths=['биология','AI','инженерия','химия','математика','физика'],campusType='big city',climate='влажный климат, жаркое лето и прохладная зима',
 fit={k:dict(score=s,note=n) for k,s,n in [('academic',3,'высокое для STEM'),('research',4,'очень высокий потенциал; доступ уточнять'),('intellectual',3,'высокое для научной траектории'),('culture',2,'зависит от языка и предпочтений'),('financial',2,'не определено до личного предложения'),('admissions',3,'селективность без подтверждённого процента')]},
 sources=dict(official=[dict(label='Буклет международного бакалавриата Fall 2026',url=brochure),dict(label='История Westlake',url=history),dict(label='Программы для иностранных студентов, 2026',url=majors),dict(label='Общественное и частное финансирование',url=news)],data=[dict(label='Исходный авторский разбор Westlake, предоставленный для публикации')],reviews=[],news=[]),
 sourceCaveat='Сверено 12 сентября 2026 года: история, перечень программ для иностранцев, заявление о need-blind приёме, стипендии и требования из буклета Fall 2026. Это выборочная проверка, а не аудит каждого утверждения. Блоки «Из исследования» сохранены из авторского материала и отдельно не подтверждены. PhD и летние программы не описывают условия бакалавриата. Данные наборов 2026 года не являются дедлайнами набора 2027. Прочерк в полной стоимости означает отсутствие проверенного общего бюджета, а не бесплатное обучение.')

sections=[('identity','Идентичность',1,4),('academics','Академика',5,10),('research','Исследования',11,15),('life','Жизнь на кампусе',16,19),('admissions','Поступление',20,23),('money','Деньги',24,27),('outcomes','Карьера и выпускники',28,31),('criticism','Критика и риски',32,35),('you','Ты × университет',36,39),('verdict','Итоговый вердикт',40,44)]
headings=['История','Философия и миссия','Что университет пытается построить','Реальные ценности','Academic structure','Curriculum','Flexibility','Major (для biomedical sciences)','Biological Sciences Major','Biomedical Engineering Major','Quantitative Biology and Complex Systems','Core','Electives','Global opportunities','Research philosophy','Labs & centers','Undergraduate research','Professors','Research opportunities','Campus','Residential life','Clubs','Traditions','Culture','Community','Who are they looking for?','Academic profile','Essays','ECs (Extracurriculars)','Interview','Demonstrated interest','Application Process','Cost','Financial aid','Full ride','Merit','International students','Employment','Graduate school','Alumni','Network','Career Support','What can be bad?','Student complaints','Structural problems','Cultural problems','Academic Freedom Concerns','Additional Risks','Why you fit',"Where you don't fit",'What you could do there','What you would miss','Academic fit','Research fit','Intellectual fit','Culture fit','Financial fit','Admissions fit','Overall fit']
translations={'Academic structure':'Структура обучения','Curriculum':'Учебная программа','Flexibility':'Гибкость','Core':'Общая подготовка','Electives':'Курсы по выбору','Global opportunities':'Международные возможности','Research philosophy':'Подход к исследованиям','Labs & centers':'Лаборатории и центры','Undergraduate research':'Исследования на бакалавриате','Professors':'Преподаватели','Research opportunities':'Исследовательские программы','Campus':'Кампус','Residential life':'Проживание','Clubs':'Клубы','Traditions':'Традиции','Culture':'Культура','Community':'Сообщество','Who are they looking for?':'Кого ищет университет','Academic profile':'Академический профиль','Essays':'Эссе','Interview':'Интервью','Demonstrated interest':'Проявленный интерес','Application Process':'Подача заявки','Cost':'Стоимость','Financial aid':'Финансовая помощь','Full ride':'Полное финансирование','Merit':'Стипендии за достижения','International students':'Иностранные студенты','Employment':'Трудоустройство','Graduate school':'Продолжение образования','Alumni':'Выпускники','Network':'Профессиональные связи','Career Support':'Карьерная поддержка','What can be bad?':'Что может не подойти','Student complaints':'Отзывы и вопросы студентов','Structural problems':'Структурные ограничения','Cultural problems':'Культурные особенности','Academic Freedom Concerns':'Академическая свобода','Additional Risks':'Дополнительные риски','Why you fit':'Кому подходит',"Where you don't fit":'Кому может не подойти','What you could do there':'Что можно делать в университете','What you would miss':'Чего может не хватать','Academic fit':'Академическое соответствие','Research fit':'Исследовательское соответствие','Intellectual fit':'Интеллектуальное соответствие','Culture fit':'Культурное соответствие','Financial fit':'Финансовое соответствие','Admissions fit':'Сложность поступления','Overall fit':'Общий вывод'}

def esc(s):
 return html.escape(s,quote=False).replace('{','&#123;').replace('}','&#125;').replace('~','≈')
def verified(text,url=brochure):
 return '<Fact label="Проверено"><p>'+esc(text)+' <Src href="'+url+'">Официальный источник</Src></p></Fact>\n'
notes={
'identity':verified('Westlake учреждён в 2018 году; первый бакалаврский набор пришёл в июле 2022 года. Институт-предшественник зарегистрирован в декабре 2015-го, церемония основания состоялась в декабре 2016-го.',history)+verified('Университет описывает свою модель как некоммерческую частную исследовательскую организацию с общественным и частным финансированием. Частный статус не означает независимости от государства или отсутствия государственного участия.',news),
'academics':verified('Для иностранных бакалавров указаны семь программ: Biological Sciences, Chemistry, Mathematics and Applied Mathematics, Physics, Artificial Intelligence, Electronic and Information Engineering, Materials Science and Engineering. Отдельные бакалаврские Mechanical Engineering и Biomedical Engineering из исходного списка не подтверждены этим перечнем.',majors)+verified('Буклет Fall 2026 указывает выбор major после третьего семестра. Раннее описание на сайте говорит о первых двух годах общей подготовки; для своего набора уточняй точный срок. Обучение Mandarin длится минимум два года.'),
'research':'<Interp label="Уровень программы"><p>Летние стажировки для уже обучающихся в вузах и программы PhD описаны ниже отдельно от бакалавриата. Их наличие не гарантирует школьнику зачисление или место в лаборатории. Основатели, попечители и приглашённые учёные также не равнозначны действующим научным руководителям.</p></Interp>\n',
'life':verified('Буклет описывает около 40 студенческих групп, проживание бакалавров на кампусе и семестр в партнёрском университете. Блок общежития включает 4–5 спален с общими ванной и гостиной. Это описание инфраструктуры, а не гарантия конкретной комнаты.'),
'admissions':verified('Fall 2026: SAT/ACT и другие стандартизированные результаты необязательны; нужны подтверждение английского, два эссе, три рекомендации (консультант и два учителя), интервью по приглашению. Заявления о 1500 словах и исследовательском предложении ниже относятся к PhD.'),
'money':verified('Буклет Fall 2026: обучение — 350 000 CNY/год, общежитие — 1 800–2 200 CNY/год; это не полный бюджет жизни. Указаны need-blind приём и полные/частичные стипендии на обучение с учётом нужды и достижений. Покрытие остальных расходов и продление нужно проверить в личном предложении.'),
'outcomes':'<Interp label="Как читать результаты"><p>Перечни возможных профессий PhD не являются статистикой трудоустройства бакалавров. Здесь нет подтверждённых долей трудоустройства, зарплат или поступлений выпускников в другие университеты. Молодость программы означает короткую историю наблюдений, а не автоматически слабое образование.</p></Interp>\n',
'criticism':'<Unknown label="Границы проверки"><p>Обобщения исходника о политике, академической свободе, генетических исследованиях и интеграции не подтверждены конкретными документами или исследованиями Westlake. Они сохранены как вопросы для оценки среды, а не юридические выводы или измеренные характеристики университета. Числа 17 и 30+ национальностей, а также 251 бакалавр не имеют согласованной даты и выборки.</p></Unknown>\n',
'you':'<Interp label="Уточнение профиля"><p>Сценарии ниже — авторские варианты для biomedical/STEM. Quantitative Biology and Complex Systems описывает PhD-траекторию; доступный бакалаврский выбор следует сверять с перечнем в разделе «Академика».</p></Interp>\n',
'verdict':'<Interp label="Вердикт автора"><p>Ниже сохранён авторский вывод с уточнениями после проверки. Высокая оценка исследовательского потенциала не означает гарантированного доступа в лабораторию; финансовая доступность зависит от индивидуальной стипендии.</p></Interp>\n'
}

def clean(s):
 s=re.sub(r'\s+',' ',s).strip()
 # Remove dangling retrieval labels, never invent URLs for them.
 s=re.sub(r'(?:china-admissions|lifesciences\.westlake\.edu|westlake\.edu|universityworldnews|academicjobs|educations|gradualin|scribd|youtube)(?:\+\d+)?','',s)
 s=s.replace('первая частная исследовательская университет','частный исследовательский университет')
 s=s.replace('Не зависит от государства, а от philanthropic funding','Получает общественное и частное финансирование, включая philanthropic funding')
 s=s.replace('Major выбирается в конце sophomore year','В буклете Fall 2026 major выбирается после третьего семестра')
 s=s.replace('major выбирается в конце sophomore year','по буклету Fall 2026 major выбирается после третьего семестра')
 s=s.replace('major в конце второго года','major после третьего семестра (буклет Fall 2026)')
 s=s.replace('major после двух лет','major после общей подготовки')
 s=s.replace('В 2026 году Westlake имеет 251 undergraduate student и 2,190 doctoral students.','Исходник приводит 251 бакалавра и 2 190 докторантов; дата и актуальность этой выборки отдельно не подтверждены.')
 return s.strip()

parts=[]; block_count=0
for num,(sid,title,start,end) in enumerate(sections,1):
 # Layout extraction preserves list boundaries and avoids one-word lines.
 text='\n'.join(reader.pages[i].extract_text(extraction_mode='layout') for i in range(start,end))
 lines=[]
 for line in text.splitlines():
  line=re.sub(r'\s+',' ',line).strip()
  if not line: lines.append(''); continue
  if line.startswith('WESTLAKE UNIVERSITY'): continue
  lines.append(line)
 text='\n'.join(lines)
 # split on headings/semantic labels even when extraction puts two on one line
 for h in sorted(headings,key=len,reverse=True):
  text=re.sub(r'(?m)^'+re.escape(h)+r'\s*$', '\n@@'+h+'@@\n',text)
 text=re.sub(r'\s*(FACT:|INTERPRETATION:|UNKNOWN:|STUDENT EXPERIENCE:)\s*',r'\n\1 ',text)
 tokens=re.split(r'(@@[^@]+@@|\bFACT:|\bINTERPRETATION:|\bUNKNOWN:|\bSTUDENT EXPERIENCE:)',text)
 out=[f'<Section num="{num:02}" id="{sid}" title="{title}">',notes[sid]]
 mode='Interp' if sid=='verdict' else 'Fact'
 for token in tokens:
  token=token.strip()
  if not token: continue
  if token.startswith('@@'):
   h=token[2:-2]; out.append('<h3>'+esc(translations.get(h,h))+'</h3>'); continue
  if token in ['FACT:','INTERPRETATION:','UNKNOWN:','STUDENT EXPERIENCE:']:
   mode={'FACT:':'Fact','INTERPRETATION:':'Interp','UNKNOWN:':'Unknown','STUDENT EXPERIENCE:':'Interp'}[token]; continue
  # Keep paragraph breaks and list items; continuation lines are joined.
  chunks=re.split(r'\n\s*\n|(?=●)',token)
  body=[]; inlist=False
  for chunk in chunks:
   chunk=clean(chunk)
   if not chunk: continue
   bullet=chunk.startswith('●'); chunk=chunk.lstrip('● ').strip()
   if bullet and not inlist: body.append('<ul>'); inlist=True
   if not bullet and inlist: body.append('</ul>'); inlist=False
   body.append(('<li>' if bullet else '<p>')+esc(chunk)+('</li>' if bullet else '</p>'))
  if inlist: body.append('</ul>')
  if not body: continue
  label=' label="Из исследования"' if mode=='Fact' else ''
  out.append(f'<{mode}{label}>'+''.join(body)+f'</{mode}>'); block_count+=1
 out.append('</Section>'); parts.append('\n\n'.join(out))

result='---\n'+ '\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in meta.items())+'\n---\n\n'+'\n\n'.join(parts)
# Correct conflicting factual wording locally; preserve the original PDF externally.
result=result.replace('Westlake предлагает 8 undergraduate majors через 4 secondary colleges:', 'В исходнике перечислены восемь направлений, но международный каталог 2026 подтверждает семь. Ниже исторический список исходника; два неподтверждённых названия отмечены:')
result=result.replace("Bachelor's in Mechanical Engineering", "Mechanical Engineering — отдельный international bachelor не подтверждён")
result=result.replace("Bachelor's in Biomedical Engineering", "Biomedical Engineering — отдельный international bachelor не подтверждён")
result=result.replace('Biomedical Engineering — один из 8 undergraduate majors.', 'Отдельный Biomedical Engineering bachelor в проверенном международном перечне не указан; исследовательское направление не следует считать отдельным доступным major.')
result=result.replace('Есть ли interview для undergraduate applicants.', 'Интервью для undergraduate подтверждено буклетом Fall 2026; проводится по приглашению.')
result=result.replace('Есть ли need-based или merit-based financial aid для undergraduates.', 'Полные и частичные tuition scholarships для undergraduates подтверждены; размер индивидуален.')
result=result.replace('Есть ли merit scholarships для undergraduates.', 'Merit scholarships для undergraduates подтверждены; условия конкретного предложения требуют уточнения.')
result=result.replace('Tuition для undergraduate international students.', 'Обучение для international undergraduates: 350 000 CNY/год по буклету Fall 2026; полная стоимость жизни выше.')
result=result.replace('фундаментальная наука+ research+technology+innovation фундаментальная наука+ research+technology+innovation', 'фундаментальная наука + research + technology + innovation')
# Rebuild the one multi-column source table that cannot be read in extraction order.
table='<Tbl><table><thead><tr><th>Идея</th><th>Что описывает автор</th><th>Что стоит проверить</th></tr></thead><tbody>'
for a,b,c in [('Исследования','Первоначальный фокус на PhD и лабораториях','Реальный доступ бакалавра к научному руководителю'),('Научные достижения','Основатели-учёные и международный поиск преподавателей','Действующий состав faculty, а не список основателей'),('Международность','Англоязычные программы и летние школы','Актуальный состав бакалавров: 17 и 30+ в исходнике не сопоставимы'),('Междисциплинарность','Биология, AI и количественные методы','Различать undergraduate major, PhD и тему лаборатории')]:
 table+='<tr>'+''.join('<td>'+x+'</td>' for x in [a,b,c])+'</tr>'
table+='</tbody></table></Tbl>'
result=re.sub(r'<Fact label="Из исследования"><p>Заявляемая.*?</Fact>',table,result,flags=re.S)
result=result.replace('созданная не государством, а группой ведущих китайских учёных','созданный по инициативе учёных')
result=result.replace('undergraduate programs (8 majors)','undergraduate programs (перечень зависит от набора)')
result=result.replace('8 undergraduate majors','программы бакалавриата (актуальный перечень выше)')
result=result.replace('восемь undergraduate programs','семь программ для иностранных бакалавров по проверенному каталогу')
result=result.replace('Major выбирается в конце sophomore year','Major выбирается после третьего семестра по буклету Fall 2026')
result=result.replace('в конце второго года','после третьего семестра по буклету Fall 2026')
result=result.replace('рекомендации (typically 2)','рекомендации (число зависит от уровня программы)')
result=result.replace('Letters of recommendation (typically 2).','Три рекомендации: консультант и два учителя (Fall 2026).')
# Do not leave resolved questions or current-looking population counts as facts.
def audit_block(m):
 b=m.group(0)
 if any(x in b for x in ['2,441','251','17 национальност','17 nationalit','2,190']):
  b=b.replace('<Fact label="Из исследования">','<Unknown label="Данные без даты">').replace('</Fact>','</Unknown>')
  b=b.replace('</Unknown>','<p>Цифры сохранены из исходника; текущая численность и сопоставимость выборок не подтверждены.</p></Unknown>')
 if 'government oversight' in b or "political environment ограничивает" in b:
  b=b.replace('<Fact label="Из исследования">','<Unknown label="Требует источника">').replace('</Fact>','</Unknown>')
 return b
result=re.sub(r'<Fact label="Из исследования">.*?</Fact>',audit_block,result,flags=re.S)
path=ROOT/'src/content/universities/westlake.mdx'; path.write_text(result,encoding='utf-8')
print(f'Created {path.name}: {block_count} blocks, {len(result)} characters, 10 sections')
