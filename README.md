# KD見積

河口電機株式会社の見積作成アプリ（単一HTML）。

**公開先：https://kd-mitsumori.pages.dev**（Cloudflare Pages・合言葉で保護）

- 見積書・請求書の作成、Excel／PDF出力
- 岐阜県単価DB・商品（型番）からの単価検索
- クラウド保存（Google Apps Script＋スプレッドシート）で全PC共有

## ファイル構成

| ファイル | 役割 |
|---|---|
| `index.html` | アプリ本体（これ1つで動きます） |
| `template_estimate.xlsx` | 見積書の様式（鑑＋内訳6ページ） |
| `template_invoice.xlsx` | 請求書の様式 |
| `products.json` | 商品（型番）データ |
| `pdfassets/` | PDF生成用のライブラリとフォント（BIZ UD明朝／ゴシック） |
| `functions/_middleware.js` | 合言葉ゲート（**Cloudflare Pages でのみ動作**） |

## 合言葉で保護する（Cloudflare Pages）

GitHub Pages には「パスワードを確認してからページを返す」仕組みがないため、
画面だけを隠しても素通りできてしまいます。Cloudflare Pages で配信すると、
`functions/_middleware.js` が**合言葉なしでは画面も様式ファイルも単価データも返しません**。

設置済み（2026-09-28）。以下は再構築するときの手順。

### 設置手順（1回だけ）

1. [Cloudflare](https://dash.cloudflare.com/) にログイン →「Workers & Pages」→「作成」→ **Pages** →「Git に接続」
2. リポジトリ `kawaguchidenki001/kd-mitsumori`、ブランチ `main` を選ぶ
3. ビルド設定
   - フレームワーク プリセット：**なし**
   - ビルドコマンド：**空欄**
   - ビルド出力ディレクトリ：**`/`**（リポジトリの直下）
4. デプロイ後 →「設定」→「変数とシークレット」→ **`SITE_PASSWORD`** を追加（値が合言葉）
5. もう一度デプロイ → 新しいURLを開いて合言葉画面が出れば完了
6. GitHub の Settings → Pages → Source を **None** にして、古いURL（保護なし）を止める

以後、`main` に push すると自動で反映されます。

### 動き

- 合言葉を入れると、その端末では約90日そのまま開けます（HttpOnly / Secure Cookie）
- `SITE_PASSWORD` 未設定のあいだは素通り（設定忘れで締め出されないように）
- 合言葉を変えると、それまでのCookieは無効になります
- 検索エンジンには載せません（`X-Robots-Tag: noindex`）

### 移行時の注意

見積データ・自社情報・客先・担当・印鑑はクラウドにあるため引き継がれますが、
**URLが変わると端末内の記憶（社内パスワード・下書き・画面の設定）は空になります**。
新しいURLで最初に一度だけ社内パスワードを入力してください。共有データは自動で戻ります。
