/**
 * KD見積の入り口。合言葉を入れないと、中の何も見せない。
 *
 * Cloudflare Pages が、画面・様式ファイル・単価データを返す前に必ずここを通る。
 * 合言葉は Cloudflare の設定（環境変数 SITE_PASSWORD）に入れる。
 * このファイルにも、公開されるページにも、合言葉そのものは書かない。
 *
 * ■ Cloudflare 側の設定（1回だけ）
 *   Workers & Pages → 対象のプロジェクト → 設定 → 変数とシークレット
 *   名前 SITE_PASSWORD ／ 値は社内に配る合言葉。
 *   ※ 未設定のあいだは素通りさせる。設定を忘れたまま締め出されるほうが
 *     困るため。設定すれば、次に開いたときから合言葉を聞く。
 *
 * ※ このファイルは Cloudflare Pages でのみ働く。GitHub Pages では
 *   ただのファイルとして無視される（＝守られない）。
 */

const COOKIE_NAME = 'kdm_pass';
const MAX_AGE = 60 * 60 * 24 * 90;      // 90日。3か月に1回入れ直す程度
const LOGIN_PATH = '/__login';

/** 合言葉から、端末に持たせる印を作る。合言葉そのものは持たせない。 */
async function markOf(pass) {
  const buf = await crypto.subtle.digest(
    'SHA-256', new TextEncoder().encode('kd-mitsumori|' + pass));
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, '0')).join('');
}

/**
 * スマホの日本語入力だと、半角のつもりが全角になることがある。
 * 見た目はほぼ同じでも別の文字なので、そのままでは弾かれる。
 * 全角を半角に直し、前後の空白も落としてから見くらべる。
 */
function normPass(s) {
  var t = String(s == null ? '' : s);
  try { t = t.normalize('NFKC'); } catch (e) {}
  return t.replace(/^[\s　]+|[\s　]+$/g, '');
}

/** 長さの違いや、何文字目で違ったかを外から測られないように比べる */
function sameText(a, b) {
  const x = new TextEncoder().encode(String(a));
  const y = new TextEncoder().encode(String(b));
  let diff = x.length ^ y.length;
  const n = Math.max(x.length, y.length);
  for (let i = 0; i < n; i++) diff |= (x[i] || 0) ^ (y[i] || 0);
  return diff === 0;
}

