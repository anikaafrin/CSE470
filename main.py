from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def Drawlines(x1,y1, x2, y2, zone):
   dx=x2-x1
   dy=y2-y1
   d=(2*dy)-dx
   incE=2*dy
   incNE=2*(dy-dx)
   y=y1
   for i in range(x1,x2+1):
       if zone==0:
           glPointSize(5)
           glColor3f(0.26, 0.84, 0.92)
           glBegin(GL_POINTS)
           glVertex2f(i, y)
           glEnd()
       elif zone==1:
           glPointSize(5)
           glColor3f(0.26, 0.84, 0.92)
           glBegin(GL_POINTS)
           glVertex2f(y, i)
           glEnd()
       elif zone==2:
           glPointSize(5)
           glColor3f(0.26, 0.84, 0.92)
           glBegin(GL_POINTS)
           glVertex2f(-y, i)
           glEnd()
       elif zone==3:
           glPointSize(5)
           glColor3f(0.26, 0.84, 0.92)
           glBegin(GL_POINTS)
           glVertex2f(-i, y)
           glEnd()
       elif zone==4:
           glPointSize(5)
           glColor3f(0.26, 0.84, 0.92)
           glBegin(GL_POINTS)
           glVertex2f(-i, -y)
           glEnd()
       elif zone==5:
           glPointSize(5)
           glColor3f(0.26, 0.84, 0.92)
           glBegin(GL_POINTS)
           glVertex2f(-y, -i)
           glEnd()
       elif zone==6:
           glPointSize(5)
           glColor3f(0.26, 0.84, 0.92)
           glBegin(GL_POINTS)
           glVertex2f(y, -i)
           glEnd()
       elif zone==7:
           glPointSize(5)
           glColor3f(0.26, 0.84, 0.92)
           glBegin(GL_POINTS)
           glVertex2f(i, -y)
           glEnd()
       if d>0:
           d=d+incNE
           y=y+1
       else:
           d=d+incE
def findZone(x1, y1, x2, y2):
   dx = x2 - x1
   dy = y2 - y1
   if abs(dx)>=abs(dy):
       if dx>=0 and dy>=0:
           Drawlines(x1,y1, x2, y2, 0)
       elif dx<=0 and dy>=0:
           Drawlines(-x1, y1, -x2, y2, 3)
       elif dx<=0 and dy<=0:
           Drawlines(-x1, -y1, -x2, -y2, 4)
       elif dx>=0 and dy<=0:
           Drawlines(x1, -y1, x2, -y2, 7)


   else:
       if dx >= 0 and dy >=0:
           Drawlines(y1, x1, y2, x2, 1)
       elif dx <= 0 and dy >= 0:
           Drawlines(-y1, x1, -y2, x2, 2)
       elif dx <= 0 and dy <= 0:
           Drawlines(-y1, -x1, -y2, -x2, 5)
       elif dx >= 0 and dy <= 0:
           Drawlines(y1, -x1, y2, -x2, 6)
def midpointcircledraw(x_centre, y_centre, r):
    x = r
    y = 0

    # Initialize the value of P
    P = 1 - r

    while x > y:

        y += 1

        # Midpoint inside or on the perimeter (East)
        if P < 0:
            P = P + 2 * y + 3

        # Midpoint outside the perimeter (South East)
        else:
            x -= 1
            P = P + 2 * y - 2 * x + 5

        # All the perimeter points have already been printed
        if (y > x):
            break

        # Printing the generated point its reflection
        # in the other octants after translation
        #zone 0
        glBegin(GL_POINTS)
        glVertex2f(x + x_centre, y + y_centre)
        glEnd()

        #zone 3
        glBegin(GL_POINTS)
        glVertex2f(-x + x_centre, y + y_centre)
        glEnd()
        #zone 4
        glBegin(GL_POINTS)
        glVertex2f(x + x_centre, -y + y_centre)
        glEnd()

        #zone 7
        glBegin(GL_POINTS)
        glVertex2f(-x + x_centre, -y + y_centre)
        glEnd()



        # If the generated point on the line x = y then
        # the perimeter points have already been printed
        if x != y:
            #zone 1
            glBegin(GL_POINTS)
            glVertex2f(y + x_centre, x + y_centre)
            glEnd()

            #zone 2
            glBegin(GL_POINTS)
            glVertex2f(-y + x_centre, x + y_centre)
            glEnd()

            #zone 6
            glBegin(GL_POINTS)
            glVertex2f(y + x_centre, -x + y_centre)
            glEnd()
            #zone 5
            glBegin(GL_POINTS)
            glVertex2f(-y + x_centre, -x + y_centre)
            glEnd()




def draw_points(x, y):
   glPointSize(5) #pixel size. by default 1 thake
   glBegin(GL_POINTS)
   glVertex2f(x,y) #jekhane show korbe pixel
   glEnd()


def iterate():
   glViewport(0, 0, 1000, 1000)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0.0, 1000, 0.0, 1000, 0.0, 1.0)
   glMatrixMode (GL_MODELVIEW)
   glLoadIdentity()



def showScreen():
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glLoadIdentity()
   iterate()
   #glColor3f(0.2, 0.3, 1.0) #konokichur color set (RGB)
   #call the draw methods here
   #draw_points(250, 250)
   i = int(input("give an integer:"))

   l = 300
   r = 400
   x = 100
   for j in range(i):
       findZone(l, 50, r, 50)

       findZone(l, 50 + x, r, 50 + x)
       findZone(l, 50, l, 50 + x)
       findZone(r, 50, r, 50 + x)
       midpointcircledraw(350, 50+(x/2), (x/2))

       glutSwapBuffers()


       l-=50
       r+=50
       x+=100


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)

glutMainLoop()
