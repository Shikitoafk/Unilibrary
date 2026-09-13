"""Reproducible editorial PDF from the same MDX used by UniLibrary."""
from pathlib import Path
import re, html, shutil
from xml.etree import ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, HRFlowable, KeepTogether, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.units import mm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'exports/Yonsei University — разбор.pdf'
raw = (ROOT/'src/content/universities/yonsei.mdx').read_text(encoding='utf-8')
meta, body = raw.split('---', 2)[1:]
BLUE = colors.HexColor('#153E76')
INK = colors.HexColor('#252A30')
MUTED = colors.HexColor('#6F757C')
RULE = colors.HexColor('#CDD2D6')
for name, filename in [('Serif','georgia.ttf'),('SerifBold','georgiab.ttf'),('SerifItalic','georgiai.ttf'),('Sans','arial.ttf'),('SansBold','arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/'+filename))
pdfmetrics.registerFontFamily('Serif', normal='Serif', bold='SerifBold', italic='SerifItalic', boldItalic='SerifBold')
pdfmetrics.registerFontFamily('Sans', normal='Sans', bold='SansBold', italic='Sans', boldItalic='SansBold')
WIDTH, HEIGHT = 210*mm, 297*mm
LEFT, RIGHT = 22*mm, 21*mm
CW = WIDTH-LEFT-RIGHT
styles = {}
def sty(name, **kw):
    base = dict(fontName='Serif',fontSize=10.5,leading=15.6,textColor=INK,spaceAfter=7,allowWidows=0,allowOrphans=0)
    base.update(kw)
    styles[name] = ParagraphStyle(name, **base)
    return styles[name]
sty('body')
sty('interp', fontName='Sans',fontSize=10.2,leading=15.3)
sty('unknown',fontName='Sans',fontSize=9.8,leading=14.7,textColor=MUTED)
sty('label',fontName='SansBold',fontSize=7.3,leading=10,textColor=BLUE,spaceBefore=9,spaceAfter=4,keepWithNext=True)
sty('h3',fontName='SerifBold',fontSize=15,leading=19,spaceBefore=17,spaceAfter=9,keepWithNext=True)
sty('chapter',fontSize=28,leading=33,spaceAfter=16,keepWithNext=True)
sty('deck',fontName='Sans',fontSize=10.8,leading=16,textColor=MUTED,spaceAfter=18)
sty('small',fontName='Sans',fontSize=8.2,leading=12,textColor=MUTED)
sty('sourceLabel',fontName='SansBold',fontSize=7.3,leading=10,textColor=BLUE,spaceBefore=5,spaceAfter=2,keepWithNext=True)
sty('quote',fontName='SerifItalic',fontSize=19,leading=27,textColor=BLUE,spaceAfter=20)
sty('title',fontSize=48,leading=54,textColor=BLUE,spaceAfter=20)
sty('toc',fontName='Serif',fontSize=12,leading=17,spaceBefore=8,spaceAfter=8)

descriptions = {
'identity':'Каким университетом Yonsei стал за свою историю - и почему UIC меняет опыт иностранного студента.',
'academics':'Что ты будешь изучать, сколько свободы получишь и где проходят границы англоязычной программы.',
'research':'От названия лаборатории до реального места в команде: доступ, наставничество и ограничения.',
'life':'Sinchon и Songdo, общежития, клубы и повседневная жизнь внутри корейского университета.',
'admissions':'Сначала маршрут и год набора. Затем документы, язык, эссе и интервью.',
'money':'Tuition, стипендии и расходы на жизнь. Финансовый план должен сходиться без обещаний будущего гранта.',
'outcomes':'Как связать бакалавриат с исследовательской работой, продолжением образования и карьерой.',
'criticism':'Языковой барьер, учебное давление, стоимость и интеграция: вопросы, которые стоит задать заранее.',
'you':'Личный выбор для biomedical / STEM абитуриента из Казахстана: подходящие сценарии и компромиссы.',
'verdict':'Окончательное решение зависит от конкретной программы, кампуса, финансирования и твоих планов.'}

