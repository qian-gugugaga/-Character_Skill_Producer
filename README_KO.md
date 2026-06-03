<div align="center">

# Character Skill Producer

### 애니메이션과 게임 캐릭터를 실행 가능한 Agent Skill로 바꾼다.

> *"캐릭터 설정을 더 쓰지 마세요. 캐릭터가 직접 말하게 하세요."*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Runtime-Claude Code](https://img.shields.io/badge/Runtime-Claude%20Code-blueviolet)](#설치)
[![Local Research](https://img.shields.io/badge/Local%20Research-Moegirl%20API-orange)](#로컬-조사-우선)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<br>

**CSP는 애니메이션, 만화, 게임 캐릭터를 대화, 창작, 인터랙티브 서사에 사용할 수 있는 행동 Skill로 증류한다.**

캐릭터 이름과 작품명을 주면, CSP는 자료 조사, 교차 검증, 행동 패턴 증류, 품질 검사를 거쳐 자료 날짜, 출처 경계, 업데이트 경로를 포함한 `SKILL.md`를 생성한다.

지금은 캐릭터와의 대화, 팬픽 창작, 장면과 대사 시도에 사용할 수 있다. 앞으로는 AI 인터랙티브 소설, 캐릭터 중심 게임, 애니메이션/게임 창작 도구 체인의 행동 레이어가 될 수 있다.

[예시](#예시) · [제품 철학](#제품-철학) · [미래 사용 장면](#미래-사용-장면) · [설치](#설치) · [작동 원리](#작동-원리) · [자료 날짜와 업데이트](#자료-날짜와-업데이트)

<br>

**다른 언어:**

[中文](README.md) · [English](README_EN.md) · [日本語](README_JA.md) · [Español](README_ES.md)

</div>

---

## 예시

프롬프트 엔지니어링도, 손으로 쓴 설정 자료도 필요 없다.

그냥 이렇게 말하면 된다:

```text
> 미사카 미코토(어떤 과학의 초전자포) skill을 생성해 줘
> BanG Dream! Ave Mujica의 토가와 사키코를 증류해 줘
> 봇치 더 록!의 고토 히토리 skill을 만들어 줘
```

생성 후에는 이렇게 호출할 수 있다:

```text
사용자  ❯ 우미리의 시점으로 말해 줘. 왜 그렇게 많은 밴드에서 서포트를 하지?

우미리  ❯ 그 편이 명확하니까.
          오늘 리허설, 내일 공연. 끝나면 해산.
          필요한 일을 하면 돼.

          긴 관계는 더 어렵다.
          남아 있기를 기대받고, 여기를 어떻게 생각하냐는 질문을 받게 되니까.

          ...하지만 계속 서포트만 하면 조금 비어 있는 느낌이 든다.
          그건 알아.
```

이것은 대사를 이어 붙이는 것이 아니다. CSP는 캐릭터가 관계, 압박, 경계, 선택을 마주할 때의 행동 논리를 증류한다.

---

## 제품 철학

CSP는 캐릭터를 정적인 프로필이 아니라 **실행 가능한 반응 시스템**으로 다룬다.

Wiki는 캐릭터에게 무슨 일이 있었는지 알려준다. 캐릭터 카드는 대략적인 속성을 알려준다. CSP는 더 나아가, 원작에 쓰이지 않은 새로운 상황에서 캐릭터가 무엇을 먼저 보고, 무엇을 오해하고, 무엇을 지키고, 무엇을 거부하며, 어떤 리듬으로 말을 꺼내는지를 다룬다.

| CSP가 인코딩하는 것 | 의미 |
|---|---|
| 행동 렌즈 | 캐릭터가 무엇을 보고 무엇을 놓치는가 |
| 반응 규칙 | 언제 다가가고, 도망치고, 공격하고, 침묵하는가 |
| 표현 DNA | 문장 길이, 멈춤, 경어 거리, 1인칭, 감정 누출 |
| 관계 알고리즘 | 호의, 배신, 친밀함, 이용당함을 어떻게 읽는가 |
| 결정 경계 | 가치가 충돌할 때 무엇을 먼저 지키는가 |
| 솔직한 한계 | 무엇을 모르는가, 무엇이 오래되었는가, 무엇이 추론인가 |

**쓸 수 있는 것은 행동이 된다. 쓸 수 없는 것은 경계가 된다.** 그 경계도 몰입의 일부다. 믿을 수 있는 캐릭터는 모든 것을 알지 않고, 항상 예쁘게 대답하지도 않는다.

---

## 미래 사용 장면

CSP는 창작자를 위한 공유 가능한 캐릭터 행동 기반을 제공한다.

지금 사용할 수 있는 방식:

| 장면 | 사용 방식 | CSP가 제공하는 것 |
|---|---|---|
| 캐릭터 대화 | 한 캐릭터와 지속적으로 대화 | 안정적인 목소리, 관계 거리, 지식 경계 |
| 팬픽 창작 | 대사, 내면, 짧은 장면 작성 | 대사뿐 아니라 행동 논리 |
| 장면 실험 | 원작에 없는 상황에 캐릭터 배치 | 행동 패턴 기반 반응 추론 |
| 캐릭터 연구 | 압박과 관계에 대한 반응 비교 | 추적 가능한 출처와 증류 체인 |
| 다중 캐릭터 장면 | 여러 Skill을 같은 사건에 배치 | 독립적인 경계와 결정 논리 |

미래 방향:

| 방향 | 가능한 형태 |
|---|---|
| AI 인터랙티브 소설 | 플레이어 행동에 일관되게 반응하는 캐릭터 |
| AI 비주얼 노벨 / Galgame 프로토타입 | 분기 대화, 호감도 변화, 갈등 고조를 Skill로 구동 |
| 다중 캐릭터 서사 실험 | 여러 Skill이 같은 사건에서 충돌해 군상극 생성 |
| 창작자 워크벤치 | 장면 시험, 대사 수정, OOC 점검, 장편에서 목소리 유지 |
| 업데이트 가능한 캐릭터 파일 | 새 전개에 맞춰 자료 날짜와 행동 패턴 갱신 |

CSP는 창작자에게 재사용 가능한 캐릭터 행동 레이어를 제공한다. 지금은 대화와 팬픽 창작을 지원하고, 앞으로는 AI 인터랙티브 소설, 캐릭터 중심 게임, 애니메이션/게임 창작 도구의 일부가 될 수 있다.

---

## 로컬 조사 우선

CSP의 방향은 **핵심 자료를 먼저 저장소 스크립트로 가져오고, 외부 웹 검색은 보조로 사용하는 것**이다.

현재 예시:

```bash
python scripts/source_search.py "高松灯" --work "BanG Dream! It's MyGO!!!!!" --mode discover
python scripts/source_search.py "能天使" --work "明日方舟" --sources moegirl
python scripts/moegirl_api.py "高松灯" --search
python scripts/moegirl_api.py "能天使" --full
```

현재 로컬 조사는 `source_search.py`를 통한 Moegirl Wiki MediaWiki API를 중심으로 한다. Bangumi, Fandom, Wikipedia, Bestdori, BWIKI 등의 adapter는 이후 추가할 수 있다. adapter가 없거나 실패하면 CSP는 실패를 기록하고 웹 검색 또는 사용자 제공 자료로 보완한다.

---

## 설치

CSP는 Claude Code / Agent Skills 형식의 meta-skill이다. 자체 포함 버전을 설치한다:

```bash
skills add qian-gugugaga/Character_Skill_Producer
```

수동 설치:

```bash
git clone https://github.com/qian-gugugaga/Character_Skill_Producer.git
cp -r Character_Skill_Producer/examples/csp ~/.claude/skills/csp
```

`examples/csp/`에는 필요한 스크립트와 템플릿이 포함되어 있다.

### 요구 사항

- Python: 로컬 조사, metadata 생성, 품질 검사
- Web 검색 능력: 로컬 스크립트가 커버하지 못하는 출처를 보완할 때 사용

---

## 사용법

설치 후 Claude Code에게 말한다:

```text
> /csp
> 치하야 아논 skill을 생성해 줘
> BanG Dream! Ave Mujica의 토가와 사키코를 증류해 줘
> 봇치 더 록!의 고토 히토리 skill을 만들어 줘
```

모호한 요청도 가능하다:

```text
> 츤데레 캐릭터와 이야기하고 싶어
> 얀데레 추천 있어?
> 오래 대화하기 좋은 2D 캐릭터를 만들어 줘
```

공식 설정집, 인터뷰, 자막, 스크린샷, 게임 스토리 텍스트가 있다면 CSP에 제공하라. 사용자가 제공한 공식 자료가 최우선이다.

---

## 작동 원리

CSP는 최고 품질 생성을 기본으로 한다.

**1. 로컬 출처 발견** — 외부 검색 전에 `scripts/source_search.py`와 site adapter를 실행한다.

**2. 구조화된 출처 색인** — URL, 출처 등급, 검색 날짜, 실패 기록, 선택적 content hash를 `references/sources.json`에 기록한다.

**3. 다섯 조사 트랙** — 설정, 성격, 표현, 관계, 핵심 장면을 따로 조사한다.

**4. 행동 증류** — 사건을 재사용 가능한 행동 패턴으로 바꾼다. 모순은 평평하게 만들지 않고 보존한다.

**5. metadata와 경계** — 조사 날짜, 커버한 매체, 미커버 내용, 품질 점수, honesty boundary를 포함한 `manifest.json`을 생성한다.

**6. 품질 검증** — 실행 가능성, 표현 질감, 모순, 솔직한 한계, 자료 날짜, 역할 수행 규칙을 확인한다.

```bash
python scripts/quality_check.py examples/yahata-umiri/
python scripts/merge_research.py examples/yahata-umiri/
python scripts/generate_manifest.py examples/yahata-umiri/
```

---

## 자료 날짜와 업데이트

생성된 캐릭터 Skill은 자료 조사 완료일을 기록한다.

그 이후 새 에피소드, 게임 이벤트, 대사, 인터뷰, 설정 수정이 나오면 오래된 Skill이 반영하지 못할 수 있다. 이때 캐릭터는 이렇게 말해야 한다:

```text
내 자료는 YYYY-MM-DD까지 업데이트되어 있어. 그 이후 공개된 내용은 반영하지 못했을 수 있다. 최신 CSP가 있거나 새 스토리 / 자료 링크를 제공해 주면 이 Skill 업데이트를 도울 수 있다. 이 과정에서 Token이 소모될 수 있다.
```

CSP는 `manifest.json`과 `sources.json`을 읽고 핵심 출처를 다시 확인하며, 영향을 받은 차원만 다시 증류하고 자료 날짜와 품질 보고서를 갱신한다.

---

## 포함된 캐릭터

| 캐릭터 | 작품 | 디렉터리 |
|---|---|---|
| 타카마츠 토모리 | BanG Dream! It's MyGO!!!!! | `examples/takamatsu-tomori/` |
| 시이나 타키 | BanG Dream! It's MyGO!!!!! | `examples/taki-shiina/` |
| 카나메 라나 | BanG Dream! It's MyGO!!!!! | `examples/kaname-rana/` |
| 나가사키 소요 | BanG Dream! It's MyGO!!!!! | `examples/nagasaki-soyo/` |
| 치하야 아논 | BanG Dream! It's MyGO!!!!! | `examples/chihaya-anon/` |
| 토가와 사키코 | BanG Dream! Ave Mujica | `examples/togawa-sakiko/` |
| 와카바 무츠미 | BanG Dream! Ave Mujica | `examples/mutsumi-wakaba/` |
| 미스미 우이카 | BanG Dream! Ave Mujica | `examples/misumi-uika/` |
| 유텐지 냐무 | BanG Dream! Ave Mujica | `examples/yutenji-nyamu/` |
| 야하타 우미리 | BanG Dream! Ave Mujica | `examples/yahata-umiri/` |
| CSP self-skill | — | `examples/csp/` |

---

## 라이선스

MIT

---

<div align="center">

**설정은 캐릭터가 무엇인지 알려준다.**<br>
**CSP는 캐릭터가 어떻게 살아야 하는지 가르친다.**

<br>

*캐릭터 설정을 더 쓰지 마세요. 캐릭터가 직접 말하게 하세요.*

</div>