function esc(s) {
  return String(s).replace(/[&<>"]/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

function loginPage(backTo, message) {
  const html = `<!doctype html><html lang="ja"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>KD見積</title>
<style>
  :root{color-scheme:dark;}
  *{box-sizing:border-box;}
  body{margin:0;min-height:100dvh;display:flex;align-items:center;justify-content:center;
    background:#0d1420;color:#e8eef7;padding:24px;
    font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif;}
  .box{width:100%;max-width:380px;}
  h1{font-size:17px;font-weight:800;margin:0 0 4px;letter-spacing:.02em;}
  .sub{font-size:12.5px;color:#8fa3bd;margin:0 0 22px;line-height:1.7;}
  label{display:block;font-size:12px;color:#8fa3bd;margin:0 0 7px;}
  .hint{display:block;font-size:11px;color:#6f8299;margin-top:2px;}
  .show{display:flex;align-items:center;gap:7px;margin:11px 0 0;font-size:12.5px;
    color:#8fa3bd;cursor:pointer;}
  .show input{width:auto;margin:0;}
  input{width:100%;font-family:inherit;font-size:16px;padding:14px 15px;border-radius:11px;
    border:1.5px solid #2a3a52;background:#141d2b;color:#e8eef7;}
  input:focus{outline:none;border-color:#ffc43c;}
  button{width:100%;margin-top:14px;font-family:inherit;font-size:15px;font-weight:800;
    padding:14px;border-radius:11px;border:none;background:#b8860b;color:#fff;cursor:pointer;}
  button:active{background:#9c7009;}
  .err{margin:14px 0 0;font-size:12.5px;color:#ff9a9a;}
  .note{margin:26px 0 0;font-size:11.5px;color:#6f8299;line-height:1.8;}
</style></head><body>
<div class="box">
  <h1>KD見積</h1>
  <p class="sub">河口電機株式会社　見積作成システム<br>
    社内用のページです。合言葉を入れてください。</p>
  <form method="POST" action="${LOGIN_PATH}">
    <input type="hidden" name="next" value="${esc(backTo)}">
    <label for="p">合言葉<span class="hint">半角の英数字。日本語入力はオフに</span></label>
    <input id="p" name="pass" type="password" autocomplete="current-password"
           inputmode="latin" autocapitalize="off" autocorrect="off"
           spellcheck="false" autofocus>
    <label class="show"><input type="checkbox" id="s"> 打った文字を表示する</label>
    <button type="submit">開く</button>
  </form>
  <script>
    (function () {
      var p = document.getElementById('p'), s = document.getElementById('s');
      s.addEventListener('change', function () { p.type = s.checked ? 'text' : 'password'; });
    })();
  </script>
  ${message ? `<p class="err">${esc(message)}</p>` : ''}
  <p class="note">一度入れると、この端末では約3か月そのまま開けます。<br>
    入れても同じ画面に戻ってくるときは、ブラウザのプライベートモードを
    解いてからもう一度お試しください。</p>
</div></body></html>`;
  return new Response(html, {
    status: 401,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Robots-Tag': 'noindex, nofollow',
    },
  });
}

export async function onRequest(context) {
  const { request, env, next } = context;
  const pass = String((env && env.SITE_PASSWORD) || '');
  if (!pass) return next();               // 設定前に締め出さない

  const url = new URL(request.url);
  const mark = await markOf(pass);

  // 合言葉を受け取る
  if (request.method === 'POST' && url.pathname === LOGIN_PATH) {
    let got = '', backTo = '/';
    try {
      const form = await request.formData();
      got = String(form.get('pass') || '');
      const n = String(form.get('next') || '/');
      backTo = n.charAt(0) === '/' && n.charAt(1) !== '/' ? n : '/';   // 外部へ飛ばさない
    } catch (e) {}
    if (sameText(got, pass) || sameText(normPass(got), normPass(pass))) {
      // 合言葉が通った印を付けて戻す。これが付いたまま戻ってきたのに
      // 記録が無ければ、その端末が覚えられていないと分かる。
      var to = backTo + (backTo.indexOf('?') >= 0 ? '&' : '?') + '_ok=1';
      return new Response(null, {
        status: 303,
        headers: {
          Location: to,
          'Set-Cookie': COOKIE_NAME + '=' + mark + '; Path=/; Max-Age=' + MAX_AGE
            + '; HttpOnly; Secure; SameSite=Lax',
          'Cache-Control': 'no-store',
        },
      });
    }
    // 総当たりを遅くする
    await new Promise((r) => setTimeout(r, 800));
    return loginPage(backTo, '合言葉が違います。');
  }

  const cookie = request.headers.get('Cookie') || '';
  const m = cookie.match(/(?:^|;\s*)kdm_pass=([0-9a-f]{64})/);
  if (m && sameText(m[1], mark)) {
    // 印は役目を終えたので、アドレスから外してきれいにする
    if (url.searchParams.get('_ok') === '1') {
      url.searchParams.delete('_ok');
      return Response.redirect(url.toString(), 302);
    }
    return next();
  }

  // 合言葉は通ったのに戻ってきた＝この端末が記録を保存できていない
  var stuck = url.searchParams.get('_ok') === '1'
    ? '合言葉は合っています。ただ、この端末がログインを覚えられません。'
      + 'プライベートモード（シークレット）を解くか、'
      + 'SafariやChromeで開き直してください。'
    : '';
  return loginPage(url.pathname, stuck);
}