sources=[]
for label,url in re.findall(r'\{label: "([^"]+)", url: "([^"]+)"\}',meta):
    if url not in [u for _,u in sources]: sources.append((label,url))
def source_number(url):
    for i,(_,u) in enumerate(sources,1):
        if u==url:return i
    sources.append(('Дополнительный источник',url)); return len(sources)
def inline(s):
    s=re.sub(r'<Src href="([^"]+)">.*?</Src>',lambda m: '<a color="#153E76" href="'+html.escape(m[1],quote=True)+'">['+str(source_number(m[1]))+']</a>',s,flags=re.S)
    s=re.sub(r'<(?!/?(?:b|i|a|br|super)\b)[^>]+>','',s)
    s=html.unescape(s)
    s=re.sub(r'&(?!#?\w+;)', '&amp;', s)
    return s.replace('—','-').replace('–','-').replace('\u2011','-')
def paragraph(s,style='body'):
    return Paragraph(inline(s),styles[style])

class Doc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=(WIDTH,HEIGHT),title='Yonsei University | UniLibrary',author='UniLibrary',leftMargin=LEFT,rightMargin=RIGHT,topMargin=22*mm,bottomMargin=20*mm)
        self.chapter=''
        self.addPageTemplates(PageTemplate(id='main',frames=[Frame(LEFT,20*mm,CW,255*mm,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=self.decorate))
    def beforeDocument(self):self.chapter=''
    def decorate(self,c,doc):
        c.saveState()
        if doc.page>1:
            c.setFont('Sans',7);c.setFillColor(MUTED)
            c.drawString(LEFT,HEIGHT-12*mm,'UNILIBRARY  /  YONSEI UNIVERSITY')
            c.setStrokeColor(RULE);c.setLineWidth(.4);c.line(LEFT,HEIGHT-15*mm,WIDTH-RIGHT,HEIGHT-15*mm)
        c.setStrokeColor(RULE);c.line(LEFT,14*mm,WIDTH-RIGHT,14*mm)
        c.setFillColor(MUTED);c.setFont('Sans',7)
        c.drawString(LEFT,9*mm,'DEEP RESEARCH  /  КАЗАХСТАН  /  2026')
        c.setFont('SansBold',8);c.setFillColor(BLUE);c.drawRightString(WIDTH-RIGHT,9*mm,f'{doc.page:02d}')
        c.restoreState()
    def afterFlowable(self,f):
        if hasattr(f,'bookmark'):
            self.canv.bookmarkPage(f.bookmark)
            self.canv.addOutlineEntry(f.getPlainText(),f.bookmark,level=0)
            self.notify('TOCEntry',(0,f.getPlainText(),self.page,f.bookmark))

story=[]
story.append(paragraph('UNILIBRARY  /  UNIVERSITY PORTRAITS','label'))
story.append(Spacer(1,18*mm))
story.append(paragraph('Yonsei<br/>University','title'))
story.append(paragraph('Южная Корея · Сеул / Инчхон<br/>Полный разбор для абитуриента из Казахстана','deck'))
story.append(HRFlowable(width='100%',thickness=1.3,color=BLUE,spaceAfter=18))
story.append(paragraph('Если убрать престиж и красивый сайт -<br/>захотел бы ты провести здесь<br/>четыре года своей жизни?','quote'))
story.append(paragraph('Англоязычный колледж, большая корейская университетская культура и медицинская исследовательская среда. Главный вопрос - какой именно Yonsei получишь ты.','body'))
story.append(Spacer(1,12*mm))
rows=[('ФОКУС','Биомедицина / STEM / undergraduate'),('МАРШРУТ','UIC с отдельными замечаниями о других колледжах'),('ВНУТРИ','10 разделов · условия · риски · личное соответствие'),('РЕДАКЦИЯ','13 сентября 2026')]
table=Table([[paragraph(a,'small'),paragraph(b,'body')] for a,b in rows],colWidths=[35*mm,CW-35*mm])
table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEABOVE',(0,0),(-1,0),.5,RULE),('LINEBELOW',(0,-1),(-1,-1),.5,RULE),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story.extend([table,PageBreak(),paragraph('Как читать этот выпуск','chapter')])
story.append(paragraph('Разбор устроен вокруг жизни и выбора: что ты изучаешь, где живёшь, как находишь исследования и сколько всё это стоит. Читай подряд или переходи к нужному разделу через оглавление.'))
toc=TableOfContents();toc.levelStyles=[styles['toc']];toc.dotsMinLevel=0
story.append(toc)
story.append(Spacer(1,8*mm))
for label,text in [('ПРОВЕРЕНО','Утверждение со ссылкой на официальный источник.'),('ИЗ ИССЛЕДОВАНИЯ','Материал авторского исходника. Пометка сама по себе не означает независимую проверку каждого утверждения.'),('ИНТЕРПРЕТАЦИЯ','Вывод и оценка автора; не статистика и не обещание университета.'),('ОТКРЫТЫЙ ВОПРОС','То, что пока не установлено и требует уточнения.')]:
    story.extend([paragraph(label,'label'),paragraph(text,'small')])

sections=re.findall(r'<Section num="([^"]+)" id="([^"]+)" title="([^"]+)">(.*?)</Section>',body,re.S)
for num,sid,title,content in sections:
    story.append(PageBreak())
    story.append(paragraph('ГЛАВА '+num,'label'))
    heading=paragraph(title,'chapter');heading.bookmark=sid;story.append(heading)
    story.append(paragraph(descriptions[sid],'deck'))
    story.append(HRFlowable(width='100%',thickness=.65,color=BLUE,spaceAfter=12))
    for m in re.finditer(r'<h3>(.*?)</h3>|<(Fact|Interp|Unknown)([^>]*)>(.*?)</\2>',content,re.S):
        if m[1]:
            story.append(paragraph(m[1],'h3'));continue
        kind,attrs,inside=m[2],m[3],m[4]
        label=re.search(r'label="([^"]+)"',attrs)
        label=label[1] if label else {'Fact':'Из исследования','Interp':'Интерпретация','Unknown':'Открытый вопрос'}[kind]
        style={'Fact':'body','Interp':'interp','Unknown':'unknown'}[kind]
        story.append(paragraph(label.upper(),'label'))
        for block in re.finditer(r'<(p|li)>(.*?)</\1>',inside,re.S):
            if block[1]=='li':
                bs=ParagraphStyle('bullet',parent=styles[style],leftIndent=12,firstLineIndent=0,bulletIndent=0,spaceAfter=5)
                story.append(Paragraph(inline(block[2]),bs,bulletText='•'))
            else:story.append(paragraph(block[2],style))

story.append(PageBreak())
h=paragraph('Источники и примечания','chapter');h.bookmark='sources';story.append(h)
story.append(paragraph('Основа выпуска - предоставленный автором PDF Yonsei University. Официальные страницы ниже позволяют проверить программу и актуальные правила. Номера в тексте кликабельны. Для поступления используй документы своего маршрута и года набора.','deck'))
for i,(label,url) in enumerate(sources,1):
    story.append(paragraph(f'{i:02d}  {label}','sourceLabel'))
    story.append(Paragraph('<a color="#153E76" href="'+html.escape(url,quote=True)+'">'+html.escape(url)+'</a>',styles['small']))
story.append(Spacer(1,3*mm))
story.append(paragraph('ГРАНИЦЫ ВЫВОДОВ','label'))
story.append(paragraph('Выпуск сохраняет авторский анализ и открытые вопросы. Отзывы о социальной среде не описывают всех студентов. Рейтинговые оценки соответствия являются мнением автора, а не вероятностью поступления. Данные graduate-программ, GKS и обычных колледжей нельзя автоматически переносить на UIC. Условия стипендии необходимо читать в индивидуальном offer.','small'))
OUT.parent.mkdir(exist_ok=True)
Doc(OUT).multiBuild(story)
public=ROOT/'public/downloads/yonsei-university.pdf';public.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(OUT,public)
from pypdf import PdfReader
r=PdfReader(OUT)
print(f'{len(r.pages)} pages; {OUT.stat().st_size} bytes; {sum(len(p.extract_text() or "") for p in r.pages)} characters')
