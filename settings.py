class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        """初始化设置"""
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        self.ship_speed = 1.5
        self.ship_limit = 3

        self.bullet_speed = 1.2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        self.alien_speed = 0.1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1