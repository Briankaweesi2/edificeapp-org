#!/usr/bin/env python3
"""Build localized sibling routes from the reviewed locale catalogs."""
import json, re, sys, zipfile
from pathlib import Path
from bs4 import BeautifulSoup, Comment
ROOT=Path(__file__).resolve().parents[2]
LANGS={'zh':'简体中文','hi':'हिन्दी','es':'Español','ar':'العربية'}
DIRECTION={'zh':'ltr','hi':'ltr','es':'ltr','ar':'rtl'}
EDITION={'zh':'新标点和合本','hi':'Indian Revised Version (Hindi), 2019','es':'Reina-Valera 1909','ar':'Van Dyck'}
BOOKS={'Genesis':'GEN','Exodus':'EXO','Leviticus':'LEV','Numbers':'NUM','Deuteronomy':'DEU','Joshua':'JOS','Judges':'JDG','Ruth':'RUT','1 Samuel':'1SA','2 Samuel':'2SA','1 Kings':'1KI','2 Kings':'2KI','1 Chronicles':'1CH','2 Chronicles':'2CH','Ezra':'EZR','Nehemiah':'NEH','Esther':'EST','Job':'JOB','Psalms':'PSA','Psalm':'PSA','Proverbs':'PRO','Ecclesiastes':'ECC','Song of Solomon':'SNG','Isaiah':'ISA','Jeremiah':'JER','Lamentations':'LAM','Ezekiel':'EZK','Daniel':'DAN','Hosea':'HOS','Joel':'JOL','Amos':'AMO','Obadiah':'OBA','Jonah':'JON','Micah':'MIC','Nahum':'NAM','Habakkuk':'HAB','Zephaniah':'ZEP','Haggai':'HAG','Zechariah':'ZEC','Malachi':'MAL','Matthew':'MAT','Mark':'MRK','Luke':'LUK','John':'JHN','Acts':'ACT','Romans':'ROM','1 Corinthians':'1CO','2 Corinthians':'2CO','Galatians':'GAL','Ephesians':'EPH','Philippians':'PHP','Colossians':'COL','1 Thessalonians':'1TH','2 Thessalonians':'2TH','1 Timothy':'1TI','2 Timothy':'2TI','Titus':'TIT','Philemon':'PHM','Hebrews':'HEB','James':'JAS','1 Peter':'1PE','2 Peter':'2PE','1 John':'1JN','2 John':'2JN','3 John':'3JN','Jude':'JUD','Revelation':'REV'}
def scripture_map(lang):
 cache=ROOT/'locales/scripture'/f'{lang}.json'
 if cache.is_file():return json.loads(cache.read_text(encoding='utf8'))
 out={};root=ROOT/'locales/bibles'
 if lang in ('es','hi'):
  refs=(root/'vref.txt').read_text().splitlines();lines=(root/f'{lang}.txt').read_text().splitlines()
  out={r:t for r,t in zip(refs,lines) if t.strip()}
 else:
  filename={'ar':'arb-vd','zh':'cmn-cu89s'}[lang];z=zipfile.ZipFile(root/f'{lang}.zip')
  for name in z.namelist():
   if not name.endswith('.usfm'):continue
   book=name.split('-')[1][:3].upper();chapter=0;verse=0;active=[]
   for raw in z.read(name).decode('utf-8-sig').splitlines():
    cm=re.match(r'\\c\s+(\d+)',raw)
    vm=re.match(r'\\v\s+(\d+)(?:-(\d+))?\s*(.*)',raw)
    if cm:chapter=int(cm.group(1));continue
    if vm:
     if active:
      out[f'{book} {chapter}:{verse}']=clean_usfm(' '.join(active))
     verse=int(vm.group(1));active=[vm.group(3)];continue
    if active and raw.startswith(('\\q','\\m','\\p','\\li')):active.append(raw)
   if active:out[f'{book} {chapter}:{verse}']=clean_usfm(' '.join(active))
 return out
def clean_usfm(text):
 text=re.sub(r'\\f .*?\\f\*','',text)
 text=re.sub(r'\\[a-z]+\d*\*?', '',text)
 return re.sub(r'\s+',' ',text).strip()

def norm(s):return re.sub(r'\s+',' ',s).strip()
def source_pages():return sorted(p for p in ROOT.rglob('*.html') if p.relative_to(ROOT).parts[0] not in set(LANGS)|{'tools','.git'} and p.name=='index.html')
def route(p):return '/'+str(p.relative_to(ROOT).parent).strip('.')+'/' if p.parent!=ROOT else '/'
def localized(path,lang):return '/'+lang+path if path.startswith('/') else '/'+lang+'/'+path

