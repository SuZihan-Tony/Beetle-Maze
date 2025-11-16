import pygame
import easygui
import sys
import os


pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_BG_COLOR = (36, 77, 69)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Beetle Game")

VOLUME = 0.5

### common ###

def resource_path(relative_path):
    """返回适用于开发与打包环境的路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


ICON = pygame.image.load(resource_path("image/sbeetle.png"))
pygame.display.set_icon(ICON)


def draw_text(surface, text, font_size, color, position, font_name = None, center=False):
    # 加载字体
    font = pygame.font.Font(font_name, font_size)

    # 渲染文字到 Surface
    text_surface = font.render(text, True, color)

    # 设置文字显示位置
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = position  # 中心对齐
    else:
        text_rect.topleft = position  # 左上对齐

    # 在屏幕上绘制文字
    surface.blit(text_surface, text_rect)


def button(event, x, y, ele_class, draw_func):
    if event == "down":
        if ele_class.start_pos[0] <= x <= ele_class.start_pos[0] + ele_class.start_size[0] and \
                ele_class.start_pos[1] <= y <= ele_class.start_pos[1] + ele_class.start_size[1]:
            ele_class.start_size[0] -= 6
            ele_class.start_size[1] -= 4
            ele_class.start_img = pygame.transform.scale(ele_class.start_img, ele_class.start_size)
            ele_class.start_pos[0] += 3
            ele_class.start_pos[1] += 2
            ele_class.start_onclick = True
        elif ele_class.exit_pos[0] <= x <= ele_class.exit_pos[0] + ele_class.exit_size[0] and \
                ele_class.exit_pos[1] <= y <= ele_class.exit_pos[1] + ele_class.exit_size[1]:
            ele_class.exit_size[0] -= 6
            ele_class.exit_size[1] -= 4
            ele_class.exit_img = pygame.transform.scale(ele_class.exit_img, ele_class.exit_size)
            ele_class.exit_pos[0] += 3
            ele_class.exit_pos[1] += 2
            ele_class.exit_onclick = True
        elif ele_class.settings_pos[0] <= x <= ele_class.settings_pos[0] + ele_class.settings_size[0] and \
                ele_class.settings_pos[1] <= y <= ele_class.settings_pos[1] + ele_class.settings_size[1]:
            ele_class.settings_size[0] -= 3
            ele_class.settings_size[1] -= 3
            ele_class.settings_img = pygame.transform.scale(ele_class.settings_img, ele_class.settings_size)
            ele_class.settings_pos[0] += 1
            ele_class.settings_pos[1] += 1
            ele_class.settings_onclick = True
        elif game_var.game_over and game_element.game_over_popup_retry_pos[0] <= x <= game_element.game_over_popup_retry_pos[
            0] + game_element.game_over_popup_retry_size[0] and \
                game_element.game_over_popup_retry_pos[1] <= y <= game_element.game_over_popup_retry_pos[
            1] + game_element.game_over_popup_retry_size[1]:
            game_element.game_over_popup_retry_pos[0] += 1
            game_element.game_over_popup_retry_pos[1] += 1
            game_element.game_over_popup_retry_onclick = True
        elif game_var.game_over and game_element.game_over_popup_exit_pos[0] <= x <= game_element.game_over_popup_exit_pos[
            0] + game_element.game_over_popup_exit_size[0] and \
                game_element.game_over_popup_exit_pos[1] <= y <= game_element.game_over_popup_exit_pos[
            1] + game_element.game_over_popup_exit_size[1]:
            game_element.game_over_popup_exit_pos[0] += 1
            game_element.game_over_popup_exit_pos[1] += 1
            game_element.game_over_popup_exit_onclick = True
        draw_func()
    elif event == "up":
        if ele_class.start_pos[0] <= x <= ele_class.start_pos[0] + ele_class.start_size[0] and \
                ele_class.start_pos[1] <= y <= ele_class.start_pos[1] + ele_class.start_size[1] and \
                ele_class.start_onclick:
            if ele_class == element:
                game()
            else:
                reset_game()
        elif ele_class.exit_pos[0] <= x <= ele_class.exit_pos[0] + ele_class.exit_size[0] and \
                ele_class.exit_pos[1] <= y <= ele_class.exit_pos[1] + ele_class.exit_size[1] and \
                ele_class.exit_onclick:
            if ele_class == element:
                pygame.quit()
                sys.exit()
            else:
                game_var.quit = True
        elif ele_class.settings_pos[0] <= x <= ele_class.settings_pos[0] + ele_class.settings_size[0] and \
                ele_class.settings_pos[1] <= y <= ele_class.settings_pos[1] + ele_class.settings_size[1] and \
                ele_class.settings_onclick:
            print("settings")
        elif game_var.game_over and game_element.game_over_popup_retry_pos[0] <= x <= \
                game_element.game_over_popup_retry_pos[0] + game_element.game_over_popup_retry_size[0] and \
                game_element.game_over_popup_retry_pos[1] <= y <= game_element.game_over_popup_retry_pos[1] \
                + game_element.game_over_popup_retry_size[1] and game_element.game_over_popup_retry_onclick:
            reset_game()
        elif game_var.game_over and game_element.game_over_popup_exit_pos[0] <= x <= \
                game_element.game_over_popup_exit_pos[0] + game_element.game_over_popup_exit_size[0] and \
                game_element.game_over_popup_exit_pos[1] <= y <= game_element.game_over_popup_exit_pos[1] + \
                game_element.game_over_popup_exit_size[1] and game_element.game_over_popup_exit_onclick:
            game_var.quit = True
        ele_class.__init__()
        draw_func()


### main func ###

class Element(object):
    def __init__(self):
        if type(self) is Element:
            self.bg_pos = (0, 0)
            self.bg_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
            self.bg = pygame.transform.scale(pygame.image.load(resource_path('image/main_bg.jpg')), self.bg_size)
            start_url = ''
            title_url = 'main_'
        else:
            start_url = 're'
            title_url = ''

        self.start_img = pygame.image.load(resource_path(f'image/{start_url}start.png'))
        self.start_size = list(self.start_img.get_size())
        self.start_pos = [(SCREEN_WIDTH - self.start_size[0]) / 2, 472]
        self.start_onclick = False

        self.title_img = pygame.image.load(resource_path(f'image/{title_url}title.png'))
        self.title_size = self.title_img.get_size()
        self.title_pos = [(SCREEN_WIDTH - self.title_size[0]) / 2 - 5, 25]

        self.exit_img = pygame.image.load(resource_path('image/exit.png'))
        self.exit_size = list(self.exit_img.get_size())
        self.exit_pos = [(SCREEN_WIDTH - self.exit_size[0]) / 2, 573]
        self.exit_onclick = False

        self.settings_img = pygame.image.load(resource_path('image/settings.png'))
        self.settings_size = list(self.settings_img.get_size())
        self.settings_pos = [1086, 688]
        self.settings_onclick = False


element = Element()


def draw():
    screen.blit(element.bg, element.bg_pos)
    screen.blit(element.title_img, element.title_pos)
    screen.blit(element.start_img, element.start_pos)
    screen.blit(element.exit_img,  element.exit_pos)
    screen.blit(element.settings_img, element.settings_pos)


draw()

def handle_events():
    global element, VOLUME
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            button("down", x, y, element, draw)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = pygame.mouse.get_pos()
            button("up", x, y, element, draw)
        elif event.type == pygame.KEYDOWN:
            if (VOLUME < 1 or event.key == pygame.K_F1) and (VOLUME > 0 or event.key == pygame.K_F2):
                if (event.key == pygame.K_F1) ^ (event.key == pygame.K_F2):
                    VOLUME += 0.05 if event.key == pygame.K_F2 else -0.05
                    pygame.mixer.music.set_volume(VOLUME)


### game section ###
class GameVar(object):
    def __init__(self):
        # 无敌模式 True:开 False:关
        self.immortal = 1
        self.game_over = False
        self.quit = False

        self.flash = False
        self.flash_time = 0
        self.moving = False
        self.moving_time = 0
        self.interval = 20
        self.time = 0
        self.map = "map1"
        try:
            with open(resource_path(f"maps/{self.map}/position"), 'r', encoding="utf-8"):
                pass
        except FileNotFoundError as error:
            print(error)
            easygui.msgbox("invalid level")
            pygame.quit()
            sys.exit()


class GameElement(Element):
    def __init__(self):
        Element.__init__(self)

        self.title_pos = [21, 26]

        self.start_pos = [52, 492]
        self.start_onclick = False

        self.exit_pos = [52, 590]
        self.exit_onclick = False

        self.settings_pos = [52, 695]
        self.settings_onclick = False

        self.popup1_img = pygame.image.load(resource_path("image/game_over_popup1.png"))
        self.popup2_img = pygame.image.load(resource_path("image/game_over_popup2.png"))
        self.popup1_size = self.popup2_size = list(self.popup1_img.get_size())
        self.popup1_pos = self.popup2_pos = [(SCREEN_WIDTH - self.popup1_size[0]) / 2, 273]

        self.game_over_popup_retry_img = pygame.image.load(resource_path("image/try again.png"))
        self.game_over_popup_retry_size = list(self.game_over_popup_retry_img.get_size())
        self.game_over_popup_retry_pos = [490, 423]
        self.game_over_popup_retry_onclick = False

        self.game_over_popup_exit_img = pygame.image.load(resource_path("image/game_over_exit.png"))
        self.game_over_popup_exit_size = list(self.game_over_popup_exit_img.get_size())
        self.game_over_popup_exit_pos = [643, 423]
        self.game_over_popup_exit_onclick = False


class Diamond(object):
    def __init__(self):
        self.x = 391
        self.y = 670
        self.width = 60
        self.height = 55
        self.img = pygame.image.load(resource_path("image/diamond.png"))


class Coin(object):
    def __init__(self):
        self.x = [1081, 405, 630, 478, 1081]
        self.y = [84, 230, 381, 683, 683]
        self.total = len(self.x)
        self.img = pygame.image.load(resource_path("image/coin.png"))
        self.width, self.height = self.img.get_size()


class Beetle(object):
    def __init__(self):
        self.upgrade_coin = 3
        with open(resource_path(f"maps/{game_var.map}/position")) as f:
            self.x, self.y = eval(f.readline().split("/n")[0])
        self.speed = 5
        self.rotated_img = self.img = pygame.image.load(resource_path("image/sbeetle.png"))
        self.rotated_img_left = self.img_left = pygame.image.load(resource_path("image/sbeetle1.png"))
        self.rotated_img_right = self.img_right = pygame.image.load(resource_path("image/sbeetle2.png"))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.direction = 0
        self.rect = self.rotated_img.get_rect()

    def upgrade(self, direction: int):
        self.img = pygame.image.load(resource_path("image/beetle.png"))
        self.img_left = pygame.image.load(resource_path("image/beetle1.png"))
        self.img_right = pygame.image.load(resource_path("image/beetle2.png"))
        self.rotated_img = pygame.transform.rotate(self.img, self.direction)
        self.rotated_img_left = pygame.transform.rotate(self.img_left, self.direction)
        self.rotated_img_right = pygame.transform.rotate(self.img_right, self.direction)
        self.to_nearist_block(direction)
        game_draw()

    def to_nearist_block(self, direction: int):
        if direction % 2 == 0:
            x_int = 75.6
            self.x = 395 + round((self.x - 395) / x_int) * x_int
        else:
            y_int = 75.67
            self.y = 72 + round((self.y - 72) / y_int) * y_int


class Wall(object):
    def __init__(self):
        self.walls = []
        with open(resource_path(f"maps/{game_var.map}/walls")) as f:
            self.walls = eval(f.read())


def game_draw():
    global beetle, diamond, game_var, coin
    screen.fill(SCREEN_BG_COLOR)
    pygame.draw.rect(screen, (220, 208, 170), (379, 56, 763, 688))
    screen.blit(pygame.image.load(resource_path("image/walls.png")), (379, 56))
    screen.blit(game_element.title_img, game_element.title_pos)
    screen.blit(game_element.start_img, game_element.start_pos)
    screen.blit(game_element.exit_img, game_element.exit_pos)
    screen.blit(game_element.settings_img, game_element.settings_pos)
    screen.blit(diamond.img, (diamond.x, diamond.y))
    for i in range(len(coin.x)):
        screen.blit(coin.img, (coin.x[i], coin.y[i]))
    draw_text(screen, "volume: " + 'I' * round(VOLUME * 20), 30, (255, 255, 255), (55, 450))
    if game_var.flash:
        if game_var.flash_time > 600:
            game_var.flash = False
            game_var.flash_time = 0
        elif game_var.flash_time % 200 >= 100:
            return
    if game_var.moving:
        if game_var.moving_time % 150 < 75:
            screen.blit(beetle.rotated_img_left, (beetle.x, beetle.y))
        else:
            screen.blit(beetle.rotated_img_right, (beetle.x, beetle.y))
    else:
        screen.blit(beetle.rotated_img, (beetle.x, beetle.y))


def check_hit(direction: int):
    global beetle, diamond, game_var, coin
    if diamond.x - beetle.width <= beetle.x <= diamond.x + diamond.width and \
            diamond.y + diamond.height >= beetle.y >= diamond.y - beetle.height:
        game_var.game_over = True
        pygame.mixer.music.stop()
        sound = pygame.mixer.Sound(resource_path("audio/victory.mp3"))
        sound.set_volume(VOLUME)
        pygame.mixer.Sound.play(sound)
        game_over_popup(1)
        return
    for i in range(len(coin.x)):
        if coin.x[i] - beetle.width <= beetle.x <= coin.x[i] + coin.width and \
                coin.y[i] + coin.height >= beetle.y >= coin.y[i] - beetle.height:
            coin.x.pop(i)
            coin.y.pop(i)
            if len(coin.x) == coin.total - beetle.upgrade_coin:
                beetle.upgrade(direction)
                sound = pygame.mixer.Sound(resource_path("audio/upgrade.mp3"))
                sound.set_volume(VOLUME)
                pygame.mixer.Sound.play(sound)
                game_var.flash = True
            else:
                sound = pygame.mixer.Sound(resource_path("audio/coin.mp3"))
                sound.set_volume(VOLUME)
                pygame.mixer.Sound.play(sound)
            break
    if game_var.immortal:
        return
    for w in wall.walls:
        if w[1][1] >= beetle.y >= w[0][1] - beetle.height and w[1][0] >= beetle.x >= w[0][0] - beetle.width:
            game_var.game_over = True
            pygame.mixer.music.stop()
            sound = pygame.mixer.Sound(resource_path("audio/fail.mp3"))
            sound.set_volume(VOLUME)
            pygame.mixer.Sound.play(sound)
            game_over_popup(2)
            return


def game_over_popup(mode: int):
    global beetle, diamond, game_var, coin, game_element
    screen.blit(game_element.__getattribute__(f"popup{mode}_img"), game_element.__getattribute__(f"popup{mode}_pos"))
    screen.blit(game_element.game_over_popup_retry_img, game_element.game_over_popup_retry_pos)
    screen.blit(game_element.game_over_popup_exit_img, game_element.game_over_popup_exit_pos)
    pygame.display.update()
    while True:
        flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_var.quit = True
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                if game_element.game_over_popup_retry_pos[0] <= x <=game_element.game_over_popup_retry_pos[0]\
                        + game_element.game_over_popup_retry_size[0] and game_element.game_over_popup_retry_pos[1]\
                        <= y <= game_element.game_over_popup_retry_pos[1] + game_element.game_over_popup_retry_size[1]:
                    game_element.game_over_popup_retry_size[0] -= 7
                    game_element.game_over_popup_retry_size[1] -= 2
                    game_element.game_over_popup_retry_pos[0] += 3.5
                    game_element.game_over_popup_retry_pos[1] += 1
                    game_element.game_over_popup_retry_img = pygame.transform.scale(
                        game_element.game_over_popup_retry_img, game_element.game_over_popup_retry_size)
                    game_element.game_over_popup_retry_onclick = True
                    flag = True
                    break
                elif game_element.game_over_popup_exit_pos[0] <= x <= game_element.game_over_popup_exit_pos[0]\
                        + game_element.game_over_popup_exit_size[0] and game_element.game_over_popup_exit_pos[1]\
                        <= y <= game_element.game_over_popup_exit_pos[1] + game_element.game_over_popup_exit_size[1]:
                    game_element.game_over_popup_exit_size[0] -= 4
                    game_element.game_over_popup_exit_size[1] -= 2
                    game_element.game_over_popup_exit_pos[0] += 2
                    game_element.game_over_popup_exit_pos[1] += 1
                    game_element.game_over_popup_exit_img = pygame.transform.scale(game_element.game_over_popup_exit_img, game_element.game_over_popup_exit_size)
                    game_element.game_over_popup_retry_onclick = True
                    game_element.game_over_popup_exit_onclick = True
                    flag = True
                    break
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                x, y = pygame.mouse.get_pos()
                if game_var.game_over and game_element.game_over_popup_retry_pos[0] <= x <= \
                        game_element.game_over_popup_retry_pos[0] + game_element.game_over_popup_retry_size[0] and \
                        game_element.game_over_popup_retry_pos[1] <= y <= game_element.game_over_popup_retry_pos[1] \
                        + game_element.game_over_popup_retry_size[1] and game_element.game_over_popup_retry_onclick:
                    pygame.mixer.music.play(-1)
                    reset_game()
                    return
                elif game_var.game_over and game_element.game_over_popup_exit_pos[0] <= x <= \
                        game_element.game_over_popup_exit_pos[0] + game_element.game_over_popup_exit_size[0] and \
                        game_element.game_over_popup_exit_pos[1] <= y <= game_element.game_over_popup_exit_pos[1] + \
                        game_element.game_over_popup_exit_size[1] and game_element.game_over_popup_exit_onclick:
                    pygame.mixer.music.play(-1)
                    game_var.quit = True
                    return
                game_element.__init__()
                flag = True
        if flag:
            game_draw()
            screen.blit(game_element.__getattribute__(f"popup{mode}_img"), game_element.__getattribute__(f"popup{mode}_pos"))
            screen.blit(game_element.game_over_popup_retry_img, game_element.game_over_popup_retry_pos)
            screen.blit(game_element.game_over_popup_exit_img, game_element.game_over_popup_exit_pos)
            pygame.display.update()



def reset_game():
    global beetle, diamond, game_var, coin
    # 重置游戏变量
    game_var = GameVar()
    beetle = Beetle()
    diamond = Diamond()
    coin = Coin()
    game_element.__init__()
    game_draw()
    game_var.game_over = False


def control() -> tuple[bool, float | None]:
    global beetle, game_var, game_element, coin, VOLUME
    if game_var.flash: return False, None
    keys = pygame.key.get_pressed()
    direction = beetle.direction
    flag = False
    dx = dy = 0
    if keys[pygame.K_RIGHT]:
        dx += beetle.speed
        flag = True
    if keys[pygame.K_LEFT]:
        dx -= beetle.speed
        flag = True
    if keys[pygame.K_DOWN]:
        dy += beetle.speed
        flag = True
    if keys[pygame.K_UP]:
        dy -= beetle.speed
        flag = True
    if dx > 0:
        direction = 270
    elif dx < 0:
        direction = 90
    if dy > 0:
        direction = 180
    elif dy < 0:
        direction = 0
    if direction != beetle.direction:
        beetle.direction = direction
        beetle.rotated_img = pygame.transform.rotate(beetle.img, beetle.direction)
        beetle.rotated_img_left = pygame.transform.rotate(beetle.img_left, beetle.direction)
        beetle.rotated_img_right = pygame.transform.rotate(beetle.img_right, beetle.direction)
        beetle.width = beetle.rotated_img.get_width()
        beetle.height = beetle.rotated_img.get_height()
        beetle.rect = beetle.rotated_img.get_rect()
    beetle.x += dx
    beetle.y += dy
    # direction: 0-UP 90-LEFT 180-DOWN 270-RIGHT
    return flag, direction/90 if flag else None


def game_handle_events():
    global beetle, game_var, game_element, coin, VOLUME
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_var.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            button("down", x, y, game_element, game_draw)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = pygame.mouse.get_pos()
            button("up", x, y, game_element, game_draw)
        elif event.type == pygame.KEYDOWN:
            if (VOLUME < 1 or event.key == pygame.K_F1) and (VOLUME > 0 or event.key == pygame.K_F2):
                if (event.key == pygame.K_F1) ^ (event.key == pygame.K_F2):
                    VOLUME += 0.05 if event.key == pygame.K_F2 else -0.05
                    pygame.mixer.music.set_volume(VOLUME)
                    game_draw()
    movement = control()
    if movement[0]:
        game_var.moving = True
        if beetle.y < 0:
            beetle.y = 0
        elif beetle.y + beetle.height > SCREEN_HEIGHT:
            beetle.y = SCREEN_HEIGHT - beetle.height
        if beetle.x < 0:
            beetle.x = 0
        elif beetle.x + beetle.width > SCREEN_WIDTH:
            beetle.x = SCREEN_WIDTH - beetle.width
        game_draw()
        check_hit(movement[1])
    elif game_var.moving:
        game_var.moving = False
        game_var.moving_time = 0
        game_draw()
    elif game_var.flash:
        game_draw()


def game():
    global beetle, diamond, game_var, game_element, coin
    reset_game()
    while True:
        game_handle_events()
        if game_var.quit:
            game_var.quit = False
            return
        pygame.display.update()
        pygame.time.delay(game_var.interval)
        game_var.time += game_var.interval
        if game_var.moving:
            game_var.moving_time += game_var.interval
        if game_var.flash:
            game_var.flash_time += game_var.interval


game_var = GameVar()
game_element = GameElement()
diamond = Diamond()
coin = Coin()
beetle = Beetle()
wall = Wall()

### main section ###
pygame.mixer.music.load(resource_path("audio/bgm.mp3"))
pygame.mixer.music.set_volume(VOLUME)
pygame.mixer.music.play(-1)
while True:
    handle_events()
    pygame.display.update()
