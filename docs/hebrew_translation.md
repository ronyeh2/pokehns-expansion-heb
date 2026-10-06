# Hebrew translation guide (Heart & Soul)

Everything here is about the Hebrew branches of this fork (`he/*`). None of it applies to upstream
Heart & Soul. The tools named here live in `tools/hebrew/` (copied from the working directory
`hns-tools/` the translation was built with).

## How Hebrew is stored

`charmap.txt` maps the alphabet onto bytes that no Latin character uses, so leftover English
(`POKéMON`, whose `é` is `0x1B`) keeps rendering:

| Letters | Bytes |
| --- | --- |
| א ב ג ד ה ו ז ח ט י כ ל מ נ ס ע פ צ ק ר ש ת | `0x3A`–`0x4F`, in alphabetical order |
| ך | `0x50` |
| ם ן ף ץ | `0x5E`–`0x61` |
| ◀ (the right-to-left menu cursor) | `0x87` |

`include/constants/characters.h` names them (`CHAR_HEB_ALEF` … `CHAR_HEB_FINAL_TSADI`,
`IS_HEBREW_CHAR`). The geresh is the ASCII apostrophe (byte `0xB4`, as in FireRed), the
gershayim is `”` (`0xB2`). There is no straight double quote.

**Write Hebrew in logical order, and write numbers the way you read them.** Unlike the FireRed
fork, digits are never reversed: the renderer draws Latin and digit runs left to right.

## How right-to-left works

All of it is in `src/text.c` (the `#if TEXT_RTL` block, switched on in `include/config/text.h`)
and `src/window.c`.

**The logical pen is upstream's.** A window printer's `x`, `currentX`, `{CLEAR_TO}`, `{SKIP}` and
every layout computed with `GetStringWidth` mean what they mean in English. Only the blit is
mirrored: a glyph at logical `x`, `w` pixels wide, lands at `axis - x - w`. So a string that fits
in English fits in Hebrew, and no call site needs an "RTL anchor".

**Runs.** When a printer meets a Latin letter or a digit (or a currency sign, plus or minus
before a digit), it measures the run up to the last Latin letter or digit before the next Hebrew
letter or pen-moving code, and draws the run left to right as one block at its mirrored place.
Neutrals between two run characters belong to the run; neutrals after it take the paragraph's
direction. Colour codes, pauses, sounds and leftover placeholder bytes do not end a run.

**Mirrored glyphs.** Outside a run, `( ) < >` swap with their partners and the menu cursor `▶`
becomes `◀`. Arrow characters are left alone: they show physical directions.

**Windows have modes** (`include/window.h`):

| Mode | What it does | Used for |
| --- | --- | --- |
| `WINDOW_RTL_MIRROR` (default) | Glyphs and the window primitives (`FillWindowPixelRect`, `BlitBitmapRectToWindow`, the 8-bit variants, `FillWindowTilesByRow`) mirror around the window's mirror width, so cursors and icons move with the text | Dialogue, lists, menus, plain boxes |
| `WINDOW_RTL_IN_PLACE` | Each text segment (up to a newline or a pen-moving code) reads right to left inside the extent it has in English; fills and blits stay. A segment with no Hebrew keeps the English layout | Text in fixed boxes on art, next to sprites or tilemap cursors, or prints that only line up in English (party slots, battle menus, the level-up banner, healthbox scratch windows, the ability pop-up, the bag pocket title, the PC box title) |
| `WINDOW_RTL_LTR` | Untouched | |

Set a mode with `SetWindowRtlMode(windowId, mode)` right after the window is created (it resets
on `InitWindows`, `AddWindow`, `RemoveWindow` and `FreeAllWindowBuffers`). A window whose box art
is narrower than the window mirrors around a smaller axis: `SetWindowRtlMirrorWidth(id, px)`.
The overworld dialogue box uses 208 px (26 tiles), because its frame pads only the left side;
the Pokédex windows use the visible 240 px of their 256-px windows.

**Sprite text** (the healthbox) is printed immediately, so the string is reordered into visual
order and printed left to right in its English position.

## Other engine changes

- `IsStringJapanese` does not count Hebrew letters as kana.
- Battle text puts "wild"/"opposing" after the name (`TEXT_NAME_SUFFIX_IN_BATTLE`), so the
  prefix strings hold `" פראי"` and `" יריב"`. The ability pop-up drops the English possessive.
- The speaker name box sits at the right end of the dialogue box.
- The start-menu clock is one 24-hour string.
- Grid menus swap LEFT and RIGHT in mirrored windows.
- The Pokédex name search groups the Hebrew alphabet three letters at a time; the list falls
  back to the narrower font when a name is wider than its column; the A–Z order is generated from
  the Hebrew names (`gen_dex_alpha.py`).
- The healthbox drops the level glyph when glyph and digits do not fit (level 100).

## Fonts

All nine Latin fonts carry the Hebrew letters, the left cursor `◀` and a Hebrew level glyph
(`רמה`, replacing `Lv` at `0x34` and `0x105`). Widths are in the tables in `src/fonts.c`; the
advance is the table value, nothing else. `tools/hebrew/textwidth.py` reads those tables.

## Budgets

Measure, do not count characters. The most common budgets (all from `notes/budgets.md`):

| Kind | Font | Width | Lines |
| --- | --- | --- | --- |
| Overworld dialogue and signs | normal | 208 px (200 on a line that ends in `\l` or `\p`) | 2 |
| Battle text | normal | 208 px | 2 |
| Item description | normal | 102 px | 3 |
| Move description (summary) | normal | 152 px | 2 |
| Ability description | small | 139 px | 1 |
| Pokédex entry | normal | 224 px | 3 |

Hard byte limits: species 12, move 16, ability 16, item 19, type 8, trainer name 10, trainer
class 12, berry 6, map name 19; an expanded message under 999 bytes (`gStringVar4`), a battle
message under 424.

## Tools and the workflow

| Tool | What it does |
| --- | --- |
| `units.py` | Extracts every live string into JSON units and writes translations back, refusing any change outside the string |
| `make_chunks.py` | Cuts batches into chunks, pre-fills names from the glossary |
| `checkunits.py` | Validates a chunk: tokens, `$`, escapes, charset, digits, widths, lines |
| `drift.py` | Compares a translated file with the English baseline: only strings may differ |
| `namecheck.py`, `glossary_widths.py` | Glossary byte limits, final letters, duplicates, on-screen widths |
| `apply_names.py` | Writes trainer and map-section names (`.party`, JSON) |
| `textwidth.py`, `audit.py`, `wrap.py` | The width model, a whole-tree budget audit, a re-wrapper |
| `rom_sweep.py` | Finds English left in a built ROM |
| `gen_dex_alpha.py` | Regenerates the Pokédex A–Z order |
| `emu/` | Headless mGBA harness, the save ladder and the screen tours (`hns.py tour`) |

## What is left / what this cannot see

Kept up to date in `TESTING.md` of each build and in the release notes.
