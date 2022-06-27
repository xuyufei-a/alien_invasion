import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self, "Play")
        self.score_board = Scoreboard(self)
        
        self._create_fleet()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_aliens()
              
            self._update_screen()

    def _check_events(self):
        """响应鼠标和按键事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_keydown_event(self, event):
        """响应按键"""
        if event.key == pygame.K_q:
            self._quit_game()
        elif self.stats.game_active:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
        elif not self.stats.game_active and event.key == pygame.K_p:
            self._start_game()
       

    def _check_keyup_event(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """响应play按钮被按下"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if not self.stats.game_active and button_clicked:
            self._start_game()

    def _start_new_ship(self):
        self.bullets.empty()
        self.aliens.empty()       
        self._create_fleet()
        self.ship.center_ship()

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.game_active = True
        self.stats.reset_stats()
        self._start_new_ship()

        self.score_board.prep_score()
        self.score_board.prep_level()
        self.score_board.prep_ships()
        pygame.mouse.set_visible(False)

    def _quit_game(self):
        self.stats.write_high_score()
        sys.exit()

    def _create_fleet(self):
        """创建外星人群"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height
        available_space_x = self.settings.screen_width - alien_width
        available_space_y = (self.settings.screen_height - 
                                alien_height * 3 - ship_height)

        number_aliens_x = available_space_x // (2 * alien_width)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(row_number, alien_number)

    def _create_alien(self, row_number, alien_number):
        """创建一个外星人并将其置于当前行""" 
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height * 2 + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        """绘制屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.score_board.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入到编组bullets中"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullet(self):
        """更新子弹，并删除消失的子弹"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        collisions = pygame.sprite.groupcollide(self.bullets, 
            self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.score_board.prep_score()
            self.score_board.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.score_board.prep_level()

    def _update_aliens(self):
        """
        检查是否有外星人位于屏幕边缘，
            并更新整群外星人的位置
        """
        self._check_fleet_edges()
        self.aliens.update()

        if (pygame.sprite.spritecollideany(self.ship, self.aliens)
        or self._check_aliens_bottom()):
            self._ship_hit()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移并改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """在有外星人到达底部时返回True"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                return True
        return False

    def _ship_hit(self):
        """响应飞船与外星人碰撞"""
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.score_board.prep_ships()
            self._start_new_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()