import html
import sys
from collections import Counter
sys.path.insert(0, "uncommons-cube/cache")
from analyze_list_nov5 import THEMES, unique_cards, card_map

# Add Gathering of Darkness and Marwyn, the Preserver into BGU/GUR/RWB
THEMES["BGU"]["enablers"].extend(["Gathering of Darkness", "Marwyn, the Preserver"])
THEMES["GUR"]["enablers"].append("Marwyn, the Preserver")
THEMES["RWB"]["enablers"].append("Gathering of Darkness")

def render_card_li(name, is_both=False):
    c = card_map[name]
    escaped = html.escape(c["name"], quote=True)
    mv = int(c["cmc"])
    ci = "".join(c["color_identity"]) or "C"
    badge = f'<span class="mv-badge">{mv}</span>'
    both_tag = ' <span class="both-tag" title="Both Payoff and Enabler in this theme">★</span>' if is_both else ''
    ci_tag = f' <span class="ci-tag">[{ci}]</span>' if len(c["color_identity"]) != 1 else ''
    return f'<li class="card-link" data-card-name="{escaped}">{badge} {html.escape(c["name"])}{ci_tag}{both_tag}</li>'

sections_html = []

for t_key, t_data in THEMES.items():
    cols = t_data["colors"]
    p_set = set(t_data["payoffs"])
    e_list_no_lands = [n for n in t_data["enablers"] if "Land" not in card_map[n]["type_line"]]
    e_set = set(e_list_no_lands)
    both_set = p_set & e_set
    
    p_cards = [card_map[n] for n in t_data["payoffs"]]
    e_cards = [card_map[n] for n in e_list_no_lands]
    u_names = list(dict.fromkeys(t_data["payoffs"] + e_list_no_lands))
    u_cards = [card_map[n] for n in u_names]

    def curve_str(clist):
        cnt = Counter(min(6, max(1, int(c["cmc"]))) for c in clist)
        return " · ".join(f"MV{mv}{'+' if mv==6 else ''}: <b>{cnt.get(mv,0)}</b>" for mv in range(1, 7))

    p_ci = Counter("".join(sorted(c["color_identity"])) or "C" for c in p_cards)
    e_ci = Counter("".join(sorted(c["color_identity"])) or "C" for c in e_cards)
    p_ci_str = ", ".join(f"{k}: {v}" for k, v in sorted(p_ci.items(), key=lambda x: (len(x[0]), x[0])))
    e_ci_str = ", ".join(f"{k}: {v}" for k, v in sorted(e_ci.items(), key=lambda x: (len(x[0]), x[0])))

    cols_html = []
    for col_key in cols + ["2C"]:
        if col_key in ("W", "U", "B", "R", "G"):
            col_p = [n for n in t_data["payoffs"] if card_map[n]["color_identity"] == [col_key]]
            col_e = [n for n in e_list_no_lands if card_map[n]["color_identity"] == [col_key] and n not in p_set]
            col_label = f"{col_key} ({len(col_p)}P / {len(col_e) + len([n for n in col_p if n in both_set])}E)"
        else:
            col_p = [n for n in t_data["payoffs"] if len(card_map[n]["color_identity"]) != 1]
            col_e = [n for n in e_list_no_lands if len(card_map[n]["color_identity"]) != 1 and n not in p_set]
            col_label = f"2C & C ({len(col_p)}P / {len(col_e) + len([n for n in col_p if n in both_set])}E)"

        col_p.sort(key=lambda n: (int(card_map[n]["cmc"]), n))
        col_e.sort(key=lambda n: (int(card_map[n]["cmc"]), n))

        p_lis = "\n            ".join(render_card_li(n, n in both_set) for n in col_p) or '<li class="empty-note">None</li>'
        e_lis = "\n            ".join(render_card_li(n, False) for n in col_e) or '<li class="empty-note">None</li>'

        cols_html.append(f"""        <div class="color-column">
          <div class="color-header color-{col_key}">{col_label}</div>
          <div class="role-header">Payoffs ({len(col_p)})</div>
          <ul class="card-list">
            {p_lis}
          </ul>
          <div class="role-header enabler-header">Enablers (+{len(col_e)} unique)</div>
          <ul class="card-list">
            {e_lis}
          </ul>
        </div>""")

    grid = "\n".join(cols_html)
    sections_html.append(f"""    <section class="theme-section">
      <div class="theme-title">
        <span>{html.escape(t_data["title"])}</span>
        <span class="theme-badges">{len(p_cards)} Payoffs · {len(e_cards)} Enablers ({len(u_cards)} unique nonland cards)</span>
      </div>
      <div class="theme-stats">
        <div><strong>Payoff Colors:</strong> {p_ci_str} &nbsp;|&nbsp; <strong>Enabler Colors:</strong> {e_ci_str}</div>
        <div><strong>Payoff Curve:</strong> {curve_str(p_cards)}</div>
        <div><strong>Theme Curve (All {len(u_cards)}):</strong> {curve_str(u_cards)}</div>
      </div>
      <div class="columns">
{grid}
      </div>
    </section>""")

