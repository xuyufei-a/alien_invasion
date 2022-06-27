class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.score_filename = "high_score.txt"
        self.level = 1
        self._get_high_score()

    def reset_stats(self):
        """初始化在游戏运行期间可能发生变化的量"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
    def _get_high_score(self):
        try:
            with open(self.score_filename) as f:
                content = f.read().strip()
                self.high_score = int(content)
        except FileNotFoundError:
            self.high_score = 0

    def write_high_score(self):
        with open(self.score_filename, 'w') as f:
            f.write(str(self.high_score))