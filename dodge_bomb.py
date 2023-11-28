import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 700

delta = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}

def check_bound(rct: pg.Rect) -> tuple[bool,bool]:#練習4
    """
    オブジェクトが画面内or画面外を判定し、真理値をタプルに返す関数
    引数　rct：コウカトンor爆弾SurfaceのRect
    戻り値：横方向、縦方向判断結果（画面内：True/画面外False）
    """
    yoko ,tate = True, True
    if rct.left < 0 or WIDTH < rct.right:#横方向はみだし判定
        yoko = False

    if rct.top < 0 or HEIGHT < rct.bottom:#縦方向はみだし判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900,400#
    bb_img = pg.Surface((20,20))  #練習1　透明なsurfaceを作る
    bb_img.set_colorkey((0,0,0)) #練習1　黒をなくす
    pg.draw.circle(bb_img,(255,0,0), (10,10), 10)
    bb_rct = bb_img.get_rect() #練習1-3

    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    vx,vy =+5,+5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            return
        key_lst = pg.key.get_pressed() #練習3
        sum_mv = [0,0]
        for k, tpl in delta.items():
            if key_lst[k]:  #キーが押されたら反応
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True): # 練習4 はみ出てない判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct) #練習1 ぶりっと
        bb_rct.move_ip(vx,vy) #練習2　爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:#横方向にはみ出たら
            vx *= -1
        if not tate:#縦方向にはみ出たら
            vy *= -1
        
        pg.display.update()
        tmr += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()