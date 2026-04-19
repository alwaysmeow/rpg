class Panel:
    """
    Базовый класс для всех HUD-панелей.

    Каждая панель владеет своими pyglet-объектами и знает
    свои границы (x, y, w, h). Layout вызывает эти методы —
    панель не знает ничего о соседях или окне.
    """

    def resize(self, x: int, y: int, w: int, h: int) -> None:
        """Пересчитать позиции внутренних объектов под новый прямоугольник."""

    def update(self, snapshot, dt: float) -> None:
        """Обновить состояние из снапшота и продвинуть анимации на dt секунд."""

    def delete(self) -> None:
        """Удалить все pyglet-объекты панели."""

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool:
        """Обработать нажатие мыши. Вернуть True, если событие поглощено."""
        return False

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int) -> bool:
        """Обработать drag мыши. Вернуть True, если событие поглощено."""
        return False

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> bool:
        """Обработать отпускание мыши. Вернуть True, если событие поглощено."""
        return False
