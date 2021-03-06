import numpy as np
import pygame

class Ball:
    """Define physics of elastic collision."""

    def __init__(self, mass, radius, position, velocity):
        """Initialize a Ball object

        mass the mass of ball
        radius the radius of ball
        position the position vector of ball
        velocity the velocity vector of ball
        """
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity
        print(self.velocity)
        self.vafter = np.copy(velocity) # temp storage for velocity of next step
        self.delete = False
    def compute_step(self, step):
        """Compute position of next step."""
        #print(self.velocity)
        self.position += step * self.velocity
        #print(self.position)
    def new_velocity(self):
        """Store velocity of next step."""
        self.velocity = self.vafter

    def compute_coll(self, ball, step):
        """Compute velocity after elastic collision with another ball."""
        m1 = self.mass
        m2 = ball.mass
        r1 = self.radius
        r2 = ball.radius
        v1 = self.velocity
        v2 = ball.velocity
        x1 = self.position
        x2 = ball.position
        di = x2-x1
        norm = np.linalg.norm(di)

        if norm-r1-r2 < step*abs(np.dot(v1-v2,di))/norm:
            self.vafter = v1 - 2.*m2/(m1+m2) * np.dot(v1-v2,di)/(np.linalg.norm(di)**2.) * di

    def compute_refl(self, step, borders,obstacle):
        """Compute velocity after hitting an edge.

        step the step of computation
        size the size of a square edge
        """

        r = self.radius
        v = self.velocity
        x = self.position
        projx = step*abs(np.dot(v,np.array([1.,0.])))
        projy = step*abs(np.dot(v,np.array([0.,1.])))

        a = pygame.Rect(0,0,borders[3][0],borders[3][0])
        b = pygame.Rect(0,borders[0][1]+borders[0][3],borders[3][0],borders[3][1]+borders[3][3])
        c = pygame.Rect(borders[2][0]+borders[2][2],0,borders[3][0],borders[3][0])
        d = pygame.Rect(borders[3][0]+borders[3][2],borders[1][1]+borders[1][3],borders[3][0],borders[3][0])

        if(a.collidepoint(*self.position) or b.collidepoint(*self.position) or c.collidepoint(*self.position) or d.collidepoint(*self.position)):
            self.vafter *= 0
            self.delete = True




        else:
            if (abs(x[0])-r -borders[0][0]-borders[0][2] < projx ) or (abs(borders[1][0]- x[0])-r < projx):
                self.vafter[0] *= -1

            if abs(x[1])-r -(borders[2][1]+borders[2][3]) < projy or abs(borders[3][1]-x[1])-r < projy:
                self.vafter[1] *= -1.

            if obstacle != None:
                obs = pygame.Rect(*obstacle)
                if obs.collidepoint(x[0] + r,x[1]):
                    self.vafter[0] = -20
                if obs.collidepoint(x[0] - r,x[1]):
                    self.vafter[0] = 20
                if obs.collidepoint(x[0],x[1]- r):
                    self.vafter[1] = 20
                if obs.collidepoint(x[0], x[1]+ r):
                    self.vafter[1] = -20


def step1(ball_list, step,borders,obstacle=None):
    """Detect reflection and collision of every ball."""

    index_list = range(len(ball_list))
    for i in index_list:
        ball_list[i].compute_refl(step,borders,obstacle)
        for j in index_list:
            if i!=j:
                ball_list[i].compute_coll(ball_list[j],step)
    return ball_list

def step2(ball_list, step):
    """Compute position of every ball."""
    index_list = range(len(ball_list))
    for i in index_list:
        ball_list[i].new_velocity()
        ball_list[i].compute_step(step)
    return ball_list

def solve_step(ball_list, step,borders,obstacle=None):

    """Solve a step for every ball."""
    ball_list = step1(ball_list, step,borders,obstacle)
    ball_list = step2(ball_list, step)


