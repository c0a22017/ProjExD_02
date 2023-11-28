import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1500, 900

delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #yoko
        yoko = False

    if rct.top < 0 or HEIGHT < rct.bottom: #tate
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img2 = pg.image.load("ex02/fig/6.png")
    kk_img2 = pg.transform.rotozoom(kk_img2, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20)) #pra1
    bb_img.set_colorkey((0, 0, 0)) #kuro
    pg.draw.circle(bb_img, (255, 0, 0), (10, 40), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5 #pra2
    kk_zis = { #dict
        (5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (5, -5): pg.transform.rotozoom(kk_img, 316, 1.0),
        (0, -5): pg.transform.rotozoom(kk_img, 270, 1.0),
        (-5, -5): pg.transform.rotozoom(kk_img, 315, 1.0),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (0, 5): pg.transform.rotozoom(kk_img, 90, 1.0),
        (5, 5): pg.transform.rotozoom(kk_img, 45, 1.0),
    }

    accs = [a for a in range(1, 11)]

    fonto = pg.font.Font(None, 80)
    moji = fonto.render("Damn It!!", True, (255, 255, 255))

    clock = pg.time.Clock()
    tmr = 0
    bb_size = 20 #bombsize
    bb_expand = True

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        if kk_rct.colliderect(bb_rct): #pra5
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img2, kk_rct)
            screen.blit(moji, [400, 400])
            pg.display.update()
            print("ゲームオーバー")
            time.sleep(5)
            pg.quit()
            sys.exit()

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        if sum_mv[0] >= 5:
            kk_img = pg.transform.flip(kk_img, False, True)
        if sum_mv != [0, 0]:
            kk_img = kk_zis[tuple(sum_mv)]
            if sum_mv[0] >= 5:
                kk_img = pg.transform.flip(kk_img, True, False)
        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        avx, avy = vx * accs[min(tmr // 500, 9)], vy * accs[min(tmr // 500, 9)]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #if yoko
            vx *= -1
        if not tate: #if tate
            vy *= -1
        if bb_expand:
            bb_size += 1 #incluce 1
            if bb_size >= 500: #if max
                bb_expand = False
        else:
            bb_size -= 1 #-1
            if bb_size <= 20: #if min
                bb_expand = True
        bb_img = pg.Surface((bb_size, bb_size))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (bb_size // 2, bb_size // 2), bb_size // 2)
        bb_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = bb_center 
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()