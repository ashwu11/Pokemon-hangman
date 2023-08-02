import pygame
import math
import random

# set up display
pygame.init()
WIDTH, HEIGHT = 800, 550
game = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hangman Game")

# load images
images = []
for i in range(7):
  image = pygame.image.load("hangman" + str(i) + ".png")
  images.append(image)

# game variables
words = ["PICHU", "TOGEPI", "RIOLU", "MUNCHLAX", "HAPPINY", 
         "CLEFFA", "IGGLYBUFF", "ELEKID", "BUDEW", "AZURILL", 
         "MAGBY", "MEW", "CHIMECO", "SMOOCHUM", "TYROGUE", 
         "WYNAUT", "MANTYKE", "TOXEL", "CHINGLING"]
status = 0
guessed = []
word = random.choice(words)

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65

def reset_buttons():
  for i in range (26):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = starty + ((i//13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 35)
WORD_FONT = pygame.font.SysFont('comicsans', 55)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (186,225,255)
DBLUE = (153, 204, 255)
PINK = (255, 204, 255)
ORANGE = (255,223,186)
PURPLE = (255, 204, 255)
GREEN = (204, 255, 204)

def draw():
  game.fill(WHITE)

  #draw title
  text = TITLE_FONT.render("POKEMON HANGMAN", 1, BLACK)
  game.blit(text, (WIDTH/2 - text.get_width()/2, 30))

  # draw word
  display_word = ""
  for letter in word:
    if letter in guessed:
      display_word += letter + " "
    else:
      display_word += "_ "
      
  text = WORD_FONT.render(display_word, 1, DBLUE)
  game.blit(text, (370, 220))

  # draw buttons
  for letter in letters:
    x, y , ltr , visible = letter
    if visible: 
      pygame.draw.circle(game, DBLUE, (x,y), RADIUS, 3)
      text = LETTER_FONT.render(ltr, 1, DBLUE)
      game.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
  
  game.blit(images[status], (100, 120))
  pygame.display.update()

def display_message(message, background, colour):
  pygame.time.delay(1000)
  game.fill(background)
  text = TITLE_FONT.render(message, 1, colour)
  game.blit(text, (WIDTH/2 - text.get_width()/2, 
                    HEIGHT/2 - text.get_height()/2))
  pygame.display.update()
  pygame.time.delay(3000)

# runs game loop
def main():
  global status
  
  status = 0
  FPS = 60
  clock = pygame.time.Clock()
  run = True
  
  while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        m_x, m_y = pygame.mouse.get_pos()
        for letter in letters:
          x, y, ltr, visible = letter
          if visible:
            dist = math.sqrt((x - m_x)**2 + (y - m_y)**2)
            if dist < RADIUS:
              letter[3] = False
              guessed.append(ltr)
              if ltr not in word:
                status += 1
  
    draw()
    
    # check if game is over
    win = True
    for letter in word:
      if letter not in guessed:
        win = False
        break
  
    if win:
      display_message("Congratulations!", GREEN, BLACK)
      break
  
    if status == 6:
      display_message("Unfortunate...", PINK, BLACK)
      break

def reset_variables(status, guessed, word):
  return 0, [], random.choice(words)

reset_buttons()
main()
while True:
  display_message("Play again?", WHITE, PURPLE)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        run = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        status, guessed, word = reset_variables(status, guessed, word)
        reset_buttons()
        main()
      
pygame.quit()