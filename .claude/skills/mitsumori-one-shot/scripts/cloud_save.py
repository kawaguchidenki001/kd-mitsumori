# -*- coding: utf-8 -*-
"""KD見積のクラウド（GAS）へ見積を直接保存する。

使い方:
  python3 cloud_save.py <見積JSON> --auth <社内パスワード> [--no 260701] [--dry-run]

- <見積JSON> は mitsumori-one-shot スキルの取込スキーマ（header/place/rows...）。
  ここで KD見積アプリの内部 state 形式に変換してから保存する。
- 自社情報はクラウドの共有マスタ（id=__masters__）から取得して埋める。
- 見積Noを省略すると、クラウド一覧から当月の次番号（YYMMNN形式）を自動採番する。
- 保存後、KD見積の「開く」一覧に表示される。
- 通信は GAS の JSONP API（GET）。ネットワークポリシーで
  script.google.com / script.googleusercontent.com の許可が必要。
"""
import json, base64, re, sys, time, random, string, urllib.parse, urllib.request, datetime

GAS_URL = "https://script.google.com/macros/s/AKfycby4mDfDGx3DUsnpGrMdUg8pzGKteFeKun5Ea16_b0_a2DmM0ICGuueit48RHIWJZc0c/exec"

def jsonp(params, auth):
    q = dict(params)
    q["auth"] = auth
    q["callback"] = "cb"
    url = GAS_URL + "?" + urllib.parse.urlencode(q)
    with urllib.request.urlopen(url, timeout=30) as r:
        body = r.read().decode("utf-8", "replace")
    m = re.search(r"cb\((.*)\)\s*;?\s*$", body, re.S)
    if not m:
        raise RuntimeError("JSONP応答を解析できません: " + body[:200])
    res = json.loads(m.group(1))
    if isinstance(res, dict) and res.get("ok") is False:
        raise RuntimeError("GASエラー: " + str(res.get("error")))
    return res

def load_masters(auth):
    try:
        res = jsonp({"action": "load", "id": "__masters__"}, auth)
        return json.loads(res.get("data") or "{}")
    except Exception:
        return {}

def next_no(auth):
    t = datetime.date.today()
    shrt = t.strftime("%y%m"); full = t.strftime("%Y%m")
    n = 0
    for it in (jsonp({"action": "list"}, auth).get("list") or []):
        no = str(it.get("no") or it.get("id") or "")
        seq = None
        m = re.match(r"^(\d{6})(\d{2,})(?:-\d+)?$", no)
        if m and m.group(1) == full: seq = int(m.group(2))
        else:
            m = re.match(r"^(\d{6})-(\d{3,})(?:-\d+)?$", no)
            if m and m.group(1) == full: seq = int(m.group(2))
            else:
                m = re.match(r"^(\d{4})(\d{2,})(?:-\d+)?$", no)
                if m and m.group(1) == shrt: seq = int(m.group(2))
        if seq and seq > n: n = seq
    return shrt + ("%02d" % (n + 1))