def picker(soup,page,current,cat):
 nav=soup.new_tag('nav',attrs={'class':'language-picker','aria-label':cat.get('Choose language','Choose language')})
 for l,label in [('en','English'),*LANGS.items()]:
  a=soup.new_tag('a',href=route(page) if l=='en' else localized(route(page),l));a['lang']='zh-Hans' if l=='zh' else l;a['hreflang']='zh-Hans' if l=='zh' else l;a.string=label
  if l==current: a['aria-current']='page'
  nav.append(a)
 skip=soup.select_one('.skip,.skip-link')
 if skip:skip.insert_after(nav)
 else:soup.body.insert(0,nav)
 return nav

def add_alternates(soup,p):
 head=soup.head
 for l in ['en',*LANGS]:
  href=('https://edificeapp.org'+route(p)) if l=='en' else 'https://edificeapp.org'+localized(route(p),l)
  tag=soup.new_tag('link',rel='alternate',hreflang='x-default' if l=='en' else ('zh-Hans' if l=='zh' else l),href=href);head.append(tag)


def render(p,lang,cat,bible,routes):
 soup=BeautifulSoup(p.read_text(), 'html.parser'); d=soup.html
 for existing in soup.select('.language-picker,link[rel=alternate],link[href="/assets/i18n.css"]'):existing.decompose()
 d['lang']='zh-Hans' if lang=='zh' else lang;d['dir']=DIRECTION[lang]
 # Translate quoted verses from the named licensed edition by their adjacent reference.
 protected=set(); translated_citations=[]
 for el in soup.select('.scripture,blockquote,.mini-reader > p,.scene-art > p'):
  protected.update(map(id,el.descendants))
  citation=''
  for ancestor in [el.parent,*list(el.parent.parents)[:4]] if el.parent else [el]:
   candidates=ancestor.select('.citation,.card-bottom') if hasattr(ancestor,'select') else []
   candidates=[c for c in candidates if 'KJV' in c.get_text(' ',strip=True)]
   if candidates:citation=candidates[-1].get_text(' ',strip=True);break
  if not citation and el.parent:
   for sibling in [el.find_next_sibling(),el.parent.find_next_sibling()]:
    if sibling and 'KJV' in sibling.get_text(' ',strip=True):citation=sibling.get_text(' ',strip=True);break
  if not citation and 'scene-art' in (el.parent.get('class') or []):citation=el.parent.get_text(' ',strip=True)
  match=re.search(r'((?:[1-3] )?[A-Za-z][A-Za-z ]*?)\s+(\d+):(\d+)(?:-(\d+))?',citation)
  if not match and 'scene-art' in (el.parent.get('class') or []):match=re.search(r'(Psalm)\s+(\d+)',citation)
  if match:
   book=match.group(1).strip();code=BOOKS.get(book);chapter=int(match.group(2));first=int(match.group(3)) if match.lastindex>=3 else 1;last=int(match.group(4) or first) if match.lastindex>=4 else first
   if book=='Psalm':first=1
   verses=[bible.get(f'{code} {chapter}:{n}') for n in range(first,last+1)] if code else []
   translated=' '.join(v for v in verses if v)
   if translated:
    el.clear();el.append(translated)
    for anc in [el.parent,*list(el.parent.parents)[:4]]:
     choices=[c for c in anc.select('.citation,.card-bottom') if 'KJV' in c.get_text(' ',strip=True)]
     if choices:translated_citations.append(choices[-1]);break
    if not choices and 'scene-art' in (el.parent.get('class') or []):
     choices=[c for c in el.parent.find_all('span') if 'KJV' in c.get_text(' ',strip=True)]
     if choices:translated_citations.append(choices[-1])

 for n in soup.find_all(string=True):
  if isinstance(n,Comment) or id(n) in protected or n.parent.name in ['script','style'] or n.find_parent('svg'):continue
  old=norm(str(n))
  if old in cat and cat[old]:n.replace_with(cat[old].replace('KJV',EDITION[lang]))
 license_text={
  'zh':'经文摘录采用《新标点和合本》（简体中文），公共领域。',
  'hi':'पवित्रशास्त्र के अंश Indian Revised Version Holy Bible (Hindi), 2019 से हैं। © Bridge Connectivity Solutions Pvt. Ltd. (2017–2019), CC BY-SA 4.0. संदर्भानुसार चुने गए अंश उसी लाइसेंस के अंतर्गत रूपांतरित हैं। स्रोत: eBible.org.',
  'es':'Los pasajes bíblicos usan la Reina-Valera 1909, de dominio público. ',
  'ar':'مقتطفات الكتاب المقدس من ترجمة فان دايك، وهي ضمن الملكية العامة. '
 }
 footer=soup.body.find('footer')
 if footer:
  note=soup.new_tag('p',attrs={'class':'bible-attribution','lang':lang})
  note.string=license_text[lang]
  source=soup.new_tag('a',href={'zh':'https://ebible.org/cmn-cu89s/copyright.htm','hi':'https://ebible.org/hin2017/copyright.htm','es':'https://ebible.org/spaRV1909/copyright.htm','ar':'https://ebible.org/arb-vd/copyright.htm'}[lang],rel='noopener')
  source.string='eBible.org';note.append(' ');note.append(source);footer.append(note)
 for el in soup.find_all(True):
  for a in ['alt','title','aria-label','placeholder','data-store-label']:
   old=norm(el.get(a,''))
   if old in cat and cat[old]:el[a]=cat[old].replace('KJV',EDITION[lang])
 for el in soup.select('meta[name="description"],meta[property="og:title"],meta[property="og:description"],meta[name="twitter:title"],meta[name="twitter:description"]'):
  old=norm(el.get('content',''))
  if old in cat and cat[old]:el['content']=cat[old]
 for citation in translated_citations:
  for text in citation.find_all(string=True):
   if 'KJV' in text:text.replace_with(str(text).replace('KJV',EDITION[lang]))
 path=route(p); page_path=localized(path,lang)
 for a in soup.select('a[href^="/"]'):
  href=a['href'];base=href.split('#',1)[0].split('?',1)[0]
  if base in routes:a['href']=localized(base,lang)+(('?'+href.split('?',1)[1]) if '?' in href else '')+(('#'+href.split('#',1)[1]) if '#' in href else '')
 for el in soup.select('link[rel="canonical"],meta[property="og:url"]'):

  if el.name=='link':el['href']='https://edificeapp.org'+page_path
  else:el['content']='https://edificeapp.org'+page_path
 for el in soup.select('script[type="application/ld+json"]'):
  try: obj=json.loads(el.string or '{}')
  except ValueError:continue
  def tr(x):
   if isinstance(x,dict):
    for k,v in x.items():
     if k in {'name','description','headline','text'} and isinstance(v,str):x[k]=cat.get(norm(v),v)
     else:tr(v)
   elif isinstance(x,list):
    for v in x:tr(v)
  tr(obj);el.string=json.dumps(obj,ensure_ascii=False)
 head=soup.head
 add_alternates(soup,p)
 css=soup.new_tag('link',rel='stylesheet',href='/assets/i18n.css');head.append(css)
 picker(soup,p,lang,cat)
 scripts=[s for s in soup.find_all('script') if s.get('src') and s.get('src').endswith(('website-v3.js','deep-links-v3.js'))]
 if scripts:
  loader=soup.new_tag('script',src=f'/assets/i18n-{lang}.js',defer=True)
  scripts[0].insert_before(loader)
 return '<!doctype html>\n'+str(soup.html)

