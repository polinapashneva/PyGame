import os
import sys
import textwrap
import pygame
import sqlite3


FPS = 50
with open('data/данные.txt', 'r') as dan: # считывает данные игрока из файла
    dan = dan.readline().split(' ')
    MONEY = int(dan[-1])
    LEVEL = int(dan[0])
KH = 0
Z = 0
XC = 0
CORP = []
DD = 0


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(): # Создаем стартовую заставку, которую можно закрыть нажатием мыши
    fon = pygame.transform.scale(load_image('заставочка.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def notll(): # выводим на экран сообщение о том, что уровня еще нет
    pygame.draw.rect(screen, (50, 50, 50), (WIDTH // 3, HEIGHT // 3, WIDTH // 3, HEIGHT // 3))
    fon = pygame.font.SysFont(None, 50)
    slov = textwrap.wrap("Ой-ой... Кажется этот уровень в процессе изготовления...",
                         (WIDTH // 3) // 50 * 2.5, break_long_words=False)
    for i in slov:
        string_rendered = fon.render(i,1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.y = HEIGHT // 3 + 20 + slov.index(i) * 50
        intro_rect.x = WIDTH // 3 + 20
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)

def zast(): # Создаем Меню
    global DD
    fon = pygame.transform.scale(load_image('заставка.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    intro_text = ['ИГРАТЬ', str(MONEY), "ВЫХОД"] # Список кнопок
    text_coord = 50
    coordkn = []
    for line in intro_text:
        # Отрисовываем каждую кнопку. Кнопка "Монеты" будет с символом перед текстом, поэтому отрисуем ее отдельно
        if line != str(MONEY):
            text_coord += 10
            pygame.draw.rect(screen, (120, 132, 73), (60, text_coord, WIDTH // 5, 60))
            coordkn.append([60, text_coord, text_coord + 60])
            font = pygame.font.SysFont(None, 50)
            string_rendered = font.render(line, 1, pygame.Color('black'))
            text_coord += 12
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            text_coord = text_coord - 12 + 80
            intro_rect.x = 70
            screen.blit(string_rendered, intro_rect)
        else:
            text_coord += 10
            pygame.draw.rect(screen, (120, 132, 73), (60, text_coord, WIDTH // 5, 60))
            coordkn.append([120, text_coord, text_coord + 60])
            image = pygame.transform.scale(load_image('символ.png'), (58, 58))
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (61, text_coord + 1))
            font = pygame.font.SysFont(None, 50)
            string_rendered = font.render(line, 1, pygame.Color('black'))
            text_coord += 12
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            text_coord = text_coord - 12 + 80
            intro_rect.x = 130
            screen.blit(string_rendered, intro_rect)

    c = [[]]
    while True:
        if 60 <= pygame.mouse.get_pos()[0] <= 60 + WIDTH // 5: # Если навести мышь на кнопку, цвет текста изменится
            for i in coordkn:
                if i[1] <= pygame.mouse.get_pos()[1] <= i[2]:
                    c.append(i[::])
                    font = pygame.font.SysFont(None, 50)
                    string_rendered = font.render(intro_text[coordkn.index(i)], 1, pygame.Color('white'))
                    text_coord = i[1] + 12
                    intro_rect = string_rendered.get_rect()
                    intro_rect.top = text_coord
                    intro_rect.x = i[0] + 10
                    screen.blit(string_rendered, intro_rect)
                    if i[0] != 60:
                        image = pygame.transform.scale(load_image('символ2.png'), (58, 58))
                        image.set_colorkey((0, 0, 0))
                        screen.blit(image, (61, i[1] + 1))
                else:
                    font = pygame.font.SysFont(None, 50)
                    string_rendered = font.render(intro_text[coordkn.index(i)], 1, pygame.Color('black'))
                    text_coord = i[1] + 12
                    intro_rect = string_rendered.get_rect()
                    intro_rect.top = text_coord
                    intro_rect.x = i[0] + 10
                    screen.blit(string_rendered, intro_rect)
                    if i[0] != 60:
                        image = pygame.transform.scale(load_image('символ.png'), (58, 58))
                        image.set_colorkey((255, 255, 255))
                        screen.blit(image, (61, i[1] + 1))
        else:
            if c[-1] != []: # Красим кнопки обратно в черный, когда мышка сдвигается
                font = pygame.font.SysFont(None, 50)
                string_rendered = font.render(intro_text[coordkn.index(c[-1])], 1, pygame.Color('black'))
                text_coord = c[-1][1] + 12
                intro_rect = string_rendered.get_rect()
                intro_rect.top = text_coord
                intro_rect.x = c[-1][0] + 10
                screen.blit(string_rendered, intro_rect)
                if c[-1][0] != 60:
                    image = pygame.transform.scale(load_image('символ.png'), (58, 58))
                    image.set_colorkey((255, 255, 255))
                    screen.blit(image, (61, c[-1][1] + 1))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 60 <= event.pos[0] <= 60 + WIDTH // 5:
                    for i in coordkn:
                        if i[1] <= event.pos[1] <= i[2]:
                            if intro_text[coordkn.index(c[-1])] == "ВЫХОД":
                                DD = 1
                                return
                            elif intro_text[coordkn.index(c[-1])] == str(MONEY):
                                DD = 2
                                return
                            elif intro_text[coordkn.index(c[-1])] == 'ИГРАТЬ':
                                DD = 3
                                return
        pygame.display.flip()
        clock.tick(FPS)


def promo():
    # Рисуем окошко для ввода промокода
    global MONEY
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100))
    font = pygame.font.SysFont(None, 40)
    string_rendered = font.render("Введите промокод", 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = HEIGHT // 2 - 290
    intro_rect.x = WIDTH // 2 - 140
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 140, HEIGHT // 2, 280, 40))
    pc = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: # Заканчиваем ввод промокода
                try:
                    bd = sqlite3.connect("data/промокод.sqlite")
                    cur = bd.cursor()
                    result = cur.execute(f"""SELECT * FROM код WHERE Код = {pc}""").fetchone()
                    if result[-1] == '0':
                        MONEY += int(result[1])
                        with open('data/данные.txt', 'w') as dan:
                            dan.write(f'{LEVEL} {MONEY}')
                        cur.execute(f'''UPDATE код SET применения = 1 WHERE Код = {pc}''')
                        bd.commit()
                    bd.close()
                    return
                except:
                    pass
            elif event.type == pygame.KEYDOWN: # Показываем ввод с клавиатуры в нашем окне
                pc = pc + str(event.unicode)
                font = pygame.font.SysFont(None, 30)
                string_rendered = font.render(pc, 1, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = HEIGHT // 2 + 5
                intro_rect.x = WIDTH // 2 - 135
                screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)


class Stolb(pygame.sprite.Sprite): # создаем столбы
    def __init__(self, pos, b, r):
        super().__init__(tiles_group, all_sprites)
        mr = {'m': 2,
              's': 4,
              'b': 6}
        self.image = pygame.transform.scale(load_image('б-столб.png'), (30, b * mr[r]))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect().move(pos[0], pos[1])


class Tile(pygame.sprite.Sprite): # создаем платформы
    def __init__(self, pos, a):
        super().__init__(tiles_group, plat_group, all_sprites)
        self.image = pygame.transform.scale(load_image('платформа.png'), (a, 29))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect().move(pos[0], pos[1])


class Coins(pygame.sprite.Sprite): # создаем монеты
    def __init__(self, x, y):
        super().__init__(money_group, all_sprites)
        self.image = pygame.transform.scale(load_image('монета.png'), (KH - 30, KH - 30))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect().move(x, y)


class Zem(pygame.sprite.Sprite): # создаем спрайт земли
    def __init__(self):
        super().__init__(tiles_group, zem_group, plat_group, all_sprites)
        self.image = pygame.Surface([WIDTH * 3, 1])
        self.rect = pygame.Rect(1, HEIGHT - (KH // 3 + KH // 12), WIDTH * 3, 1)


class Player(pygame.sprite.Sprite): # создаем стоящего игрока
    def __init__(self, w, h):
        super().__init__(char_group, all_sprites)
        self.image = pygame.transform.scale(load_image('челик стоит.png'), (w - 55, h - 40))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect().move(70, HEIGHT - h + 50 - Z)


class Prun(pygame.sprite.Sprite): # создаем бегущего игрока в одну сторону
    def __init__(self, w, h):
        super().__init__(charrun_group, all_sprites)
        self.image = pygame.transform.scale(load_image('челик бежит.png'), (w - 55, h - 40))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect().move(70, HEIGHT - h + 50 - Z)


class Prunl(pygame.sprite.Sprite): # создаем игрока бегущего в другую сторону
    def __init__(self, w, h):
        super().__init__(charrunl_group, all_sprites)
        self.image = pygame.transform.scale(load_image('челик бежит-2.png'), (w - 55, h - 40))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect().move(70, HEIGHT - h + 50 - Z)


class Fon(pygame.sprite.Sprite): # создаем спрайт фона
    def __init__(self, h):
        super().__init__(fon_group, all_sprites)
        self.image = pygame.transform.scale(load_image(f'{LEVEL}.png'), (h, HEIGHT))
        self.rect = self.image.get_rect().move(0, 0)
        pygame.display.flip()
        clock.tick(FPS)


class Man(pygame.sprite.Sprite): # создаем спрайт npc для первого уровня
    def __init__(self, x, h):
        super().__init__(man_group, all_sprites)
        self.image = pygame.transform.scale(load_image('Джей.png'), (x - 70, h - 60))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect().move(WIDTH * 3 - WIDTH // 2, HEIGHT - Z - h + 80)


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
char_group = pygame.sprite.Group()
charrun_group = pygame.sprite.Group()
fon_group = pygame.sprite.Group()
plat_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()
zem_group = pygame.sprite.Group()
charrunl_group = pygame.sprite.Group()
man_group = pygame.sprite.Group()


def generate_level_1(): # создаем карту уровня
    global KH, Z, XC
    new_player = None
    if WIDTH <= 5356:
        m = round(5356 / WIDTH / 3)
        z = round(75 / m)
    else:
        m = WIDTH / 5356 / 3
        z = round(75 * m)
    Z = z
    kh = round((HEIGHT - z) / 7) + 20
    KH = kh
    xc = round(WIDTH / 10)
    XC = xc
    crd = [(xc, kh * 5), (xc * 2, kh * 4), (xc * 3, kh * 3), (xc * 5, kh * 3), (xc * 6, kh * 2), (xc * 7, kh),
           (xc * 7, kh * 5), (xc * 8, kh * 4), (xc * 9, kh * 3), (xc * 10, kh * 2), (xc * 10, kh * 5),
           (xc * 11, kh * 4), (xc * 13, kh * 3), (xc * 16, kh * 5), (xc * 16, kh * 3),
           (xc * 16, kh), (xc * 17, kh * 4), (xc * 17, kh * 2), (xc * 18, kh), (xc * 19, kh * 2),
           (xc * 19, kh * 4), (xc * 20 + 30, kh * 3), (xc * 20 + 30, kh * 5), (xc * 21, kh * 4)]
    for i in crd:
        Tile(i, xc)
    crd = [(xc * 4 - 25, kh * 3 + 15, 's'), (xc * 5 + 10, kh * 3 + 15, 's'), (xc * 11 - 15, 0 + 15, 'm'),
           (xc * 12 - 25, kh * 4 + 15, 's'), (xc * 13, kh * 3 + 15, 's'), (xc * 19 - 25, kh + 15, 'b'),
           (xc * 21, kh * 3, 's'), ]
    for i in crd:
        Stolb(i[0:-1], kh, i[-1])
    crd = [(XC * 5 + 45, KH * 5 + 30), (XC * 10 + 15, KH + 15), (XC * 19 + 15, KH * 5 + 30)]
    for i in crd:
        Coins(i[0], i[1])
    new_player = Player(xc, kh)
    runp = Prun(xc, kh)
    runpl = Prunl(xc, kh)
    Man(xc, kh)
    Fon(WIDTH * 3)
    Zem()
    # вернем игрока, а также размер поля в клетках
    return new_player, runp, runpl, WIDTH, HEIGHT


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = - WIDTH // 2
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)

    def sb(self, s):
        self.dx = - WIDTH // 2 - s


def up(): # возвращает координаты платформы с которой столкнулся спрайт игрока
    if pygame.sprite.spritecollideany(player, plat_group):
        return pygame.sprite.spritecollideany(player, plat_group).rect.y


def mcoin(): # уничтожает спрайт созданной монетки
    if pygame.sprite.spritecollideany(player, money_group):
        pygame.sprite.spritecollideany(player, money_group).kill()


try:
    pygame.init()
    pygame.display.set_caption('')
    infoObject = pygame.display.Info()
    size = width, height = WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 50
    player_image = load_image('челик стоит.png', -1)
    tile_width = tile_height = 50

    start_screen()
    while True: # связываем меню и выбранные кнопки
        zast()
        if DD == 1:
            terminate()
        elif DD == 2:
            promo()
        elif DD == 3:
            break
    while True:
        if LEVEL == 1: # если игроку нужно пройти уровень 1...
            *char, level_x, level_y = generate_level_1()
            camera = Camera()
            running = True

            p = 0
            s = 0
            r = False
            lor = 1
            mp = 0
            cor = [70, HEIGHT - KH + 50 - Z]
            while running: # запускаем платформер
                player = char[0]
                lor = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]: # зажата кнопка "влево"
                    player = char[2]
                    lor = 2
                    player.rect.x -= 7
                    s -= 7
                    if pygame.sprite.spritecollideany(player, tiles_group):
                        player.rect.x += 7
                        s += 7
                elif keys[pygame.K_RIGHT]: # зажата кнопка "вправо"
                    player = char[1]
                    lor = 1
                    player.rect.x += 7
                    s += 7
                    if pygame.sprite.spritecollideany(player, tiles_group):
                        player.rect.x -= 7
                        s -= 7
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP: # нажата кнопка "вверх", отвечающая за прыжок
                            player = char[1]
                            t = KH // 9 * 2 + 5
                            if t % 2 != 0:
                                t += 1
                            r = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if 60 <= event.pos[0] <= 120 and 60 <= event.pos[1] <= 120:
                            # если игрок мышкой нажал на кнопку в левом верхнем углу экрана перезапускаем уровень
                            player.rect.x = 70
                            camera.update(player)
                            mp = 0
                            s = 0
                            for i in all_sprites:
                                i.kill()
                            *char, level_x, level_y = generate_level_1()
                            Camera()
                if r:
                    player = char[lor]
                    p += 1
                    if p <= t // 2: # если игрок должен пойти на снижение после прыжка
                        player.rect.y -= 9
                        if pygame.sprite.spritecollideany(player, tiles_group):
                            player.rect.y += 9
                    else:
                        player.rect.y += 9
                        if pygame.sprite.spritecollideany(player, tiles_group):
                            player.rect.y -= 9
                    if p == t:
                        p = 0
                        r = False
                if not pygame.sprite.spritecollideany(player, plat_group) and not r:
                    player.rect.y += 9
                    try:
                        if player.rect.y + player.rect.h > int(up()): # проверка на провал в текстуры платформ
                            player.rect.y -= 9
                    except Exception as ex:
                        pass
                if pygame.sprite.spritecollideany(player, money_group): # если игрок собрал монетку
                    mp += 1
                    mcoin()

                if pygame.sprite.spritecollideany(player, man_group): # если игрок дошел до npc
                    running = False

                cor = [player.rect.x, player.rect.y]
                for i in range(3):
                    char[i].rect.x, char[i].rect.y = cor[0], cor[1] # перемещаем все картинки с игроком


                # изменяем ракурс камеры
                if s + XC - player.rect.w // 2 - WIDTH // 2 > 0 and s + WIDTH // 2 + player.rect.w // 2 < WIDTH * 3 - 70:
                    camera.update(player)
                    # обновляем положение всех спрайтов
                    for sprite in all_sprites:
                        camera.apply(sprite)

                screen.fill((0, 0, 0))
                fon_group.draw(screen)
                tiles_group.draw(screen)
                money_group.draw(screen)
                man_group.draw(screen)
                if player == char[0]: # показываем только одну картинку с игроком
                    char_group.draw(screen)
                elif player == char[1]:
                    charrun_group.draw(screen)
                else:
                    charrunl_group.draw(screen)

                if 60 <= pygame.mouse.get_pos()[0] <= 120 and 60 <= pygame.mouse.get_pos()[1] <= 120:
                    # проверяем наведение на экран
                    image = pygame.transform.scale(load_image('назад-2.png'), (60, 60))
                    image.set_colorkey((255, 255, 255))
                    screen.blit(image, (60, 60))
                else:
                    image = pygame.transform.scale(load_image('назад-1.png'), (60, 60))
                    image.set_colorkey((255, 255, 255))
                    screen.blit(image, (60, 60))

                pygame.display.flip()
                clock.tick(fps)
            running = True
            rep = [(0, "Джей", "*Бубнит какую-то тарабарщину*"), (0, "Пасси", "~Что это с ним?~"),
                   (0, "Пасси", "Что мне делать?", "Окликнуть", "Пройти мимо"), (1, "Пасси", "Папа? Ты в порядке?"),
                   (1, "Джей", "*Вздрогнул*"), (1, "Джей", "Да, Пасси, не беспокойся. Ступай, я догоню."),
                   (2, "Пасси", "*Пожала плечами*"), (0, "Пасси", "*Посмотрела на каменную пирамиду, поросшую мхом*"),
                   (0, "Пасси", "*Вздохнув, стала взбираться по высоким ступеням*")] # список реплик
            vb = 0
            p = [0]
            while running:
                for event in pygame.event.get():
                    if len(rep[0]) == 3: # если не надо будет делать выбор
                        fon_group.draw(screen)
                        tiles_group.draw(screen)
                        if rep[0][0] in p:
                            if rep[0][1] == "Джей": # если говорит не игрок
                                pers = pygame.transform.scale(load_image('Джей1-2.png'), (WIDTH // 4, HEIGHT // 8 * 6))
                                pers.set_colorkey((255, 255, 255))
                                screen.blit(pers, (WIDTH // 3 * 2, HEIGHT // 8 * 2))

                                pygame.draw.rect(screen, (100, 100, 100), (60, HEIGHT // 3 * 2,
                                                                           WIDTH // 5 * 3, HEIGHT // 3 - 60))
                                font = pygame.font.SysFont(None, 50)
                                string_rendered = font.render(rep[0][-1], 1, pygame.Color('white'))
                                intro_rect = string_rendered.get_rect()
                                intro_rect.x = 70
                                intro_rect.y = HEIGHT // 3 * 2 + 10
                                intro_rect.w = WIDTH // 5 * 3 - 20
                                intro_rect.h = HEIGHT // 3 - 80
                                screen.blit(string_rendered, intro_rect)
                            elif rep[0][1] == 'Пасси': # если игрок
                                pers = pygame.transform.scale(load_image('Пасс1-2.png'), (WIDTH // 4, HEIGHT // 8 * 6))
                                pers.set_colorkey((255, 255, 255))
                                screen.blit(pers, (60, HEIGHT // 8 * 2))
                                pygame.draw.rect(screen, (100, 100, 100), (WIDTH // 4 + 80, HEIGHT // 3 * 2,
                                                                           WIDTH // 5 * 3, HEIGHT // 3 - 60))
                                font = pygame.font.SysFont(None, 50)
                                slov = textwrap.wrap(rep[0][2], (WIDTH // 5 * 3 - 20) * 2.5 // 50, break_long_words=False)
                                for i in range(len(slov)):
                                    string_rendered = font.render(slov[i], 1, pygame.Color('white'))
                                    intro_rect = string_rendered.get_rect()
                                    intro_rect.x = WIDTH // 4 + 80 + 10
                                    intro_rect.y = HEIGHT // 3 * 2 + 10 + 50 * i
                                    intro_rect.w = WIDTH // 5 * 3 - 20
                                    intro_rect.h = HEIGHT // 3 - 80
                                    screen.blit(string_rendered, intro_rect)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            del rep[0]
                    elif len(rep[0]) > 3: # если будет выбор
                        fon_group.draw(screen)
                        tiles_group.draw(screen)
                        pers = pygame.transform.scale(load_image('Пасс1-2.png'), (WIDTH // 4, HEIGHT // 8 * 6))
                        pers.set_colorkey((255, 255, 255))
                        screen.blit(pers, (60, HEIGHT // 8 * 2))
                        pygame.draw.rect(screen, (100, 100, 100), (WIDTH // 4 + 80, HEIGHT // 3 * 2,
                                                                   WIDTH // 5 * 3, HEIGHT // 9 - 30))
                        font = pygame.font.SysFont(None, 50)
                        string_rendered = font.render(rep[0][2], 1, pygame.Color('white'))
                        intro_rect = string_rendered.get_rect()
                        intro_rect.x = WIDTH // 4 + 80 + 10
                        intro_rect.y = HEIGHT // 3 * 2 + 10
                        intro_rect.w = WIDTH // 5 * 3 - 20
                        intro_rect.h = HEIGHT // 9 - 50

                        screen.blit(string_rendered, intro_rect)

                        # настраиваем цвет кнопок в зависимости от наведения
                        if (WIDTH // 4 + 80 < pygame.mouse.get_pos()[0] < WIDTH // 4 + 80 + WIDTH // 5 * 3 and
                                HEIGHT // 3 * 2 + HEIGHT // 9 - 20 < pygame.mouse.get_pos()[1]
                                < HEIGHT // 3 * 2 + HEIGHT // 9 * 2 - 30):
                            screen.blit(pers, (60, HEIGHT // 8 * 2))
                            pygame.draw.rect(screen, (100, 112, 53), (WIDTH // 4 + 80,
                                                                      HEIGHT // 3 * 2 + HEIGHT // 9 - 20, WIDTH // 5 * 3,
                                                                      HEIGHT // 9 - 30))
                        else:
                            screen.blit(pers, (60, HEIGHT // 8 * 2))
                            pygame.draw.rect(screen, (100, 100, 100), (WIDTH // 4 + 80,
                                                                       HEIGHT // 3 * 2 + HEIGHT // 9 - 20,
                                                                       WIDTH // 5 * 3, HEIGHT // 9 - 30))
                        font = pygame.font.SysFont(None, 50)
                        string_rendered = font.render(rep[0][3], 1, pygame.Color('white'))
                        intro_rect = string_rendered.get_rect()
                        intro_rect.x = WIDTH // 4 + 80 + 10
                        intro_rect.y = HEIGHT // 3 * 2 + HEIGHT // 9 - 20 + 10
                        intro_rect.w = WIDTH // 5 * 3 - 20
                        intro_rect.h = HEIGHT // 9 - 30

                        screen.blit(string_rendered, intro_rect)

                        if (WIDTH // 4 + 80 < pygame.mouse.get_pos()[0] < WIDTH // 4 + 80 + WIDTH // 5 * 3 and
                                HEIGHT // 3 * 2 + HEIGHT // 9 * 2 - 40 < pygame.mouse.get_pos()[1]
                                < HEIGHT // 3 * 2 + HEIGHT // 9 * 2 - 40 + HEIGHT // 9 - 30):
                            screen.blit(pers, (60, HEIGHT // 8 * 2))
                            pygame.draw.rect(screen, (100, 112, 53), (WIDTH // 4 + 80,
                                                                      HEIGHT // 3 * 2 + HEIGHT // 9 * 2 - 40,
                                                                      WIDTH // 5 * 3, HEIGHT // 9 - 30))
                        else:
                            screen.blit(pers, (60, HEIGHT // 8 * 2))
                            pygame.draw.rect(screen, (100, 100, 100), (WIDTH // 4 + 80,
                                                                       HEIGHT // 3 * 2 + HEIGHT // 9 * 2 - 40,
                                                                       WIDTH // 5 * 3, HEIGHT // 9 - 30))
                        font = pygame.font.SysFont(None, 50)
                        string_rendered = font.render(rep[0][4], 1, pygame.Color('white'))
                        intro_rect = string_rendered.get_rect()
                        intro_rect.x = WIDTH // 4 + 80 + 10
                        intro_rect.y = HEIGHT // 3 * 2 + HEIGHT // 9 * 2 - 40 + 10
                        intro_rect.w = WIDTH // 5 * 3 - 20
                        intro_rect.h = HEIGHT // 9 - 30

                        screen.blit(string_rendered, intro_rect)

                        if (event.type == pygame.MOUSEBUTTONDOWN and
                                ((WIDTH // 4 + 80 < pygame.mouse.get_pos()[0] < WIDTH // 4 + 80 + WIDTH // 5 * 3 and
                                  HEIGHT // 3 * 2 + HEIGHT // 9 * 2 - 40 < pygame.mouse.get_pos()[1]
                                  < HEIGHT // 3 * 2 + HEIGHT // 9 * 2 - 40 + HEIGHT // 9 - 30) or
                                 (WIDTH // 4 + 80 < pygame.mouse.get_pos()[0] < WIDTH // 4 + 80 + WIDTH // 5 * 3 and
                                  HEIGHT // 3 * 2 + HEIGHT // 9 - 20 < pygame.mouse.get_pos()[1]
                                  < HEIGHT // 3 * 2 + HEIGHT // 9 * 2 - 30))):
                            del rep[0]
                            if (HEIGHT // 3 * 2 + HEIGHT // 9 - 20 < pygame.mouse.get_pos()[1]
                                    < HEIGHT // 3 * 2 + HEIGHT // 9 * 2 - 30):
                                p = [0, 1]
                            else:
                                p = [0, 2]

                    while True:
                        if len(rep) > 0:
                            if rep[0][0] in p:
                                break
                            else:
                                del rep[0]
                        else:
                            running = False
                            break

                    pygame.display.flip()
                    clock.tick(FPS)

            running = True

            while running:
                screen.fill((135, 168, 109))
                pygame.draw.rect(screen, (72, 99, 51), (WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2))
                font = pygame.font.SysFont(None, 100)
                string_rendered = font.render('Уровень пройден!', 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                intro_rect.x = WIDTH // 4 + 20
                intro_rect.y = HEIGHT // 4 + 20
                screen.blit(string_rendered, intro_rect)

                font = pygame.font.SysFont(None, 50)
                string_rendered = font.render(f'+ 5x{mp}', 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                intro_rect.x = WIDTH // 4 + 10
                intro_rect.y = HEIGHT // 4 + 120
                screen.blit(string_rendered, intro_rect)

                font = pygame.font.SysFont(None, 50)
                string_rendered = font.render(f'Итог: + {mp * 5}', 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                intro_rect.x = WIDTH // 4 + 10
                intro_rect.y = HEIGHT // 4 + 180
                screen.blit(string_rendered, intro_rect)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        running = False
                pygame.display.flip()
                clock.tick(FPS)

            MONEY = MONEY + mp * 5
            LEVEL = 2
            with open('data/данные.txt', 'w') as dan:
                dan.write(f'{LEVEL} {MONEY}')

            LEVEL += 1
        else:
            notll()
        zast()
        pygame.quit()
except:
    print('Error')
