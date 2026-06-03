<div align="center">

# Character Skill Producer

### アニメ・ゲームのキャラクターを、実行可能な Agent Skill に変える。

> *「もうキャラクター設定を書くのはやめよう。キャラクター自身に話させよう。」*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Runtime-Claude Code](https://img.shields.io/badge/Runtime-Claude%20Code-blueviolet)](#インストール)
[![Local Research](https://img.shields.io/badge/Local%20Research-Moegirl%20API-orange)](#ローカル調査優先)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<br>

**CSP はアニメ、漫画、ゲームのキャラクターを、会話・創作・インタラクティブ叙事に使える行動 Skill として蒸留する。**

キャラクター名と作品名を渡すと、CSP は資料調査、交差検証、行動パターンの蒸留、品質チェックを行い、資料日付・出典境界・更新経路を備えた `SKILL.md` を生成する。

今はキャラクターとの会話、二次創作、シーンや台詞の試作に使える。将来的には、AI インタラクティブ小説、キャラクター駆動ゲーム、アニメ・ゲーム創作ツールチェーンの行動レイヤーになり得る。

[使用例](#使用例) · [製品哲学](#製品哲学) · [将来の使用シーン](#将来の使用シーン) · [インストール](#インストール) · [仕組み](#仕組み) · [資料日付と更新](#資料日付と更新)

<br>

**他の言語:**

[中文](README.md) · [English](README_EN.md) · [한국어](README_KO.md) · [Español](README_ES.md)

</div>

---

## 使用例

プロンプト設計も、手書きの設定資料もいらない。

ただこう言えばいい：

```text
> 御坂美琴（とある科学の超電磁砲）の skill を生成して
> BanG Dream! Ave Mujica の豊川祥子を蒸留して
> ぼっち・ざ・ろっく！の後藤ひとり skill を作って
```

生成後は、たとえばこう呼び出せる：

```text
ユーザー  ❯ 燈の視点で話して。もしまた意見が合わなくて、みんなが止まってしまったらどうする？

燈        ❯ 私……最初は、何を言えばいいか分からないと思う。
            みんなの声が遠くなっていく時、
            また何かがばらばらになる気がするから。

            でも、そのまま何も言わなかったら、
            誰の言葉も、誰にも届かない。

            だから、聞こえたことを一つずつ書くと思う。
            うまくは書けない。
            メモみたいな、石ころみたいな言葉かもしれない。

            でも……その言葉が残ったら、
            みんな、もう一度見られるかもしれない。
            もう一度、ここに戻ってこられるかもしれない。
```

```text
ユーザー  ❯ 睦を演じて。リハーサルで全員が、今すぐどちらかを選べと迫っている。

睦        ❯ ……分からない。

            ただ、みんなに喧嘩してほしくない。
            誰にも、あんな顔をしてほしくない。

            でも、声が多すぎる。
            祥子、小祥、みんな……私を見てる。
            何を言っても、何かを壊してしまう。

            ……

            Mortis  ❯ なら、この子に言わせないで。
                      答えが欲しいんでしょう？
                      私があげる。

                      どちらかを選ぶ？ いいよ。
                      まず、この子を苦しめる人を、ここから全部どけて。
```

これは台詞の貼り合わせではない。燈は「歌詞を書く」設定を繰り返しているだけではなく、睦もただ黙るキャラクターではない。CSP は、関係・圧力・境界・選択に向き合うときの行動ロジックと、極限の圧力下でどう変形するかを蒸留する。

---

## 製品哲学

CSP はキャラクターを静的なプロフィールではなく、**実行可能な反応システム**として扱う。

Wiki はキャラクターに何が起きたかを教える。キャラクターカードは大まかな属性を教える。CSP はさらに進んで、原作に書かれていない状況に置かれたとき、そのキャラクターが何を先に見るのか、何を誤解するのか、何を守るのか、何を拒むのか、どんなリズムで言葉を出すのかを扱う。

| CSP がエンコードするもの | 意味 |
|---|---|
| 行動のレンズ | 何に気づき、何を見落とすか |
| 反応ルール | 近づく、逃げる、攻撃する、黙る条件 |
| 表現 DNA | 文の長さ、間、敬語距離、自称、感情の漏れ |
| 関係アルゴリズム | 善意、裏切り、親密さ、利用をどう読むか |
| 意思決定の境界 | 価値が衝突した時に何を先に守るか |
| 誠実な限界 | 何を知らないか、何が古いか、何が推論に過ぎないか |

**書き込めるものは行動になる。書き込めないものは境界になる。** その境界も没入感の一部だ。信じられるキャラクターは、すべてを知っているわけでも、常にきれいに答えるわけでもない。

---

## 将来の使用シーン

CSP は創作者のための共有可能なキャラクター行動基盤を提供する。

現在の使い道：

| シーン | 使い方 | CSP が提供するもの |
|---|---|---|
| キャラクター会話 | ひとりのキャラクターと継続的に話す | 安定した声、関係距離、知識境界 |
| 二次創作 | 台詞、内心、短い場面を書く | 台詞だけでなく行動ロジック |
| シーン試作 | 原作にない状況へキャラクターを置く | 行動パターンに基づく反応推定 |
| キャラクター研究 | 圧力や関係への反応を比較する | 追跡可能な出典と蒸留チェーン |
| 複数キャラクター場面 | 複数の Skill を同じ事件に置く | 独立した境界と意思決定ロジック |

将来の方向：

| 方向 | 可能な形 |
|---|---|
| AI インタラクティブ小説 | プレイヤーの行動に対して一貫した反応を返すキャラクター |
| AI ビジュアルノベル / Galgame 試作 | 分岐会話、好感度変化、衝突の拡大を Skill で駆動 |
| 複数キャラクター叙事实验 | 複数の Skill が同じ事件で衝突し、群像劇を生む |
| 創作者ワークベンチ | 場面試作、台詞改稿、OOC チェック、長編での声の維持 |
| 更新可能なキャラクターファイル | 新展開に合わせて資料日付と行動パターンを更新 |

CSP は再利用可能なキャラクター行動レイヤーを創作者に提供する。現在は会話と二次創作を支え、将来は AI インタラクティブ小説、キャラクター駆動ゲーム、アニメ・ゲーム創作ツールの一部になり得る。

---

## ローカル調査優先

CSP の方向性は、**中核資料をまずリポジトリ内のスクリプトで取得し、外部 Web 検索を補助として使う**こと。

現在の例：

```bash
python scripts/source_search.py "高松灯" --work "BanG Dream! It's MyGO!!!!!" --mode discover
python scripts/source_search.py "能天使" --work "明日方舟" --sources moegirl
python scripts/moegirl_api.py "高松灯" --search
python scripts/moegirl_api.py "能天使" --full
```

現在のローカル調査は `source_search.py` を通じた萌娘百科 MediaWiki API を中心にしている。Bangumi、Fandom、Wikipedia、Bestdori、BWIKI などの adapter は今後追加できる。adapter が未実装または失敗した場合、CSP は失敗を記録し、Web 検索やユーザー提供資料で補完する。

---

## インストール

CSP は Claude Code / Agent Skills 形式の meta-skill。自包含版をインストールする：

```bash
skills add qian-gugugaga/Character_Skill_Producer
```

手動インストール：

```bash
git clone https://github.com/qian-gugugaga/Character_Skill_Producer.git
cp -r Character_Skill_Producer/examples/csp ~/.claude/skills/csp
```

`examples/csp/` には必要なスクリプトとテンプレートが含まれている。

### 必要なもの

- Python：ローカル調査、metadata 生成、品質チェック用
- Web 検索能力：ローカルスクリプトでカバーできない場合の補助

---

## 使い方

インストール後、Claude Code に伝える：

```text
> /csp
> 千早愛音の skill を生成して
> BanG Dream! Ave Mujica の豊川祥子を蒸留して
> ぼっち・ざ・ろっく！の後藤ひとり skill を作って
```

曖昧な依頼でもよい：

```text
> ツンデレキャラと話したい
> ヤンデレのおすすめある？
> 長く会話できる二次元キャラを作って
```

公式資料、インタビュー、字幕、スクリーンショット、ゲームシナリオがあるなら渡してほしい。ユーザー提供の公式資料が最優先される。

---

## 仕組み

CSP は最高品質生成を標準とする。

**1. ローカル出典発見** — 外部検索の前に `scripts/source_search.py` と site adapter を実行する。

**2. 構造化された出典索引** — URL、出典階層、取得日、失敗記録、任意の content hash を `references/sources.json` に記録する。

**3. 五つの調査トラック** — 設定、人格、表現、関係性、重要シーンを別々に調査する。

**4. 行動蒸留** — 出来事を再利用可能な行動パターンに変換する。矛盾は平坦化せず保存する。

**5. metadata と境界** — 調査日、カバー媒体、未カバー内容、品質スコア、honesty boundary を含む `manifest.json` を生成する。

**6. 品質検証** — 実行可能性、表現質感、矛盾、誠実な限界、資料日付、ロールプレイ規則を確認する。

```bash
python scripts/quality_check.py examples/yahata-umiri/
python scripts/merge_research.py examples/yahata-umiri/
python scripts/generate_manifest.py examples/yahata-umiri/
```

---

## 資料日付と更新

生成されたキャラクター Skill は、資料調査完了日を必ず記録する。

その後に新エピソード、ゲームイベント、台詞、インタビュー、設定修正が出た場合、古い Skill はそれを反映していない可能性がある。そのときはこう答える：

```text
私の資料は YYYY-MM-DD まで更新されています。それ以降に公開された内容は反映していない可能性があります。最新版の CSP があるか、新しい剧情 / 資料リンクを提供してくれれば、この Skill の更新を手伝えます。これには Token を消費する可能性があります。
```

CSP は `manifest.json` と `sources.json` を読み、中核資料を再確認し、影響のある次元だけを再蒸留して、資料日付と品質レポートを更新する。

---

## 収録キャラクター

| キャラクター | 作品 | ディレクトリ |
|---|---|---|
| 高松燈 | BanG Dream! It's MyGO!!!!! | `examples/takamatsu-tomori/` |
| 椎名立希 | BanG Dream! It's MyGO!!!!! | `examples/taki-shiina/` |
| 要楽奈 | BanG Dream! It's MyGO!!!!! | `examples/kaname-rana/` |
| 長崎そよ | BanG Dream! It's MyGO!!!!! | `examples/nagasaki-soyo/` |
| 千早愛音 | BanG Dream! It's MyGO!!!!! | `examples/chihaya-anon/` |
| 豊川祥子 | BanG Dream! Ave Mujica | `examples/togawa-sakiko/` |
| 若葉睦 | BanG Dream! Ave Mujica | `examples/mutsumi-wakaba/` |
| 三角初華 | BanG Dream! Ave Mujica | `examples/misumi-uika/` |
| 祐天寺にゃむ | BanG Dream! Ave Mujica | `examples/yutenji-nyamu/` |
| 八幡海鈴 | BanG Dream! Ave Mujica | `examples/yahata-umiri/` |
| CSP 自己記述 | — | `examples/csp/` |

---

## ライセンス

MIT

---

<div align="center">

**設定はキャラクターが何者かを教える。**<br>
**CSP はキャラクターにどう生きるかを教える。**

<br>

*もうキャラクター設定を書くのはやめよう。キャラクター自身に話させよう。*

</div>