def to_state(d, masters):
    """取込スキーマ → アプリ内部 state 形式"""
    s = (masters.get("settings") or {})
    company = s.get("company") or {}
    profiles = s.get("companies") or []
    if profiles:
        company = {k: profiles[0].get(k, "") for k in
                   ("name", "rep", "trade", "zip", "addr", "tel", "fax", "invoice", "bank")}
    h = d.get("header") or {}
    doc = dict(s.get("doc") or {})
    for k_src, k_doc in (("place", "place"), ("remarks", "remarks"),
                         ("validity", "validity"), ("payment", "payment")):
        if d.get(k_src) is not None: doc[k_doc] = str(d[k_src])
    rows = []; seq = [0]
    def uid():
        seq[0] += 1; return "r%d" % seq[0]
    for r in d.get("rows") or []:
        if r.get("type") == "cat":
            rows.append({"id": uid(), "type": "cat", "name": str(r.get("name") or "")}); continue
        name = str(r.get("name") or "").strip()
        if not name: continue
        row = {"id": uid(), "type": "item", "name": name,
               "spec": str(r.get("spec") or ""),
               "qty": float(r["qty"]) if r.get("qty") not in (None, "") else 1,
               "unit": str(r.get("unit") or "式"),
               "price": round(float(r.get("price") or 0)),
               "cost": round(float(r.get("cost") or 0)),
               "note": str(r.get("note") or "")}
        if r.get("pl") is not None: row["pl"] = round(float(r["pl"]))
        for k in ("rate", "welfare", "expense"):
            if r.get(k) and float(r[k]) > 0: row[k] = str(float(r[k])); row["spec"] = row["spec"] or "率計上"
        rows.append(row)
    return {"header": {"name": h.get("name") or "", "client": h.get("client") or "",
                       "client2": h.get("client2") or "", "honorific": h.get("honorific") or "御中",
                       "date": h.get("date") or datetime.date.today().isoformat(),
                       "term": h.get("term") or "", "no": h.get("no") or "", "staff": h.get("staff") or "",
                       "status": ""},
            "company": company, "companyId": (profiles[0].get("id") if profiles else None),
            "doc": doc, "discount": float(d.get("discount") or 0),
            "taxRate": float(d.get("taxRate") if d.get("taxRate") is not None else (s.get("taxRate", 10))),
            "targetMargin": float(s.get("targetMargin", 20)),
            "dateMode": s.get("dateMode") or "wareki",
            "priceMode": d.get("priceMode") or s.get("priceMode") or "comp",
            "taxMode": d.get("taxMode") or s.get("taxMode") or "in",
            "outputSummary": False, "rows": rows}

def doc_total(st):
    mat = sum((r.get("qty") or 0) * (r.get("price") or 0)
              for r in st["rows"] if r.get("type") == "item" and not any(r.get(k) for k in ("rate", "welfare", "expense")))
    rate = sum(round(mat * float(r[k]) / 100)
               for r in st["rows"] for k in ("rate", "welfare", "expense") if r.get(k))
    net = mat + rate - (st.get("discount") or 0)
    if st.get("taxMode") == "out":
        return round(net * (1 + st["taxRate"] / 100))
    return round(net)

def save(state, auth, no):
    payload = json.dumps(state, ensure_ascii=False, separators=(",", ":"))
    b64 = base64.b64encode(payload.encode()).decode()
    chunks = [b64[i:i + 1200] for i in range(0, len(b64), 1200)] or [""]
    token = "tk" + format(int(time.time() * 1000), "x") + "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    jsonp({"action": "save_begin", "token": token}, auth)
    for i, ch in enumerate(chunks):
        jsonp({"action": "save_chunk", "token": token, "data": ch}, auth)
        print(f"  送信 {i+1}/{len(chunks)}", end="\r")
    h = state["header"]
    jsonp({"action": "save_end", "token": token, "id": no,
           "name": h["name"], "client": h["client"], "no": no,
           "date": h["date"], "total": doc_total(state), "status": ""}, auth)
    print(f"\n保存完了: 見積No {no}『{h['name']}』")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    src = args[0]
    auth = args[args.index("--auth") + 1] if "--auth" in args else ""
    no = args[args.index("--no") + 1] if "--no" in args else ""
    dry = "--dry-run" in args
    d = json.load(open(src, encoding="utf-8"))
    masters = load_masters(auth) if not dry else {}
    state = to_state(d, masters)
    if dry:
        print(json.dumps(state, ensure_ascii=False, indent=1)[:2000])
        print("... dry-run（送信なし） rows=%d" % len(state["rows"])); sys.exit(0)
    if not auth:
        print("--auth <社内パスワード> が必要です"); sys.exit(1)
    if not no:
        no = next_no(auth)
    state["header"]["no"] = no
    save(state, auth, no)