def main():
 changed=0; missing=[]
 for p in source_pages():
  d=BeautifulSoup(p.read_text(), 'html.parser')
  for existing in d.select('.language-picker,link[rel=alternate],link[href="/assets/i18n.css"]'):existing.decompose()
  add_alternates(d,p);picker(d,p,'en',{'Choose language':'Choose language'})
  d.head.append(d.new_tag('link',rel='stylesheet',href='/assets/i18n.css'));p.write_text('<!doctype html>\n'+str(d.html),encoding='utf8')
 for lang in LANGS:
  cat=json.loads((ROOT/'locales'/f'{lang}.json').read_text())
  bible=scripture_map(lang)
  files=source_pages()
  routes={route(f) for f in files}
  empty=[k for k,v in cat.items() if not v]
  if empty:raise SystemExit(f'{lang}: {len(empty)} untranslated strings; refusing to generate')
  (ROOT/lang).mkdir(exist_ok=True)
  for p in files:
   target=ROOT/lang/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(render(p,lang,cat,bible,routes),encoding='utf8');changed+=1
 for lang in LANGS:
  cat=json.loads((ROOT/'locales'/f'{lang}.json').read_text())
  jskeys=['Website analytics preference','Your cookie preferences','We use optional analytics cookies to understand how our website is used and improve your experience. You can accept or reject them, and change your choice anytime.','Learn more','Reject optional','Accept cookies','Cookie preferences','Open in Edifice','I am requesting deletion of my Edifice account.','Account email:','Reason (optional):','I understand this permanently deletes your account, journal entries, streaks and saved data ','after the 7-day safety period.','Account Deletion Request - Edifice']
  mapping={k:cat.get(k,k) for k in jskeys}
  asset=ROOT/'assets'/f'i18n-{lang}.js'
  asset.write_text('window.edificeText='+json.dumps(mapping,ensure_ascii=False)+';\n',encoding='utf8')
 sitemap=ROOT/'sitemap.xml'
 original=sitemap.read_text(encoding='utf8')
 entries=[]
 for p in source_pages():
  for lang in LANGS:entries.append(f'  <url><loc>https://edificeapp.org{localized(route(p),lang)}</loc></url>')
 if '</urlset>' in original:
  fresh=[entry for entry in entries if entry not in original]
  if fresh:sitemap.write_text(original.replace('</urlset>','\n'+'\n'.join(fresh)+'\n</urlset>'),encoding='utf8')
 print(f'Generated {changed} locale pages, runtime labels, and {len(entries)} sitemap entries')
if __name__=='__main__':main()
