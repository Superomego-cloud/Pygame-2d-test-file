import pygame, time, json, os, asyncio, sys

screen = pygame.display.set_mode([720, 500])
currentScriptDir = os.path.dirname(__file__)
if getattr(sys, 'frozen', False):
    currentScriptDir = sys._MEIPASS
else:
    currentScriptDir = os.path.dirname(os.path.abspath(__file__))

image = pygame.image.load(os.path.join(currentScriptDir, 'Assets/box art/pee.jpg')).convert()
running = True 
dead = False
win = False
currentData = ""
SmallJump = False
powerList = ("red", "orange", "yellow", "green", "cyan", "indigo", "purple", "Normie")
dirList = [os.path.join(currentScriptDir, "Assets/box art/usable boxes/1-redbox.png"),os.path.join(currentScriptDir, "Assets/box art/usable boxes/2-orangebox.png"), os.path.join(currentScriptDir, "Assets/box art/usable boxes/3-yellowbox.png"), os.path.join(currentScriptDir, "Assets/box art/usable boxes/4-greenbox.png"),os.path.join(currentScriptDir, "Assets/box art/usable boxes/5-cyanbox.png"), os.path.join(currentScriptDir, "Assets/box art/usable boxes/6-indigobox.png"), os.path.join(currentScriptDir, "Assets/box art/usable boxes/7-purplebox.png")]
inventory = False
clock = pygame.time.Clock()
StartJumpTimer = [False, 0]
StartRunTimer = [False, 0]
collidedObjectTop = ""

with open(os.path.join(currentScriptDir, 'Assets/LevelList/Lvl1.json'), "r") as read_file:
    currentData = json.load(read_file)

class Player:
    def __init__(self, xpl, ypl,hp):
        self.hitbox = pygame.Rect([xpl, ypl],[64, 64])
        self.coord = [xpl, ypl]
        self.vel = [1, 2]
        self.defvel = tuple(self.vel)
        self.inventory = {"red":0, "orange":0, "yellow":0, "green":0, "cyan":0, "indigo":0, "purple":0}
        self.hp = hp
        self.maxhp = hp 
        self.hpbar = pygame.Rect([self.hitbox.left - 10, self.hitbox.top - 30], [80, 10])

class Wall:
    
    def __init__(self, arr=list, rgbArr = [255, 255, 255], ability = str ,killVal=50):
        self.defaulthitbox = pygame.Rect([arr[0], arr[2]],[arr[1] - arr[0], arr[3] - arr[2]]) 
        self.hitbox = pygame.Rect([arr[0], arr[2]],[arr[1] - arr[0], arr[3] - arr[2]])
        self.color = rgbArr 
        self.ability = ability
        if ability == powerList[0] or ability == powerList[3]:
            self.dmg = killVal
        self.touched = False
        self.anim = False
    
    def jump(self):
        
        global StartJump
        
        player.vel[1] = player.vel[1]*2
        StartJump = True
    
    def run(self):
        player.vel[0] = player.vel[0]*2

    def money(self):
        newBox = BoxObject("yellow", [self.hitbox.left + ((self.hitbox.width/2) - 32), self.hitbox.top - 164], dirList[2])
        anim(self)
        newArr2.append(newBox)
        self.touched = True

    def heal(self):
        player.hp = player.maxhp
        self.touched = True

class LevelLayout:
    def __init__(self, RelativeInterval=list, LevelName = str, objList = list, bugBypass = bool):
        self.RelativeInterval = RelativeInterval
        self.LevelName = LevelName
        self.objList = objList
        self.bugBypass = bugBypass

class BoxObject:
    def __init__(self, color, pos, sprite):
        self.hitbox = pygame.Rect(pos, [64,64])
        self.defaulthitbox = pygame.Rect(pos, [64,64])
        self.color = color
        self.sprite = pygame.image.load(sprite).convert_alpha()
    async def jump(a):
        player.vel[1] += player.vel[1]
        StartJumpTimer[0] = True
        StartJumpTimer[1] = 6000

player = Player(150, 236, 100)
Arr = currentData["ObjectList"]
Arr2 = currentData["BoxList"]
newArr = []
newArr2 = []
boxArr = []
level = ""

