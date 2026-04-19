import pyglet
from pyglet import shapes

from ui.panel import Panel
from ui.hud.resource_bar import ResourceBar
from ui.color import Color

PADDING   = 12
FONT_NAME = "Courier New"

# Размеры баров
BAR_H    = 22
BAR_GAP  = 8

# Строки статов
STAT_FONT   = 11
STAT_H      = 16
STAT_GAP    = 4


class StatsPanel(Panel):
    """
    Правая панель: подробные статы одного юнита.

    Юнит выбирается вручную через select(unit_id).

    Показывает:
      - имя + тег команды
      - HP / MP (если есть) / Stamina (если есть) бары
      - Armor, Magic Resistance, Attack Speed, атрибуты (если есть)
    """

    def __init__(self, batch, group_bg, group_bar, group_text):
        self._batch  = batch
        self._g_bg   = group_bg
        self._g_bar  = group_bar
        self._g_text = group_text

        self._x = self._y = self._w = self._h = 0

        # Выбранный юнит
        self._selected_id: int | None = None

        # Заголовок
        self._header_bg:   shapes.RoundedRectangle | None = None
        self._name_label:  pyglet.text.Label | None = None
        self._team_label:  pyglet.text.Label | None = None

        # Ресурс-бары
        self._hp_bar: ResourceBar | None = None
        self._mp_bar: ResourceBar | None = None
        self._st_bar: ResourceBar | None = None
        self._has_mp: bool | None = None
        self._has_st: bool | None = None

        # Строки атрибутов  {key: Label}
        self._stat_labels: dict[str, pyglet.text.Label] = {}

        # «нет данных»
        self._empty_label: pyglet.text.Label | None = None

        self._built = False

    # ------------------------------------------------------------------
    # Panel interface
    # ------------------------------------------------------------------

    def resize(self, x: int, y: int, w: int, h: int) -> None:
        self._x, self._y, self._w, self._h = x, y, w, h
        self._full_rebuild()

    def update(self, snapshot, dt: float) -> None:
        if snapshot is None:
            return

        entities = snapshot.entities

        # Собираем юнитов
        units: dict[int, dict] = {
            int(eid): data
            for eid, data in entities.items()
            if "Unit" in data.get("Tags", [])
        }

        if not units:
            self._show_empty("No units")
            return

        if self._selected_id is None:
            self._show_empty("Click a unit")
            return

        if self._selected_id not in units:
            self._selected_id = None
            self._show_empty("Unit not found")
            return

        data = units[self._selected_id]

        # Определяем наличие ресурсов
        mana    = data.get("Mana", {})
        stamina = data.get("Stamina", {})
        has_mp  = bool(mana)
        has_st  = bool(stamina)

        if has_mp != self._has_mp or has_st != self._has_st or not self._built:
            self._has_mp = has_mp
            self._has_st = has_st
            self._full_rebuild()

        self._hide_empty()

        # Имя и команда
        name  = data.get("Name", {}).get("name", "???")
        team  = data.get("CombatParticipation", {}).get("team_index", 0)
        alive = "Dead" not in data.get("Tags", [])

        if self._name_label:
            self._name_label.text  = name
            self._name_label.color = Color.UNIT_TEXT.rgba if alive else (180, 60, 60, 220)
        if self._team_label:
            tc = Color.UNIT_TEAM_0 if team == 0 else Color.UNIT_TEAM_1
            self._team_label.text  = f"Team {team + 1}"
            self._team_label.color = (*tc.rgb, 220)

        # HP
        health   = data.get("Health", {})
        hp_ratio = health.get("_value_ratio", 1.0)
        hp_max   = health.get("effective_max_value", 100)
        if self._hp_bar:
            self._hp_bar.set_target(hp_ratio, f"HP  {round(hp_ratio * hp_max)}/{hp_max}")
            self._hp_bar.tick(dt)

        # MP
        if self._mp_bar and mana:
            mp_ratio = mana.get("_value_ratio", 1.0)
            mp_max   = mana.get("effective_max_value", 100)
            self._mp_bar.set_target(mp_ratio, f"MP  {round(mp_ratio * mp_max)}/{mp_max}")
            self._mp_bar.tick(dt)

        # Stamina
        if self._st_bar and stamina:
            st_ratio = stamina.get("_value_ratio", 1.0)
            st_max   = stamina.get("effective_max_value", 100)
            self._st_bar.set_target(st_ratio, f"ST  {round(st_ratio * st_max)}/{st_max}")
            self._st_bar.tick(dt)

        # Статы
        self._update_stat_labels(data)

    def delete(self) -> None:
        self._clear_all()

    # ------------------------------------------------------------------
    # Публичный API
    # ------------------------------------------------------------------

    def select(self, unit_id: int) -> None:
        """Выбрать юнит вручную."""
        self._selected_id = unit_id

    def deselect(self) -> None:
        self._selected_id = None

    @property
    def selected_id(self) -> int | None:
        return self._selected_id

    # ------------------------------------------------------------------
    # Внутренние методы
    # ------------------------------------------------------------------

    def _full_rebuild(self) -> None:
        self._clear_all()
        if self._w < 10 or self._h < 10:
            return

        x, y, w, h = self._x, self._y, self._w, self._h
        bw = w - PADDING * 2    # ширина баров

        # --- Шапка ---
        header_h = 44
        self._header_bg = shapes.RoundedRectangle(
            x, y + h - header_h, w, header_h, radius=8,
            color=Color.UNIT_BG.rgb, batch=self._batch, group=self._g_bg,
        )
        self._header_bg.opacity = Color.UNIT_BG.alpha

        self._name_label = pyglet.text.Label(
            "", font_name=FONT_NAME, font_size=13,
            x=x + PADDING, y=y + h - header_h // 2,
            anchor_y="center",
            color=Color.UNIT_TEXT.rgba,
            batch=self._batch, group=self._g_text,
        )
        self._team_label = pyglet.text.Label(
            "", font_name=FONT_NAME, font_size=10,
            x=x + w - PADDING, y=y + h - header_h // 2,
            anchor_x="right", anchor_y="center",
            color=Color.UNIT_LABEL.rgba,
            batch=self._batch, group=self._g_text,
        )

        # --- Бары (снизу шапки вниз) ---
        cursor_y = y + h - header_h - PADDING

        active = ["hp"] + (["mp"] if self._has_mp else []) + (["st"] if self._has_st else [])

        for name in active:
            cursor_y -= BAR_H
            bx = x + PADDING
            by = cursor_y
            if name == "hp":
                self._hp_bar = ResourceBar(
                    bx, by, bw, BAR_H,
                    fg_color=Color.UNIT_HP_FG.rgba,
                    bg_color=Color.UNIT_HP_BG.rgba,
                    ghost_color=Color.UNIT_HP_GHOST.rgba,
                    label_text="HP",
                    batch=self._batch,
                    group_bg=self._g_bg, group_bar=self._g_bar, group_text=self._g_text,
                )
            elif name == "mp":
                self._mp_bar = ResourceBar(
                    bx, by, bw, BAR_H,
                    fg_color=Color.UNIT_CD_FG.rgba,
                    bg_color=Color.UNIT_CD_BG.rgba,
                    ghost_color=Color.COMBAT_DONE.rgba,
                    label_text="MP",
                    batch=self._batch,
                    group_bg=self._g_bg, group_bar=self._g_bar, group_text=self._g_text,
                )
            elif name == "st":
                self._st_bar = ResourceBar(
                    bx, by, bw, BAR_H,
                    fg_color=Color.COMBAT_ACTIVE.rgba,
                    bg_color=Color.UNIT_CD_BG.rgba,
                    ghost_color=Color.COMBAT_DONE.rgba,
                    label_text="ST",
                    batch=self._batch,
                    group_bg=self._g_bg, group_bar=self._g_bar, group_text=self._g_text,
                )
            cursor_y -= BAR_GAP

        # --- Разделитель ---
        cursor_y -= 6

        # --- Строки атрибутов ---
        self._stat_labels = {}
        stat_keys = self._stat_key_order()
        for key in stat_keys:
            cursor_y -= STAT_H
            lbl = pyglet.text.Label(
                "", font_name=FONT_NAME, font_size=STAT_FONT,
                x=x + PADDING, y=cursor_y,
                color=Color.UNIT_LABEL.rgba,
                batch=self._batch, group=self._g_text,
            )
            self._stat_labels[key] = lbl
            cursor_y -= STAT_GAP

        # --- Пустая заглушка ---
        self._empty_label = pyglet.text.Label(
            "", font_name=FONT_NAME, font_size=11,
            x=x + w // 2, y=y + h // 2,
            anchor_x="center", anchor_y="center",
            color=Color.UNIT_LABEL.rgba,
            batch=self._batch, group=self._g_text,
        )

        self._built = True

    def _stat_key_order(self) -> list[str]:
        return [
            "Armor", "MagicResistance",
            "AttackDamage", "AttackSpeed",
            "CritChance", "CritMultiplier",
            "MoveSpeed",
        ]

    def _update_stat_labels(self, data: dict) -> None:
        display = {
            "Armor":           ("Armor",       self._fmt_stat(data, "Armor")),
            "MagicResistance": ("Mag.Res",     self._fmt_stat(data, "MagicResistance")),
            "AttackDamage":    ("Atk.Dmg",     self._fmt_stat(data, "AttackDamage")),
            "AttackSpeed":     ("Atk.Spd",     self._fmt_stat(data, "AttackSpeed")),
            "CritChance":      ("Crit%",        self._fmt_stat(data, "CritChance", pct=True)),
            "CritMultiplier":  ("Crit×",        self._fmt_stat(data, "CritMultiplier")),
            "MoveSpeed":       ("Move.Spd",     self._fmt_stat(data, "MoveSpeed")),
        }
        for key, lbl in self._stat_labels.items():
            label_name, value = display.get(key, (key, "—"))
            if value is not None:
                lbl.text  = f"{label_name:<10}{value}"
                lbl.color = Color.UNIT_LABEL.rgba
            else:
                lbl.text = ""

    @staticmethod
    def _fmt_stat(data: dict, component: str, pct: bool = False) -> str | None:
        comp = data.get(component, {})
        if not comp:
            return None
        val = comp.get("effective_value", comp.get("value"))
        if val is None:
            return None
        if pct:
            return f"{val * 100:.1f}%"
        return f"{val:.1f}" if isinstance(val, float) else str(val)

    def _show_empty(self, text: str) -> None:
        if self._empty_label:
            self._empty_label.text = text

    def _hide_empty(self) -> None:
        if self._empty_label:
            self._empty_label.text = ""

    def _clear_all(self) -> None:
        for obj in (self._header_bg, self._name_label,
                    self._team_label, self._empty_label):
            if obj:
                obj.delete()
        for bar in (self._hp_bar, self._mp_bar, self._st_bar):
            if bar:
                bar.delete()
        for lbl in self._stat_labels.values():
            lbl.delete()
        self._header_bg  = None
        self._name_label = None
        self._team_label = None
        self._empty_label = None
        self._hp_bar = self._mp_bar = self._st_bar = None
        self._stat_labels = {}
        self._built = False
