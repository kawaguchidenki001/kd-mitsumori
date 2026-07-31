---
name: mitsumori-one-shot
description: 図面・内訳書・器具表などから見積項目と数量を拾い出し、tanka-search（複合単価データ）や products.json（器具定価）で単価を付け、KD見積（kd-mitsumori）へワンタップで取り込めるリンク／JSONを作って印刷まで完結させる日本語ワークフロー。「図面から見積を作って」「内訳から拾い出してKD見積に入れて」「見積書にして印刷して」「拾い出しから印刷まで」などのリクエストで必ず使うこと。図面PDF・内訳Excel・器具表の写真などがアップロードされ見積作成が目的のときもこのスキルを使う。
---

# 見積ワンショット（拾い出し→単価→KD見積→印刷）

図面や内訳から見積を作り、KD見積アプリに1タップで反映して印刷するまでを、1つの指示で完結させる。
token-saver ルール（テキスト抽出優先・150DPI先行など）を常に併用する。正確性＞節約。

## 全体の流れ

1. **拾い出し** — アップロードされた図面/内訳/器具表から明細（分類・品名・仕様・数量・単位）を抽出
2. **単価付け** — tanka-search の複合単価、products.json の器具定価で単価を決定
3. **JSON生成** — 下記スキーマの見積JSONを作成
4. **反映リンク** — base64url化して KD見積の取込リンクを作成（`print:true` で印刷まで自動）
5. **納品** — リンク（長い場合は .json ファイル）＋合計金額の要点のみ報告

## 1. 拾い出し

- PDF はまず pdfplumber/PyMuPDF でテキスト抽出。図面はテキストで拾えない記号のみラスタライズ（150DPI先行→必要箇所のみ300DPI）。
- Excel の内訳書は openpyxl 等で直接読む。
- 拾う内容：分類（電灯設備/動力設備/弱電設備/経費 など）、品名、仕様（型番・サイズ）、数量、単位。
- 配線・配管の m 数、器具・スイッチ・コンセントの個数は図面のカウント根拠を必ず記録（note か作業メモに）。
- 数量が図面から確定できないものは「1式」にして note に「数量要確認」と書く。勝手に推定確定しない。

## 2. 単価付け

**複合単価（工事単価）** — tanka-search リポジトリの `unit_prices.json`（約9,000件）：
- セッションにリポジトリがあれば直接読む。なければ `https://raw.githubusercontent.com/kawaguchidenki001/tanka-search/main/unit_prices.json` を取得（約2.9MB。全文をコンテキストに読み込まず、Pythonで検索する）。
- 1件の形式：`{category, name, spec, work, unit, material_unit_price, material_cost, labor_cost, expense, composite_price, removal_factor, removal_cost}`
- 通常は `composite_price`（複合単価）を KD見積の `price` に入れる。材工分離（`priceMode:"ml"`）のときは `price`=材料、`pl`=労務。
- 撤去は `removal_cost` を使う。
- name+spec の完全一致→部分一致→category内の近い仕様の順で探す。仕様違いを流用したら note に「単価: ○○で代用」と書く。

**器具定価** — kd-mitsumori リポジトリの `products.json`（照明・ドアホン等の定価データ）：
- 定価×掛率で単価を決める。掛率はKの指示に従う（指示がなければ定価のまま入れて note に「定価・掛率未適用」）。

**どちらにも無い単価**：`price:0` のまま note に「別途見積」または「単価要確認」。勝手にWeb相場で確定しない（Kが後で入れられる）。

## 3. 見積JSONスキーマ

```json
{
  "header": {"name":"工事名","client":"客先名","honorific":"御中","date":"YYYY-MM-DD","staff":"担当"},
  "place": "工事場所",
  "remarks": "備考",
  "taxMode": "out",
  "rows": [
    {"type":"cat","name":"電灯コンセント設備"},
    {"name":"電線管","spec":"GP-16 溶融亜鉛めっき","qty":25,"unit":"m","price":3160,"note":"複合単価"},
    {"name":"埋込コンセント","spec":"2口 E付","qty":8,"unit":"個","price":3500},
    {"type":"cat","name":"経費"},
    {"name":"諸経費","rate":10}
  ],
  "print": true
}
```

- 行は上から順に表示される。`{"type":"cat"}` は分類見出し行。
- 集計行：`rate`=純工事費×%（諸経費など）、`welfare`=労務費×%（法定福利費）、`expense`=経費率。数値だけ入れれば金額はアプリが自動計算する。小計・合計・消費税の行は**入れない**（アプリが計算する）。
- 任意項目：`header.client2/term/no`、`taxRate`（既定10）、`discount`（値引き額）、`priceMode`（"comp"=複合単価（既定）/"ml"=材工分離）、行の `cost`（原価）・`pl`（労務単価）。
- `print:true` を付けるとリンクを開いたとき自動で印刷ダイアログが開く。指示に「印刷」が含まれるときだけ付ける。

## 4. 反映リンクの作成

```python
import base64, json
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
b64 = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + b64
print(len(url))
```

- **URLが約8,000文字以内**（目安：明細60行程度まで）→ リンクをそのまま渡す。タップするだけでKD見積に取り込まれる。
- それを超える場合 → `見積_{工事名}.json` ファイルで渡し、「KD見積の📥取込ボタンから読み込んでください」と一言添える。
- どちらの場合も、渡す前に JSON を再パースして合計金額を自前計算し、明細の合計・税額を検算する（正確性チェック）。

## 5. 納品・報告

報告は1〜3文のみ：リンク（またはファイル）＋「明細◯件・税抜合計◯円」＋単価未確定の件数。
明細の全リストをチャットに再掲しない。単価要確認の項目だけ箇条書きで示す。

## 注意

- KD見積アプリ側の取込仕様は `index.html` の「JSON取込」コメント（`importFromJson` 付近）が正。スキーマに迷ったらそちらを確認。
- 既存の見積を編集中にリンクを開いても、確認ダイアログが出るので上書き事故はない（新規起動時は確認なしで取り込まれる）。
- 取込後の保存（クラウド保存・見積No採番）はKがアプリ内で行う。Claudeはクラウド保存APIを直接叩かない。
