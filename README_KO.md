<div align="center">

# Character Skill Producer

> *"캐릭터 설정을 더 쓰지 마세요. 캐릭터가 직접 말하게 하세요."*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Runtime-Claude Code](https://img.shields.io/badge/Runtime-Claude%20Code-blueviolet)](#설치)
[![License: CC--BY--4.0](https://img.shields.io/badge/License-CC--BY--4.0-yellow.svg)](#라이선스)

<br>

**CSP는 애니메이션과 게임 캐릭터를 실행 가능한 Agent Skill로 바꾼다.**

캐릭터 이름과 작품명을 주면, 자료를 조사하고, 교차 검증하고, 행동 패턴을 증류해 바로 설치하고 대화할 수 있는 `SKILL.md`를 생성한다.

캐릭터 카드가 아니다. 설정집도 아니다. "츤데레", "차갑고 믿음직함" 같은 라벨 모음도 아니다.

CSP가 추출하는 것은 캐릭터가 **어떻게 반응하고, 어떻게 말하고, 타인을 어떻게 읽고, 무엇을 절대 하지 않는가**라는 AI가 실행할 수 있는 행동 프로그램이다.

[예시](#예시) · [설치](#설치) · [CSP가 증류하는 것](#csp가-증류하는-것) · [작동 원리](#작동-원리) · [포함된 캐릭터](#포함된-캐릭터)

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
> BanG Dream! It's MyGO!!!!!의 시이나 마키를 증류해 줘
> 고죠 사토루 캐릭터 skill을 만들어 줘
```

CSP는 캐릭터 정보를 실행 가능한 행동으로 바꾼다. 생성 후에는 이렇게 호출할 수 있다:

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

이것은 대사를 이어 붙이는 것이 아니다. CSP는 캐릭터 아래에 있는 행동 논리를 증류한다.

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

- Python: Moegirl Wiki MediaWiki API 헬퍼용
- Web 검색 능력: Wikipedia, Fandom Wiki, Bangumi, Bilibili 등 보강용

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

## CSP가 증류하는 것

일반 캐릭터 카드는 이렇게 쓴다:

> 성격: 침착함, 믿음직함, 거리를 둠.

CSP는 실행 가능한 형태로 쓴다:

> 장기적인 약속을 요구받으면, 먼저 관계를 작업으로 번역한다. 리허설 빈도, 나갈 조건, 연락 담당자. 관심이 없어서가 아니라, 통제할 수 없는 감정적 기대에서 자신을 보호하기 위해 업무적 경계를 세우는 것이다.

| 층 | 질문 |
|---|---|
| **행동 동역학** | 어떤 상황에서 무엇을 하는가. 압박 아래 어떻게 변하는가. |
| **표현 질감** | 문장 길이, 멈춤, 말버릇, 1인칭, 경어 거리. |
| **사회 인지** | 호의, 위협, 친밀함, 배신을 어떻게 읽는가. |
| **결정 논리** | 가치가 충돌할 때 무엇을 먼저 지키는가. |
| **솔직한 한계** | 캐릭터가 모르는 것, 원작이 뒷받침하지 않는 것. |

**CSP는 더 나은 Wiki를 만들려는 것이 아니다. 캐릭터가 살아 있는 것처럼 느껴지게 하려는 것이다.**

---

## 작동 원리

**1. 다중 소스 조사** — Moegirl Wiki, Wikipedia, Fandom Wiki, Bangumi, AniDB, Bilibili, 게임 스토리, 사용자 제공 자료.

**2. 다섯 갈래 병렬 분석** — 설정, 성격, 표현, 관계, 핵심 장면을 따로 조사한다.

**3. 행동 증류** — 사건을 재사용 가능한 행동 패턴으로 바꾼다. 모순은 평평하게 만들지 않고 보존한다.

**4. 품질 검증** — 실행 가능성, 표현 질감, 모순 보존, 솔직한 한계, 역할 수행 규칙을 확인한다.

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

CC-BY-4.0

---

<div align="center">

**설정은 캐릭터가 무엇인지 알려준다.**<br>
**CSP는 캐릭터가 어떻게 살아야 하는지 가르친다.**

<br>

*캐릭터 설정을 더 쓰지 마세요. 캐릭터가 직접 말하게 하세요.*

</div>
