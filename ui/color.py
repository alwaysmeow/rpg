from enum import Enum

class Color(Enum):
    BACKGROUND = (252, 242, 240, 255)

    COMBAT_BG     = (200, 200, 230, 200)
    COMBAT_ACTIVE = (80, 200, 120, 255)
    COMBAT_DONE   = (180, 180, 60, 255)
    COMBAT_TEXT   = (220, 220, 220, 255)
    COMBAT_LABEL  = (20, 20, 30, 255)

    UNIT_BG       = (212, 203, 203, 220)
    UNIT_BORDER   = (80, 80, 120, 255)
    UNIT_HP_BG    = (251, 187, 187, 255)
    UNIT_HP_FG    = (245, 66, 66, 255)
    UNIT_CD_BG    = (20, 20, 60, 255)
    UNIT_CD_FG    = (80, 140, 240, 255)
    UNIT_DEAD     = (120, 40, 40, 180)
    UNIT_TEXT     = (59, 49, 49, 255)
    UNIT_LABEL    = (150, 150, 170, 255)

    UNIT_TEAM_0   = (80, 160, 240, 255)
    UNIT_TEAM_1   = (240, 100, 80, 255)

    @property
    def rgb(self):
        return self.value[:3]

    @property
    def rgba(self):
        return self.value

    @property
    def red(self):
        return self.value[0]
    
    @property
    def green(self):
        return self.value[1]
    
    @property
    def blue(self):
        return self.value[2]

    @property
    def alpha(self):
        return self.value[3]
    
    def __iter__(self):
        return iter(self.value)