def anim(obj):
    
    if obj.ability == "yellow":
        obj.color[2] += 2
        if obj.color[2] == 250:
            obj.anim = False
            obj.ability = "Normie"

def updAnim():
    for obj in newArr:
        if obj.anim:
            anim(obj)

def drawobj():
    for obj in newArr:
        if obj.hitbox.left < 720 and obj.hitbox.right > 0:
            pygame.draw.rect(screen, obj.color, obj.hitbox)
    for obj in newArr2:
        screen.blit(obj.sprite, [obj.hitbox.left, obj.hitbox.top])
    return

def load():
    
    global level
    global boxArr
    
    pygame.init()

    currentObj = ""
    currentBox = ""
    for obj in Arr:
        currentObj = Wall(Arr[obj]["hitbox"], Arr[obj]["color"], Arr[obj]["ability"], Arr[obj]["dmg"])
        newArr.append(currentObj)
    for box in Arr2:
        currentBoxSprite = int(Arr2[box]["spriteIndex"])
        for box in Arr2[box]["boxList"]:
            currentBox = BoxObject(powerList[currentBoxSprite],box, dirList[currentBoxSprite])
            newArr2.append(currentBox)
            boxArr.append(currentBox)
    level = LevelLayout(currentData["LevelSize"], currentData["name"], newArr, currentData["bugBypass"])
    boxArr = tuple(boxArr)

def boxGrav():
    
    for obj in newArr2:
        collision = False
        obj.hitbox.move_ip(0, 1)
        for obj2 in newArr:
            if pygame.Rect.colliderect(obj.hitbox, obj2.hitbox):
                collision = True
                if obj2.ability == powerList[0]:
                    newArr2.remove(obj)
                break        
            for obj2 in newArr2:
                if obj2 == obj:
                    continue
                if pygame.Rect.colliderect(obj.hitbox, obj2.hitbox):
                    collision = True
                    break
        
        if not collision:
            obj.hitbox.move_ip(0, 1)
        
        obj.hitbox.move_ip(0, -1)

def playerCol():
    
    for obj in newArr2:
        if pygame.Rect.colliderect(obj.hitbox, player.hitbox):
            newArr2.remove(obj)
            player.inventory[obj.color] += 1
            match obj.color:
                case "red":
                    player.hp -= 10
                case "green":
                    if player.hp < player.maxhp - 10:
                        player.hp += 10
                    elif player.hp < player.maxhp:
                        player.hp = player.maxhpxhp
                case "orange":
                    asyncio.run(obj.jump())

def HpBarUpdate():
    pygame.draw.rect(screen, [255, 0, 0], player.hpbar)
    pygame.draw.rect(screen, [0, 255, 0], pygame.Rect([player.coord[0] - 10, player.coord[1] - 30], [player.hpbar.width*(player.hp/player.maxhp), 10]))

def collisionCheck():

    global player
    global collisionRight
    global collisionLeft
    global collisionUp
    global collisionDown
    global StartJump
    global SmallJump

    player.hitbox.move_ip(1, 0)
    for obj in newArr:
        if pygame.Rect.colliderect(player.hitbox, obj.hitbox):
            collisionRight = True
            if obj.ability == powerList[0]:
                player.hp -= obj.dmg
            break
        else:
            collisionRight = False

    player.hitbox.move_ip(-1, 0)

    player.hitbox.move_ip(-1, 0)
    for obj in newArr:
        if pygame.Rect.colliderect(player.hitbox, obj.hitbox):
            collisionLeft = True
            if obj.ability == powerList[0]:
                player.hp -= obj.dmg
            if obj.ability == powerList[3]:
                obj.heal()
                obj.anim = True
            break
        else:
            collisionLeft = False
    player.hitbox.move_ip(1, 0)

    player.hitbox.move_ip(0, 2)
    for obj in newArr:
        if pygame.Rect.colliderect(player.hitbox, obj.hitbox):
            collisionDown = True
            match obj.ability:
                case "red":
                    player.hp -= obj.dmg
                case "orange":
                    obj.jump()
                case "yellow":
                    if not obj.touched:
                        obj.money()
                        obj.anim = True
                case "green":
                    player.hp += obj.dmg 
                    obj.anim = True
                case "cyan":
                    obj.run()
            break
        else:
            collisionDown = False
            player.vel[0] = player.defvel[0]
            player.vel[1] = player.defvel[1]
    
    player.hitbox.move_ip(0, -2)

    player.hitbox.move_ip(0, -2)
    for obj in newArr:
        if pygame.Rect.colliderect(player.hitbox, obj.hitbox):
            collisionUp = True
            if obj.ability == powerList[0]:
                player.hp -= obj.dmg
            break
        else:
            collisionUp = False
    player.hitbox.move_ip(0, 2)