full_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>list-nov5.txt — 10-Theme Payoff & Enabler Breakdown</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --surface: #ffffff;
      --border: #d8dce3;
      --text: #1c2026;
      --muted: #5c6470;
      --accent: #2d5be3;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 32px 24px 64px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
    }}
    .container {{
      max-width: 1180px;
      margin: 0 auto;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 1.75rem;
      font-weight: 700;
    }}
    .subtitle {{
      margin: 0 0 24px;
      color: var(--muted);
      font-size: 0.95rem;
    }}
    .theme-section {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      margin-bottom: 22px;
      overflow: hidden;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }}
    .theme-title {{
      padding: 12px 18px;
      font-size: 1.05rem;
      font-weight: 600;
      background: #eef1f6;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .theme-badges {{
      font-size: 0.85rem;
      font-weight: 600;
      color: #2d5be3;
      background: #e3ecfc;
      padding: 3px 10px;
      border-radius: 999px;
    }}
    .theme-stats {{
      padding: 8px 18px;
      background: #fafbfc;
      border-bottom: 1px solid var(--border);
      font-size: 0.82rem;
      color: var(--muted);
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .columns {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
    }}
    .color-column {{
      padding: 14px 16px 18px;
      border-right: 1px solid var(--border);
    }}
    .color-column:last-child {{ border-right: none; }}
    .color-header {{
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 4px 10px;
      border-radius: 5px;
      display: inline-block;
      margin-bottom: 8px;
    }}
    .color-W {{ background: #fdf6d8; color: #6b5600; border: 1px solid #e6d89c; }}
    .color-U {{ background: #dcebfa; color: #0f4c81; border: 1px solid #aacbef; }}
    .color-B {{ background: #e3dfe8; color: #2d2536; border: 1px solid #bdb5c7; }}
    .color-R {{ background: #fadcd6; color: #8a2511; border: 1px solid #f0b1a4; }}
    .color-G {{ background: #d9f0df; color: #195c2d; border: 1px solid #a7d9b4; }}
    .color-2C {{ background: #f3e8c8; color: #5c4308; border: 1px solid #dbc48a; }}
    .role-header {{
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: #1c2026;
      margin: 6px 0 4px;
      padding-bottom: 2px;
      border-bottom: 1px dashed #e1e4ea;
    }}
    .enabler-header {{
      margin-top: 12px;
      color: #5c6470;
    }}
    .card-list {{
      list-style: none;
      margin: 0;
      padding: 0;
    }}
    .card-link {{
      padding: 4px 8px;
      margin: 1px -8px;
      border-radius: 5px;
      cursor: pointer;
      font-size: 0.88rem;
      color: var(--accent);
      transition: background 0.12s ease;
      user-select: none;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .card-link:hover {{
      background: #eef3fd;
      text-decoration: underline;
    }}
    .mv-badge {{
      display: inline-block;
      min-width: 18px;
      height: 18px;
      line-height: 18px;
      text-align: center;
      font-size: 0.72rem;
      font-weight: 700;
      color: #4a525d;
      background: #eaedf2;
      border-radius: 4px;
      flex-shrink: 0;
    }}
    .ci-tag {{
      font-size: 0.72rem;
      color: #6b7280;
      font-weight: 600;
    }}
    .both-tag {{
      font-size: 0.75rem;
      color: #d97706;
      margin-left: auto;
    }}
    .empty-note {{
      font-size: 0.82rem;
      color: #9ca3af;
      font-style: italic;
      padding: 2px 0;
    }}
    #card-preview {{
      position: fixed;
      z-index: 1000;
      pointer-events: none;
      display: none;
      width: 260px;
      border-radius: 13px;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.32);
      background: #111;
      overflow: hidden;
    }}
    #card-preview img {{ display: block; width: 100%; height: auto; }}
    #card-preview .status {{
      padding: 16px;
      color: #fff;
      font-size: 0.85rem;
      text-align: center;
    }}
    @media (max-width: 768px) {{
      .columns {{ grid-template-columns: repeat(2, 1fr); }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>list-nov5.txt — 10-Theme Payoff & Enabler Breakdown</h1>
    <p class="subtitle">Full breakdown of the 333-card Nov 5 list across all 10 triad themes in default order (WUB, WBG, BRG, BGU, GWU, GUR, UBR, URW, RGW, RWB). Hover any card to preview from Scryfall.</p>

{chr(10).join(sections_html)}
  </div>

  <div id="card-preview" role="tooltip" aria-hidden="true">
    <div class="status">Loading…</div>
    <img alt="" />
  </div>

  <script>
    (() => {{
      const preview = document.getElementById('card-preview');
      const img = preview.querySelector('img');
      const status = preview.querySelector('.status');
      const imageCache = new Map();
      let activeCard = null;

      function scryfallImageUrl(cardName) {{
        const params = new URLSearchParams({{
          exact: cardName,
          format: 'image',
          version: 'normal',
        }});
        return `https://api.scryfall.com/cards/named?${{params.toString()}}`;
      }}

      function positionPreview(event) {{
        const pad = 18;
        const rect = preview.getBoundingClientRect();
        const vw = window.innerWidth;
        const vh = window.innerHeight;
        let x = event.clientX + pad;
        let y = event.clientY + pad;
        if (x + rect.width + pad > vw) x = event.clientX - rect.width - pad;
        if (y + rect.height + pad > vh) y = Math.max(pad, vh - rect.height - pad);
        preview.style.left = `${{x}}px`;
        preview.style.top = `${{y}}px`;
      }}

      function showCard(cardName, event) {{
        activeCard = cardName;
        preview.style.display = 'block';
        preview.setAttribute('aria-hidden', 'false');
        const url = scryfallImageUrl(cardName);
        if (imageCache.get(cardName) === 'loaded') {{
          status.style.display = 'none';
          img.style.display = 'block';
          img.src = url;
          positionPreview(event);
          return;
        }}
        img.style.display = 'none';
        status.style.display = 'block';
        status.textContent = 'Loading…';
        positionPreview(event);
        const loader = new Image();
        loader.onload = () => {{
          imageCache.set(cardName, 'loaded');
          if (activeCard !== cardName) return;
          img.src = url;
          status.style.display = 'none';
          img.style.display = 'block';
        }};
        loader.onerror = () => {{
          imageCache.set(cardName, 'error');
          if (activeCard !== cardName) return;
          status.textContent = `Could not load "${{cardName}}"`;
        }};
        loader.src = url;
      }}

      function hideCard() {{
        activeCard = null;
        preview.style.display = 'none';
        preview.setAttribute('aria-hidden', 'true');
      }}

      document.querySelectorAll('.card-link').forEach((el) => {{
        const name = (el.dataset.cardName || el.textContent).trim();
        el.addEventListener('mouseenter', (e) => showCard(name, e));
        el.addEventListener('mousemove', positionPreview);
        el.addEventListener('mouseleave', hideCard);
      }});
    }})();
  </script>
</body>
</html>
"""

with open("uncommons-cube/list-nov5-breakdown.html", "w") as f:
    f.write(full_html)
print("Wrote uncommons-cube/list-nov5-breakdown.html")

