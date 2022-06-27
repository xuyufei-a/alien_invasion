class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
      
        self.ship_limit = 3

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        self.speedup_scale = 1.1
        self.scale_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.bullet_speed = 1.2  
        self.ship_speed = 1.5
        self.alien_speed = 0.1

        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置"""
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.scale_scale)