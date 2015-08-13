TEXT_ALIGN_LEFT=0
TEXT_ALIGN_CENTER=1
TEXT_ALIGN_RIGHT=2


def drawtextcentered(surface, position, font, text="", aa=1, color=(255,255,255), alignment=(1,1)):
    surf=font.render(text, aa, color)
    rect=surf.get_rect()
    newpos=[0,0]
    for i in xrange(2):
        if alignment[i]==TEXT_ALIGN_LEFT:
            newpos[i]=position[i]
        elif alignment[i]==TEXT_ALIGN_CENTER:
            newpos[i]=position[i]-rect.center[i]
        elif alignment[i]==TEXT_ALIGN_RIGHT:
            newpos[i]=position[i]-rect.bottomright[i]
    #print newpos
    surface.blit(surf, newpos)
    