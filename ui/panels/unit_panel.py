import pyglet
from pyglet import shapes

from ui.panel import Panel
from ui.hud.unit_card import UnitCard, CARD_W, CARD_H
from ui.color import Color

CARD_GAP = 8


class UnitPanel(Panel):
    def __init__(
        self,
        team_index: int,
        batch: pyglet.graphics.Batch,
        group_bg, group_bar, group_text,
    ):
        self.team_index = team_index
        self._batch = batch
        self._g_bg, self._g_bar, self._g_text = group_bg, group_bar, group_text

        self._x = self._y = self._w = self._h = 0
        self._cards: dict[int, UnitCard] = {}

    # ------------------------------------------------------------------

    def resize(self, x: int, y: int, w: int, h: int) -> None:
        self._x, self._y, self._w, self._h = x, y, w, h
        self._reposition_cards()

    def update(self, snapshot, dt: float) -> None:
        if snapshot is None:
            return

        entities = snapshot.entities
        units: dict[int, dict] = {}
        abilities: dict[int, dict] = {}

        for eid_raw, data in entities.items():
            eid = int(eid_raw)
            tags = data.get("Tags", [])
            if "Unit" in tags:
                team = data.get("CombatParticipation", {}).get("team_index")
                if team == self.team_index:
                    units[eid] = data
            if "Ability" in tags:
                abilities[eid] = data

        ability_by_owner: dict[int, dict] = {}
        for ab in abilities.values():
            owner_id = ab.get("Owner", {}).get("unit_id")
            if owner_id is not None:
                ability_by_owner[int(owner_id)] = ab

        # Синхронизируем набор карточек
        current_ids = set(units.keys())
        card_ids    = set(self._cards.keys())

        for eid in card_ids - current_ids:
            self._cards.pop(eid).delete()

        if current_ids - card_ids:
            for eid in sorted(current_ids - card_ids):
                self._cards[eid] = self._make_card(eid)
            self._reposition_cards()

        for eid, card in self._cards.items():
            card.update(units[eid], ability_by_owner.get(eid), dt)

    def delete(self) -> None:
        for card in self._cards.values():
            card.delete()
        self._cards.clear()

    # ------------------------------------------------------------------

    def _make_card(self, unit_id: int) -> UnitCard:
        return UnitCard(
            self._x, self._y,          # позиция поставится в _reposition_cards
            self.team_index,
            self._batch,
            self._g_bg, self._g_bar, self._g_text,
        )

    def _reposition_cards(self) -> None:
        """Расставить карточки сверху вниз по _y + _h."""
        top = self._y + self._h     # pyglet: y растёт вверх
        for i, card in enumerate(self._cards.values()):
            cy = top - (i + 1) * CARD_H - i * CARD_GAP
            card.move(self._x, cy)
