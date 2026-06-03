<div align="center">

# Character Skill Producer

> *"Deja de escribir fichas de personaje. Haz que el personaje hable."*

**Estado:** estándar Agent Skills · runtime Claude Code · licencia MIT

<br>

**CSP convierte personajes de anime y videojuegos en Agent Skills ejecutables.**

Dale un nombre de personaje y una obra. CSP investiga, valida con varias fuentes, destila patrones de comportamiento y genera un `SKILL.md` instalable con el que puedes conversar directamente.

No es una ficha de personaje. No es una enciclopedia de lore. No es una lista de etiquetas como "tsundere" o "fría y distante".

CSP captura **cómo reacciona el personaje, cómo habla, cómo interpreta a los demás, cómo decide y dónde debe admitir que no sabe.**

[Ejemplos](#ejemplos) · [Instalación](#instalación) · [Qué destila CSP](#qué-destila-csp) · [Cómo funciona](#cómo-funciona) · [Personajes incluidos](#personajes-incluidos)

<br>

**Otros idiomas:**

[中文](README.md) · [English](README_EN.md) · [日本語](README_JA.md) · [한국어](README_KO.md)

</div>

---

## Ejemplos

No necesitas ingeniería de prompts ni una carpeta de lore escrita a mano.

Solo di:

```text
> Genera un skill de Misaka Mikoto de A Certain Scientific Railgun
> Destila a Maki Shiina de BanG Dream! It's MyGO!!!!!
> Haz un skill de personaje de Gojo Satoru
```

CSP convierte información de personaje en comportamiento ejecutable. Una vez generado, puedes invocarlo así:

```text
Usuario  ❯ Habla desde la perspectiva de Umiri. ¿Por qué alguien apoyaría a tantas bandas?

Umiri    ❯ Porque así todo queda claro.
           Ensayo hoy, concierto mañana, y luego termina.
           Hago lo que hace falta.

           Las relaciones largas son más difíciles.
           La gente empieza a esperar que te quedes. Preguntan qué significa este lugar para ti.

           ...Pero si solo apoyas a otros todo el tiempo, se siente un poco vacío.
           Eso lo sé.
```

Esto no es pegar citas. CSP destila la lógica de comportamiento que sostiene al personaje.

---

## Instalación

CSP es un meta-skill en estilo Claude Code / Agent Skills. Instala la versión autocontenida:

```bash
skills add qian-gugugaga/Character_Skill_Producer
```

O instala manualmente:

```bash
git clone https://github.com/qian-gugugaga/Character_Skill_Producer.git
cp -r Character_Skill_Producer/examples/csp ~/.claude/skills/csp
```

`examples/csp/` ya incluye los scripts y plantillas necesarios.

### Requisitos

- Python, para el helper de la API MediaWiki de Moegirl Wiki
- Capacidad de búsqueda web, para Wikipedia, Fandom Wiki, Bangumi, Bilibili y fuentes de respaldo

---

## Uso

Después de instalar, dile a Claude Code:

```text
> /csp
> Genera un skill de Chihaya Anon
> Destila a Togawa Sakiko de BanG Dream! Ave Mujica
> Haz un skill de Hitori Gotoh de Bocchi the Rock!
```

También funcionan solicitudes vagas:

```text
> Quiero hablar con un personaje tsundere
> ¿Recomiendas algún personaje yandere?
> Hazme un personaje 2D adecuado para conversaciones largas
```

Si tienes materiales oficiales, entrevistas, subtítulos, capturas o texto de historias de juego, dáselos a CSP. El material oficial proporcionado por el usuario tiene la máxima prioridad.

---

## Qué destila CSP

Una ficha normal diría:

> Personalidad: calmada, confiable, distante.

CSP escribe algo ejecutable:

> Cuando se le pide un compromiso a largo plazo, primero traduce la relación en tareas: frecuencia de ensayos, condiciones de salida, quién coordina. No porque no le importe, sino porque los límites operativos la protegen de expectativas emocionales que no puede controlar.

| Capa | Pregunta |
|---|---|
| **Dinámica de comportamiento** | Qué hace en cada situación. Cómo cambia bajo presión. |
| **Textura expresiva** | Longitud de frases, pausas, muletillas, pronombres, distancia honorífica. |
| **Cognición social** | Cómo lee la bondad, la amenaza, la cercanía y la traición. |
| **Lógica de decisión** | Qué protege primero cuando los valores chocan. |
| **Límites honestos** | Qué no sabe el personaje. Qué no sostiene el material original. |

**CSP no intenta ser una wiki mejor. Intenta hacer que el personaje se sienta vivo.**

---

## Cómo funciona

**1. Investigación multi-fuente** — Moegirl Wiki, Wikipedia, Fandom Wiki, Bangumi, AniDB, Bilibili, historias de juego y materiales del usuario.

**2. Cinco líneas paralelas de análisis** — ambientación, personalidad, expresión, relaciones y escenas clave se investigan por separado.

**3. Destilación conductual** — los eventos se transforman en patrones de comportamiento reutilizables. Las contradicciones se preservan en lugar de aplanarse.

**4. Validación de calidad** — se verifica ejecutabilidad, textura expresiva, contradicciones preservadas, límites honestos y reglas completas de role-play.

---

## Personajes incluidos

| Personaje | Obra | Directorio |
|---|---|---|
| Takamatsu Tomori | BanG Dream! It's MyGO!!!!! | `examples/takamatsu-tomori/` |
| Shiina Taki | BanG Dream! It's MyGO!!!!! | `examples/taki-shiina/` |
| Kaname Rana | BanG Dream! It's MyGO!!!!! | `examples/kaname-rana/` |
| Nagasaki Soyo | BanG Dream! It's MyGO!!!!! | `examples/nagasaki-soyo/` |
| Chihaya Anon | BanG Dream! It's MyGO!!!!! | `examples/chihaya-anon/` |
| Togawa Sakiko | BanG Dream! Ave Mujica | `examples/togawa-sakiko/` |
| Mutsumi Wakaba | BanG Dream! Ave Mujica | `examples/mutsumi-wakaba/` |
| Misumi Uika | BanG Dream! Ave Mujica | `examples/misumi-uika/` |
| Yutenji Nyamu | BanG Dream! Ave Mujica | `examples/yutenji-nyamu/` |
| Yahata Umiri | BanG Dream! Ave Mujica | `examples/yahata-umiri/` |
| CSP self-skill | — | `examples/csp/` |

---

## Licencia

MIT

---

<div align="center">

**El lore te dice qué es un personaje.**<br>
**CSP le enseña al personaje cómo vivir.**

<br>

*Deja de escribir fichas de personaje. Haz que el personaje hable.*

</div>