def delodge():
    
    global y

    for obj in newArr:
        if pygame.Rect.colliderect(player.hitbox, obj.hitbox):
            if (player.hitbox.top - obj.hitbox.bottom)<(player.hitbox.bottom - obj.hitbox.top):
                y -= obj.hitbox.bottom - player.hitbox.top
            else:
                y += player.hitbox.bottom - obj.hitbox.top
            break

movement = False
right = False
left = False
up = False
StartJump = False
jump = False
ijump = 0
x = 0
y = 0

load()

while running:

    clock.tick(500)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            movement = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_UP:
                up = True
            if event.key == pygame.K_e:
                if not inventory:
                    inventory = True
                else:
                    inventory = False
        if event.type == pygame.KEYUP:
            movement == False        
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_UP:
                up = False   
    
    if player.hp <= 0:
            dead = True

    if StartJumpTimer[0]:
        if StartJumpTimer[1]>0:
            StartJumpTimer[1] -= 1
        else:
            StartJumpTimer[0] = False
            player.vel[1] -= player.vel[1]/2

    if StartRunTimer[0]:
        if StartRunTimer[1]>0:
            StartRunTimer -= 1
        else:
            StartRunTimer[0] = False
            player.vel[0] -= player.vel[0]/2

    
    if not inventory:

        if len(newArr2)>0:
            boxGrav()
            playerCol()
        
        collisionCheck()
        updAnim()

        if movement:
            if right and not collisionRight:
                x -= player.vel[0]
            if left and not collisionLeft:
                x += player.vel[0]
            
            if up and not jump and not StartJump:
                StartJump = True
            
            if StartJump:    
                ijump += 1
                if not collisionUp and not ijump > 106:
                    y += player.vel[1] 
                else:
                    StartJump = False
                    ijump = 0
                    jump = True

            if not collisionDown:
                if not StartJump:
                    y -= player.vel[1]
            else:
                jump = False
            
            if collisionUp and collisionDown:
                delodge()
                if not level.bugBypass:
                    jump = True

            if x != 0 or y != 0:    
                for obj in newArr:
                    obj.hitbox.move_ip(x, y)
                for obj in newArr2:
                    obj.hitbox.move_ip(x, y)
                x = 0 
                y = 0
        
        screen.fill([0,0,0])
        drawobj()
        if not dead:
            screen.blit(image, player.coord)   
            if player.hp != player.maxhp:
                HpBarUpdate()
            pygame.display.flip()
        else:
            pygame.display.flip()
            time.sleep(1)
            player.hp = 100
            dead = False
            for obj in newArr:
                obj.hitbox.left = obj.defaulthitbox.left
                obj.hitbox.top = obj.defaulthitbox.top
                obj.hitbox.width = obj.defaulthitbox.width
                obj.hitbox.height = obj.defaulthitbox.height
                obj.touched = False
            newArr2 = []
            for obj in boxArr:
                newArr2.append(obj)
                obj.hitbox.left = obj.defaulthitbox.left
                obj.hitbox.top = obj.defaulthitbox.top
                obj.hitbox.width = obj.defaulthitbox.width
                obj.hitbox.height = obj.defaulthitbox.height
            player.inventory = {"red":0, "orange":0, "yellow":0, "green":0, "cyan":0, "indigo":0, "purple":0}

    else:
        screen.fill([0,100,0])
        pygame.display.flip()

pygame.quit()