def init_list(N):
    """Generate N Ball objects in a list."""
    ball_list = []
    r = 10.
    for i in range(N):
        v = 10.*np.array([(-1.)**i,1.])
        pos = 800./float(N+1)*np.array([float(i+1),float(i+1)])+[50,50]
        ball_list.append(Ball(r, r, pos, v))
    return ball_list


def gameLoop(time_before):
    ball_list = init_list(20)
    size = 800.
    step = 0.1
    pygame.init()
    border = 50

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    yellow = (255,125,0)
    grey = (0,255,0)

    gameDisplay = pygame.display.set_mode((int(size)+2*border,int(size)+2*border))
    pygame.display.set_caption("Elastic Collision")

    clock = pygame.time.Clock()
    left_border   =  [0,3*border//2,border,size-border]
    right_border  =  [size+border,3*border//2,size+2*border,size-border]
    top_border    =  [3*border//2,0,size-border,border]
    bottom_border =  [3*border//2,size+border,size-border,border]
    pressed = False
    time = 0
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    space = False
    exit = False
    game_over = False
    prev_obs = []

    while(True):
        space = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mp = pygame.mouse.get_pos()
                #print(a)
                pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                pressed = False
        if exit == True:
            pygame.quit()
            quit()
        gameDisplay.fill((255, 255, 255))
        #LEFT
        gameDisplay.fill(yellow, rect=left_border)
        #RIGHT
        gameDisplay.fill(yellow, rect=right_border)
        #UP
        gameDisplay.fill(yellow, rect=top_border)
        #DOWN
        gameDisplay.fill(yellow, rect=bottom_border)

        borders = [left_border,right_border,top_border,bottom_border]
        gameDisplay.fill(black,rect=[0,0,borders[3][0],borders[3][0]])
        gameDisplay.fill(black,rect=[0,borders[0][1]+borders[0][3],borders[3][0],borders[3][1]+borders[3][3] ])
        gameDisplay.fill(black,rect=[borders[2][0]+borders[2][2],0,borders[3][0],borders[3][0]])
        gameDisplay.fill(black,rect=[borders[3][0]+borders[3][2],borders[1][1]+borders[1][3],borders[3][0],borders[3][0]])
        #gameDisplay.fill(black,rect=[borders[2][0]+borders[2]])


        if len(ball_list) == 0:
            textsurface = myfont.render("Game Over. Your time is "+str((time-time_before)//1000), False, (0, 0, 0))
            gameDisplay.blit(textsurface, (size // 2, size // 2 - size // 4))
            game_over = True

        if game_over == False:
            time = pygame.time.get_ticks()
            textsurface = myfont.render('Time: ' + str((time-time_before) // 1000), False, (0, 0, 0))
            gameDisplay.blit(textsurface, (size // 2, 0))
            if pressed == True:

                a =  pygame.mouse.get_pressed()
                print(a)
                if a[0]==1:
                    obstacle = list(pygame.mouse.get_pos()) + [20, 400]
                    #obstacle = list(mp) + [20, 400]
                elif a[2]==1:
                    obstacle = list(pygame.mouse.get_pos()) + [400, 20]
                    #obstacle = list(mp) + [400, 20]

                if obstacle == prev_obs:
                    pygame.draw.rect(gameDisplay,black,obstacle)
                    solve_step(ball_list, step, borders,obstacle)
                else:
                    pygame.draw.rect(gameDisplay,grey,obstacle)
                    solve_step(ball_list, step, borders)
                prev_obs = obstacle

            else:
                solve_step(ball_list, step, borders)
            for i in ball_list:
                if i.delete == True:
                    ball_list.remove(i)
                pygame.draw.circle(gameDisplay,(255, 0, 0) , i.position.astype('int'),int(i.radius))
        else:
            if game_over == True and space == True:
                break

        pygame.display.update()
        clock.tick(1000)
    pygame.quit()
    gameLoop(time)


if __name__ == "__main__":
    gameLoop(0)
