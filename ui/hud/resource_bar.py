import pyglet
from pyglet import shapes

class ResourceBar:
    """
    Универсальный бар ресурса (HP, MP, Stamina, Cooldown и т.д.).

    Анимации:
    - _display тянется к _target через lerp (скорость LERP_SPEED).
    - _ghost тянется к _target медленнее (GHOST_SPEED) и рисуется
      позади _display жёлтым цветом — эффект «хвоста» при уроне.
      При восстановлении (target > display) ghost не показывается.

    Использование:
        bar = ResourceBar(x, y, w, h, fg, bg, ghost, label, batch, g_bg, g_bar, g_text)
        bar.set_target(0.6)          # вызывать при каждом update()
        bar.tick(dt)                 # вызывать каждый кадр
    """

    LERP_SPEED  = 6.0   # скорость основного бара (в единицах/сек)
    GHOST_SPEED = 1.8   # скорость ghost-хвоста

    def __init__(
        self,
        x: int, y: int,
        width: int, height: int,
        fg_color: tuple,
        bg_color: tuple,
        ghost_color: tuple,
        label_text: str,
        batch: pyglet.graphics.Batch,
        group_bg,
        group_bar,
        group_text,
    ):
        self._x = x
        self._y = y
        self._max_w = width
        self._h = height

        self._target: float = 1.0
        self._display: float = 1.0
        self._ghost: float = 1.0

        self._bg = shapes.RoundedRectangle(
            x, y, width, height, radius=3,
            color=bg_color[:3], batch=batch, group=group_bg,
        )
        self._bg.opacity = bg_color[3] if len(bg_color) == 4 else 255

        self._ghost_bar = shapes.RoundedRectangle(
            x, y, width, height, radius=3,
            color=ghost_color[:3], batch=batch, group=group_bar,
        )
        self._ghost_bar.opacity = ghost_color[3] if len(ghost_color) == 4 else 200

        self._bar = shapes.RoundedRectangle(
            x, y, width, height, radius=3,
            color=fg_color[:3], batch=batch, group=group_bar,
        )
        self._bar.opacity = fg_color[3] if len(fg_color) == 4 else 255

        self._label = pyglet.text.Label(
            label_text,
            font_name="Courier New", font_size=20,
            x=x, y=y + height + 3,
            color=(50, 50, 90, 200),
            batch=batch, group=group_text,
        )

    # ------------------------------------------------------------------

    def set_target(self, ratio: float, label: str = "") -> None:
        """Задать целевое значение бара (0.0–1.0) и текст метки."""
        self._target = max(0.0, min(1.0, ratio))
        if label:
            self._label.text = label

    def tick(self, dt: float) -> None:
        """Продвинуть анимацию на dt секунд. Вызывать каждый кадр."""
        t = self._target

        # Основной бар — быстрый lerp
        self._display += (t - self._display) * self.LERP_SPEED * dt
        self._display = max(0.0, min(1.0, self._display))

        # Ghost тянется медленнее, но только в сторону уменьшения
        if self._ghost > t:
            self._ghost += (t - self._ghost) * self.GHOST_SPEED * dt
            self._ghost = max(self._display, self._ghost)
        else:
            self._ghost = self._display

        # Обновляем ширины
        self._bar.width = max(0, int(self._max_w * self._display))
        ghost_w = max(0, int(self._max_w * self._ghost))
        self._ghost_bar.width = ghost_w

        # Ghost видим только когда он шире основного бара
        self._ghost_bar.opacity = 180 if self._ghost > self._display + 0.005 else 0

    def move(self, x: int, y: int) -> None:
        """Переместить бар (при resize панели)."""
        dx, dy = x - self._x, y - self._y
        self._x, self._y = x, y
        for obj in (self._bg, self._ghost_bar, self._bar):
            obj.x += dx
            obj.y += dy
        self._label.x += dx
        self._label.y += dy

    def resize_width(self, width: int) -> None:
        """Изменить максимальную ширину (при resize панели)."""
        self._max_w = width
        self._bg.width = width
        # bar и ghost пересчитаются на следующем tick()

    def delete(self) -> None:
        for obj in (self._bg, self._ghost_bar, self._bar, self._label):
            obj.delete()