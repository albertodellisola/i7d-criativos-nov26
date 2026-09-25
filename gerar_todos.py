# Página única com todos os criativos da campanha, categorizados (25/09/2026).
# Fontes: index antigo (30 + Risco ZERO) e consenso do lote de 100.
import json, re, html, os
D = os.path.dirname(os.path.abspath(__file__))
CONS = os.path.expanduser('~/i7d-copywriting/pecas/2026-09-15_meta-100-imagens/')
antigo = open(os.environ['ANTIGO']).read()
NO_AR = {'D01-01','D03-01','D05-08','D06-03','N07','N24'}
e = html.escape

# legendas antigas: id -> texto
leg = {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<b>(\w+)</b><span>(.*?)</span>', antigo)}

def card(id_, titulo, a, b=None, nota=''):
    badge = '<i class="ar">já rodou no anúncio</i>' if id_ in NO_AR else ''
    dual = f' data-b="{b}"' if b else ''
    fmt = '<small class="fmt">4:5 · feed</small>' if b else '<small class="fmt">quadrado</small>'
    return (f'<figure{dual} data-a="{a}"><a href="{a}" target="_blank"><img loading="lazy" src="{a}" alt="{e(id_)}"></a>'
            f'<figcaption><b>{e(id_)}</b>{badge}{fmt}<span>{e(titulo)}</span>{nota}</figcaption></figure>')

secoes = []  # (id, titulo, desc, [subsecoes (id, nome, desc, cards)])
# 1. Risco ZERO
rz = [card(f'G0{i}', leg.get(f'G0{i}',''), f'img/rz/G0{i}_4x5.jpg', f'img/rz/G0{i}_9x16.jpg') for i in range(1,9)]
secoes.append(('risco','Série Risco ZERO','8 peças com a garantia como assunto principal: “se não gostar até o 2º dia, devolvemos todo o seu dinheiro”. Fotos reais das turmas. Cada uma em 4:5 (feed) e 9:16 (Stories/Reels).',[('risco-g','', '', rz)]))
# 2. Lote de 100 por dor
grupos = json.load(open(CONS+'consenso_grupos.json'))
pecas = json.load(open(CONS+'consenso_pecas.json'))
subs = []
for g in grupos:
    cs = [card(p['id'], p['titulo'].replace('*',''), f'cem/img/{p["id"]}_4x5.jpg', f'cem/img/{p["id"]}_9x16.jpg')
          for p in pecas if p['grupo'] == g['grupo']]
    txt = ''.join(f'<li><b>Título {i+1}:</b> {e(t)}</li>' for i,t in enumerate(g['titulos']))
    txt += ''.join(f'<li><b>Texto {i+1}:</b> {e(t).replace(chr(10),"<br>")}</li>' for i,t in enumerate(g['textos']))
    subs.append((g['grupo'], f'{g["grupo"]} · {g["nome"]}', f'<details><summary>Texto do anúncio deste grupo</summary><ul>{txt}</ul></details>', cs))
secoes.append(('dor','Lote por dor · 100 peças','10 grupos, um para cada dor ou objeção de quem já estudou inglês e trava. Cada peça em 4:5 (feed) e 9:16 (Stories/Reels).', subs))
# 3. As 30 com CTA de WhatsApp
blocos = [('geral','Público geral','Legenda: “Você entende inglês. Na hora de falar, trava.”',
           'A1 A2 A3 A5 A6 N01 N02 N03 N04 N05 N06 N07 N08 N10 N19 N20 N21 N22 N23 N24 N25'),
          ('corp','Corporativo','Legenda: “Você entende a reunião. Mas, quando chega sua vez de falar, trava?”','C16 C17 C18 C09'),
          ('depo','Depoimentos · público cético','Legenda: “Já estudou inglês por anos e ainda não fala como gostaria?”','R11 R12 R13 R14 R15')]
subs = []
for sid, nome, desc, ids in blocos:
    cs = []
    for i in ids.split():
        orig = f'img/{i}_orig.jpg'
        nota = f'<details><summary>ver como era antes</summary><img loading="lazy" src="{orig}" alt=""></details>' if os.path.exists(os.path.join(D,orig)) else ''
        cs.append(card(i, leg.get(i,''), f'img/{i}.jpg', None, nota))
    subs.append((sid, f'{nome} · {len(cs)}', f'<p>{e(desc)}</p>', cs))
secoes.append(('whats','Peças da equipe com chamada para o WhatsApp','30 peças já existentes, com o botão ou a frase de chamada trocados para o WhatsApp. O desenho não mudou. Formato quadrado.', subs))

total = sum(len(c) for *_, ss in secoes for *__, c in ss)
CURTO = {'risco':'Risco ZERO','dor':'Por dor (100)','whats':'Chamada WhatsApp (30)'}
nav = ''.join(f'<a href="#{s[0]}">{CURTO[s[0]]}</a>' for s in secoes)
corpo = ''
for sid, tit, desc, ss in secoes:
    n = sum(len(c) for *_, c in ss)
    sub_nav = ''
    if len(ss) > 1:
        sub_nav = '<div class="chips">' + ''.join(f'<a href="#{x[0]}">{e(x[1])}</a>' for x in ss) + '</div>'
    corpo += f'<section id="{sid}"><header class="sec"><h2>{e(tit)} <em>{n}</em></h2><p>{e(desc)}</p>{sub_nav}</header>'
    for xid, xnome, xdesc, cs in ss:
        if xnome:
            corpo += f'<div class="sub" id="{xid}"><h3>{e(xnome)}</h3>{xdesc}</div>'
        corpo += f'<div class="grid">{"".join(cs)}</div>'
    corpo += '</section>'

page = open(os.path.join(D,'todos_modelo.html')).read()
page = page.replace('{{TOTAL}}', str(total)).replace('{{NAV}}', nav).replace('{{CORPO}}', corpo)
open(os.path.join(D,'index.html'),'w').write(page)
print('peças:', total)
