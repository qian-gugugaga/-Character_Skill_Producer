<div align="center">

# Character Skill Producer

> *「もうキャラクター設定を書くのはやめよう。キャラクター自身に話させよう。」*

**状態:** Agent Skills 標準 · Claude Code ランタイム · MIT License

<br>

**CSP はアニメ・ゲームのキャラクターを、実行可能な Agent Skill に変える。**

キャラクター名と作品名を渡すだけで、調査、交差検証、行動パターンの蒸留を行い、直接インストールして会話できる `SKILL.md` を生成する。

キャラカードではない。設定集でもない。「ツンデレ」「クール」みたいなラベルの束でもない。

CSP が抽出するのは、キャラクターが**どう反応し、どう話し、他人をどう読み、何を絶対にしないか**という、AI が実行できる行動プログラムだ。

[使用例](#使用例) · [インストール](#インストール) · [CSPが蒸留するもの](#cspが蒸留するもの) · [仕組み](#仕組み) · [収録キャラクター](#収録キャラクター)

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
> BanG Dream! It's MyGO!!!!! の椎名真希を蒸留して
> 五条悟のキャラクター skill を作って
```

CSP はキャラクター資料を、実行可能な行動に変える。生成後は、たとえばこう呼び出せる：

```text
ユーザー  ❯ 海鈴の視点で話して。なぜたくさんのバンドをサポートするの？

海鈴      ❯ その方が、はっきりしているから。
            今日リハ、明日ライブ。終わったら解散。
            必要なことをするだけ。

            長い関係は、少し面倒。
            残ることを期待されるし、ここを何だと思っているのか聞かれる。

            ……でも、ずっとサポートだけだと、少し空っぽになる。
            それは分かってる。
```

これは台詞の貼り合わせではない。CSP はキャラクターの下にある行動ロジックを蒸留する。

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

- Python：萌娘百科 MediaWiki API ヘルパー用
- Web 検索能力：Wikipedia、Fandom Wiki、Bangumi、Bilibili などの補強用

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

## CSPが蒸留するもの

普通のキャラカードはこう書く：

> 性格：冷静、頼れる、距離がある。

CSP は実行可能な形で書く：

> 長期的な約束を求められると、まず関係をタスクに翻訳する。リハ頻度、退出条件、連絡担当。興味がないのではなく、制御できない感情的期待から自分を守るために、事務的な境界を置く。

| 層 | 問い |
|---|---|
| **行動動態** | どんな状況で何をするか。圧力下でどう変わるか。 |
| **表現の質感** | 文の長さ、間、口癖、自称、敬語距離。 |
| **社会認知** | 善意、脅威、親しさ、裏切りをどう読むか。 |
| **意思決定ロジック** | 価値が衝突した時、何を先に守るか。 |
| **誠実な限界** | キャラクターが知らないこと、原作が支えていないこと。 |

**CSP はより良い Wiki を作るのではない。キャラクターを生きているようにする。**

---

## 仕組み

**1. 複数ソース調査** — 萌娘百科、Wikipedia、Fandom Wiki、Bangumi、AniDB、Bilibili、ゲームシナリオ、ユーザー提供資料。

**2. 五つの並列分析** — 設定、人格、表現、関係性、重要シーンを別々に調査する。

**3. 行動蒸留** — 出来事を、再利用可能な行動パターンに変換する。矛盾は平坦化せず保存する。

**4. 品質検証** — 実行可能性、表現の質感、矛盾、誠実な限界、ロールプレイ規則を確認する。

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
