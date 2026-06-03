<div align="center">

# Character Skill Producer

### Convierte personajes de anime y videojuegos en Agent Skills ejecutables.

> *"Deja de escribir fichas de personaje. Haz que el personaje hable."*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Runtime-Claude Code](https://img.shields.io/badge/Runtime-Claude%20Code-blueviolet)](#instalación)
[![Local Research](https://img.shields.io/badge/Local%20Research-Moegirl%20API-orange)](#investigación-local-primero)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<br>

**CSP destila personajes de anime, manga y videojuegos en skills de comportamiento para conversación, escritura y narrativa interactiva.**

Dale un nombre de personaje y una obra. CSP investiga fuentes, valida evidencias, destila patrones de comportamiento, ejecuta comprobaciones de calidad y genera un `SKILL.md` con fecha de investigación, límites de fuentes y ruta de actualización.

Hoy sirve para conversar con personajes, escribir fanfiction y prototipar escenas o diálogos. En el futuro puede convertirse en la capa de comportamiento de personajes para ficción interactiva con IA, juegos guiados por personajes y flujos creativos de anime/videojuegos.

[Ejemplos](#ejemplos) · [Filosofía del producto](#filosofía-del-producto) · [Escenarios futuros](#escenarios-futuros) · [Instalación](#instalación) · [Cómo funciona](#cómo-funciona) · [Fechas de investigación](#fechas-de-investigación-y-actualizaciones)

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
> Destila a Togawa Sakiko de BanG Dream! Ave Mujica
> Haz un skill de Hitori Gotoh de Bocchi the Rock!
```

Una vez generado, puedes invocarlo así:

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

Esto no es pegar citas. CSP destila la lógica de comportamiento del personaje: cómo maneja relaciones, presión, límites y decisiones.

---

## Filosofía del producto

CSP trata a un personaje como **un sistema de reacción ejecutable**, no como una página de perfil estática.

Una wiki te dice qué le ocurrió al personaje. Una ficha te dice sus rasgos generales. CSP va más allá: cuando el personaje entra en una situación que la obra original nunca escribió, qué nota primero, qué malinterpreta, qué protege, qué rechaza y con qué ritmo habla.

| Lo que CSP codifica | Qué significa |
|---|---|
| Lente conductual | Qué nota y qué ignora el personaje |
| Reglas de reacción | Cuándo se acerca, huye, ataca o guarda silencio |
| ADN expresivo | Longitud de frases, pausas, distancia honorífica, pronombres, fuga emocional |
| Algoritmo relacional | Cómo lee bondad, traición, cercanía y ser utilizado |
| Límite de decisión | Qué protege primero cuando los valores chocan |
| Límites honestos | Qué no sabe, qué está desactualizado, qué es solo inferencia |

**Lo que puede codificarse se vuelve comportamiento. Lo que no puede codificarse se vuelve límite.** Ese límite también forma parte de la inmersión: un personaje creíble no lo sabe todo ni responde siempre de forma perfecta.

---

## Escenarios futuros

CSP ofrece una capa reutilizable de comportamiento de personajes para creadores.

Hoy puede usarse para:

| Escenario | Uso | Qué aporta CSP |
|---|---|---|
| Conversación con personajes | Hablar con un personaje a lo largo del tiempo | Voz estable, distancia relacional, límite de conocimiento |
| Fanfiction | Redactar diálogos, monólogos internos y escenas breves | Lógica de comportamiento, no solo líneas |
| Prototipado de escenas | Poner al personaje en una situación nueva | Reacciones inferidas desde patrones de comportamiento |
| Estudio de personajes | Comparar cómo manejan presión y relaciones | Fuentes trazables y cadena de destilación |
| Escenas multicaste | Cargar varios personajes en un mismo evento | Límites y lógica de decisión independientes |

Direcciones futuras:

| Dirección | Forma posible |
|---|---|
| Ficción interactiva con IA | Personajes que responden de forma consistente a las acciones del jugador |
| Novela visual / prototipo galgame con IA | Skills que impulsan diálogo ramificado, cambios de afecto y escalada de conflicto |
| Experimentos narrativos multicaste | Varios skills chocan en un mismo evento y generan drama coral |
| Mesa de trabajo para creadores | Probar escenas, reescribir diálogos y detectar desvíos OOC |
| Archivos de personaje actualizables | Nuevas historias actualizan fechas de investigación y patrones de comportamiento |

CSP ofrece a los creadores una capa reutilizable de comportamiento de personajes. Hoy sirve para conversación y fanfiction; mañana puede formar parte de ficción interactiva con IA, juegos guiados por personajes y herramientas creativas de anime/videojuegos.

---

## Investigación local primero

La dirección de CSP es: **las fuentes centrales se obtienen primero con scripts del repositorio; la búsqueda web externa es un complemento.**

Ejemplos actuales:

```bash
python scripts/source_search.py "高松灯" --work "BanG Dream! It's MyGO!!!!!" --mode discover
python scripts/source_search.py "能天使" --work "明日方舟" --sources moegirl
python scripts/moegirl_api.py "高松灯" --search
python scripts/moegirl_api.py "能天使" --full
```

La investigación local actual se centra en la API MediaWiki de Moegirl Wiki mediante `source_search.py`. Más adelante se pueden añadir adaptadores para Bangumi, Fandom, Wikipedia, Bestdori y BWIKI. Si falta un adaptador o falla, CSP registra el fallo y permite complementar con búsqueda web o materiales del usuario.

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

- Python, para investigación local, generación de metadata y comprobaciones de calidad
- Capacidad de búsqueda web como respaldo opcional cuando los scripts locales no cubren una fuente

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

## Cómo funciona

CSP usa por defecto generación de máxima fidelidad.

**1. Descubrimiento local de fuentes** — Ejecuta `scripts/source_search.py` y adaptadores de sitio antes de usar búsqueda externa.

**2. Índice estructurado de fuentes** — Escribe `references/sources.json` con URLs, niveles de fuente, fechas de consulta, fallos y content hash opcional.

**3. Cinco líneas de investigación** — Ambientación, personalidad, expresión, relaciones y escenas clave se investigan por separado.

**4. Destilación conductual** — Los eventos se transforman en patrones de comportamiento reutilizables. Las contradicciones se preservan en lugar de aplanarse.

**5. Metadata y límites** — Genera `manifest.json` con fechas de investigación, medios cubiertos, material no cubierto, puntuación de calidad y honesty boundary.

**6. Validación de calidad** — Comprueba ejecutabilidad, textura expresiva, contradicciones, límites honestos, fechas de investigación y reglas de role-play.

```bash
python scripts/quality_check.py examples/yahata-umiri/
python scripts/merge_research.py examples/yahata-umiri/
python scripts/generate_manifest.py examples/yahata-umiri/
```

---

## Fechas de investigación y actualizaciones

Cada skill de personaje generado registra la fecha de finalización de la investigación.

Cuando aparece un nuevo episodio, evento de juego, línea, entrevista o revisión de configuración después de esa fecha, el skill antiguo puede no cubrirlo. En ese caso, el personaje debe decir:

```text
Mis materiales están actualizados hasta YYYY-MM-DD, así que puede que no cubra contenido publicado después. Si tienes la versión más reciente de CSP o puedes proporcionar enlaces a nueva historia / fuentes, puedo ayudarte a actualizar este Skill; esto puede consumir algunos tokens.
```

CSP actualiza skills antiguos leyendo `manifest.json` y `sources.json`, revisando fuentes centrales, redestilando solo las dimensiones afectadas y renovando la fecha de investigación y el informe de calidad.

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
