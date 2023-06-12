import graphics
import time
import random
import math

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400
PADDLE_BOTTOM_Y1 = CANVAS_HEIGHT - 30 #paddle stays a bit above from the bottom
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
FONT_SIZE = CANVAS_HEIGHT/25
USER_ERROR_MARGIN = BALL_RADIUS*1.1 #it means paddle covers more area on left and right. higher number makes easier to catch the ball.
DELAY = 0.05

#a list that stores scores locally, resets when program stops
scores = [] 

def main():
    canvas = graphics.Canvas(CANVAS_WIDTH,CANVAS_HEIGHT-BALL_RADIUS*2)
    
    #user chooses EASY or HARD game mode
    game_mode = game_mode_function(canvas)
    canvas.clear()
    
    #starting score
    score = 0
    
    #starting speed
    speed = speed_function(score, game_mode)
    
    #creates a red line under the paddle
    line = canvas.create_rectangle(0, CANVAS_HEIGHT-25, CANVAS_WIDTH, CANVAS_HEIGHT, "red")

    #creates the first paddle
    paddle_color = paddle_color_function(score)
    paddle_width = paddle_width_function(score, game_mode)
    paddle_top_x = (CANVAS_WIDTH/2) - (paddle_width/2)
    paddle_top_y = PADDLE_BOTTOM_Y1 - PADDLE_HEIGHT
    paddle_bottom_x = paddle_top_x + paddle_width
    paddle_bottom_y = PADDLE_BOTTOM_Y1
    paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_bottom_x, paddle_bottom_y, str(paddle_color))

    #creates the first ball in random position on top
    ball_left_x = random.randint(0, CANVAS_WIDTH - BALL_RADIUS*2)
    ball = canvas.create_oval(ball_left_x, 0, ball_left_x + BALL_RADIUS*2, 0 + BALL_RADIUS*2, "green")
    
    #to start and stop the game, it uses "game" variable and assigns "ON" or "OVER" to it
    game = "ON" 
    
    while game == "ON":
        canvas.move(ball, 0, 10) #moves the ball, top-down
        mouse_x_adjusted = canvas.get_mouse_x() - paddle_width/2 #get mouse coordinate and adjust it to the center of paddle
        canvas.moveto(paddle, mouse_x_adjusted, paddle_top_y) #moves paddle to mouse's coordinate
        time.sleep(DELAY - speed) #for animation effect. it also means speed of the ball

        #gets ball's coordinates
        ball_top_x = canvas.get_left_x(ball)
        ball_top_y = canvas.get_top_y(ball)
       
        #gets paddle's coordinate
        paddle_top_x = canvas.get_left_x(paddle)

        #GAME OVER case
        #if ball touches the bottom
        if ball_top_y > CANVAS_HEIGHT:
            canvas.clear() #clears the player screen
            game = "OVER"

            #shows the game over, score, restart note, high scores texts (like a menu UI)
            game_over_text = canvas.create_text(10, 10, font_size = int(FONT_SIZE), text='GAME OVER!')
            game_over_score = canvas.create_text(10, 10 + int(FONT_SIZE) + 5, font_size = int(FONT_SIZE), text='Score: ' + str(score))
            game_over_game_mode = canvas.create_text(10, 10 + int(FONT_SIZE) + 25, font_size = int((FONT_SIZE)*2/3), color ="gray", text=game_mode + " MODE")
            game_over_note = canvas.create_text(10, CANVAS_HEIGHT - (FONT_SIZE * 3), font_size = int(FONT_SIZE), text="Click anywhere to restart...")
            high_scores (canvas, score)
            
            #to restart the game, waits for the mouse click on the canvas
            canvas.wait_for_click()
            canvas.clear()
            canvas.get_new_mouse_clicks()
            
            #asks game mode when game is over and restarts
            game_mode = game_mode_function(canvas)
            canvas.clear()
            
            #after restarts it creates the line, ball and paddle again before animations start
            #creates a red line under the paddle
            line = canvas.create_rectangle(0, CANVAS_HEIGHT-25, CANVAS_WIDTH, CANVAS_HEIGHT, "red")
            
            #creates a ball in random position on top
            ball_left_x = random.randint(0, CANVAS_WIDTH - BALL_RADIUS*2)
            ball = canvas.create_oval(ball_left_x, 0, ball_left_x + BALL_RADIUS*2, 0 + BALL_RADIUS*2, "green")

            #creates the paddle
            paddle_width = paddle_width_function(score, game_mode)
            paddle_top_x = CANVAS_WIDTH/2 - paddle_width/2
            paddle_top_y = PADDLE_BOTTOM_Y1 - PADDLE_HEIGHT
            paddle_bottom_x = paddle_top_x + paddle_width
            paddle_bottom_y = PADDLE_BOTTOM_Y1
            paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_bottom_x, paddle_bottom_y, "grey")
            
            score = 0
            speed = speed_function(score, game_mode)
            game = "ON"


        #SCORE case, when catch the ball
        #if paddle touchs the ball
        elif paddle_top_x - USER_ERROR_MARGIN <= (ball_top_x + BALL_RADIUS) and (paddle_top_x + paddle_width) + USER_ERROR_MARGIN >= ball_top_x + BALL_RADIUS and ball_top_y + BALL_RADIUS == (paddle_top_y + PADDLE_HEIGHT/3):
            canvas.delete(ball)
            ball_left_x = random.randint(0, CANVAS_WIDTH - BALL_RADIUS*2)
            ball = canvas.create_oval(ball_left_x, 0, ball_left_x + BALL_RADIUS*2, 0 + BALL_RADIUS*2, "green")
            
            if score > 0: #if there is no score, there is no game_score text to delete
                canvas.delete(game_score)
            score += 1
            
            speed = speed_function(score, game_mode)
            paddle_width = paddle_width_function(score, game_mode)
            canvas.delete(paddle)
            paddle_color = paddle_color_function(score)
            paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_top_x + paddle_width, paddle_bottom_y, str(paddle_color))
            
            #shows the score dynamically on top left
            game_score = canvas.create_text(10, 10, font_size = int(FONT_SIZE), text='Score: ' + str(score))

#score_up_function out of use
def score_up_function(canvas, score, paddle, game_mode, paddle_top_x, paddle_top_y, paddle_bottom_y):
        if score > 0: #if there is no score, there is no game_score text to delete
            canvas.delete(game_score)
        score += 1
        game_score = canvas.create_text(10, 10, text='Score: ' + str(score))
        speed = speed_function(score, game_mode)
        paddle_width = paddle_width_function(canvas, score)
        canvas.delete(paddle)
        paddle_color = paddle_color_function(score)
        paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_top_x + paddle_width, paddle_bottom_y, str(paddle_color))

#game_over_function out of use
def game_over_function(canvas, score, game_mode, game, ball):

    if score > 0:
        canvas.delete(game_score)
    canvas.clear() #clears the player screen
    game = "OVER"

    #shows the game over, score, restart note, high scores texts (like a menu UI)
    game_over_text = canvas.create_text(10, CANVAS_HEIGHT/2, anchor = "center", font_size = int(FONT_SIZE), text='GAME OVER!')
    game_over_score = canvas.create_text(10, CANVAS_HEIGHT/2 + int(FONT_SIZE) + 5, font_size = int(FONT_SIZE), text='Score: ' + str(score))
    game_over_note = canvas.create_text(10, CANVAS_HEIGHT - (FONT_SIZE * 3), font_size = int(FONT_SIZE), text="Click anywhere to restart...")
    high_scores (canvas, score)
    
    #to restart the game, waits for the mouse click on the canvas
    canvas.wait_for_click()
    canvas.clear()
    time.sleep(0.5)
    
    #asks game mode when game is over and restarts
    game_mode = game_mode_function(canvas)
    canvas.clear()
    
    #after restarts it creates the line, ball and paddle again before animations start
    #creates a red line under the paddle
    line = canvas.create_rectangle(0, CANVAS_HEIGHT-25, CANVAS_WIDTH, CANVAS_HEIGHT, "red")
    
    #creates a ball in random position on top
    ball_left_x = random.randint(0, CANVAS_WIDTH - BALL_RADIUS*2)
    ball = canvas.create_oval(ball_left_x, 0, ball_left_x + BALL_RADIUS*2, 0 + BALL_RADIUS*2, "green")

    #creates the paddle
    paddle_width = paddle_width_function(score, game_mode)
    paddle_top_x = CANVAS_WIDTH/2 - paddle_width/2
    paddle_top_y = PADDLE_BOTTOM_Y1 - PADDLE_HEIGHT
    paddle_bottom_x = paddle_top_x + paddle_width
    paddle_bottom_y = PADDLE_BOTTOM_Y1
    paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_bottom_x, paddle_bottom_y, "grey")
    
    score = 0
    speed = speed_function(score, game_mode)
    game = "ON"

#create_origin_paddle function out of use
def create_origin_paddle (canvas, score, game_mode):
        #creates an origin paddle
        paddle_width = paddle_width_function(score, game_mode)
        paddle_top_x = CANVAS_WIDTH/2 - paddle_width/2
        paddle_top_y = PADDLE_BOTTOM_Y1 - PADDLE_HEIGHT
        paddle_bottom_x = paddle_top_x + paddle_width
        paddle_bottom_y = PADDLE_BOTTOM_Y1
        paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_bottom_x, paddle_bottom_y, "grey")

#game mode selection screen
def game_mode_function(canvas):
    easy_text = canvas.create_text(200, CANVAS_HEIGHT/2, font_size = int(FONT_SIZE)*2, text = 'EASY <<< ', anchor = "center", color = "forestgreen")
    info_text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT*3/4, font_size = int(FONT_SIZE), text = 'Click with your mouse to choose your game mode', anchor = "center", color = "black")
    hard_text = canvas.create_text(CANVAS_WIDTH-200, CANVAS_HEIGHT/2, font_size = int(FONT_SIZE)*2, text = '>>> HARD', anchor = "center", color = "salmon")
    
    paddle_width = 80
    paddle_top_x = CANVAS_WIDTH/2 - paddle_width/2
    paddle_top_y = PADDLE_BOTTOM_Y1 - PADDLE_HEIGHT
    paddle_bottom_x = paddle_top_x + paddle_width
    paddle_bottom_y = PADDLE_BOTTOM_Y1

    while True:
        paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_bottom_x, paddle_bottom_y, random_color())
        mouse_x_adjusted = canvas.get_mouse_x() - paddle_width/2 #get mouse coordinate and adjust it to the center of paddle
        ball = canvas.create_oval(0, 0, BALL_RADIUS*2, BALL_RADIUS*2, color = "green")
        canvas.moveto(paddle, mouse_x_adjusted, PADDLE_BOTTOM_Y1) #moves paddle to mouse's coordinate
        canvas.moveto(ball, (CANVAS_WIDTH-canvas.get_mouse_x()), 0) #moves ball, depends on mouse's coordinate
        time.sleep(DELAY)
        canvas.delete(paddle)
        canvas.delete(ball)
        
        clicks = canvas.get_new_mouse_clicks()
    
        #EASY mode selection
        if canvas.get_mouse_x() < CANVAS_WIDTH*1/2 and CANVAS_HEIGHT/2 - 100 < canvas.get_mouse_y() < CANVAS_HEIGHT/2 + 100:
            canvas.delete(easy_text)
            canvas.delete(hard_text)
            easy_text = canvas.create_text(200, CANVAS_HEIGHT/2, font_size = int(FONT_SIZE)*3, text = 'EASY <<< ', anchor = "center", color = "forestgreen")
            hard_text = canvas.create_text(CANVAS_WIDTH-200, CANVAS_HEIGHT/2, font_size = int(FONT_SIZE)*2, text = '>>> HARD', anchor = "center", color = "salmon")
            if len(clicks) > 0:
                return "EASY"

        #HARD mode selection
        elif canvas.get_mouse_x() > CANVAS_WIDTH*1/2 and CANVAS_HEIGHT/2 - 100 < canvas.get_mouse_y() < CANVAS_HEIGHT/2 + 100:
            canvas.delete(hard_text)
            canvas.delete(easy_text)
            easy_text = canvas.create_text(200, CANVAS_HEIGHT/2, font_size = int(FONT_SIZE)*2, text = 'EASY <<< ', anchor = "center", color = "forestgreen")
            hard_text = canvas.create_text(CANVAS_WIDTH-200, CANVAS_HEIGHT/2, font_size = int(FONT_SIZE)*3, text = '>>> HARD', anchor = "center", color = "salmon")
            if len(clicks) > 0:
                return "HARD"

        #while mouse hover around
        else:
            canvas.delete(hard_text)
            canvas.delete(easy_text)
            easy_text = canvas.create_text(200, CANVAS_HEIGHT/2, font_size = int(FONT_SIZE)*2, text = 'EASY <<< ', anchor = "center", color = "forestgreen")
            hard_text = canvas.create_text(CANVAS_WIDTH-200, CANVAS_HEIGHT/2, font_size = int(FONT_SIZE)*2, text = '>>> HARD', anchor = "center", color = "salmon")
        
def random_color():
    colors = ['blue', 'purple', 'salmon', 'lightblue', 'cyan', 'forestgreen', 'gray', 'midnightblue', 'silver']
    return random.choice(colors) #returns a random color

#changes paddle color, depends on score and game mode
def paddle_color_function(score):        
    if score < 16:
        return "gray"
        
    elif score > 15 and score < 51:
        return "midnightblue"
    
    elif score > 50 and score < 95:
        return "lightsteelblue" 
    
    elif score > 94:
        return "silver"

#changes paddle width, depends on score and game mode
def paddle_width_function(score, game_mode):
    if game_mode == "EASY":
        if score < 16:
            return BALL_RADIUS*8 #starting width for easy mode

        elif score > 15 and score < 51:
            return BALL_RADIUS*7 #shorter paddle makes it harder, starting from score 16 to 50

        elif score > 50 and score < 95:
            return BALL_RADIUS*5 #shorter paddle makes it harder, starting from score 51 to 94

        elif score > 94:
            return BALL_RADIUS*3 #shortest paddle after score 95
 

    elif game_mode == "HARD":
        if score < 16:
            return BALL_RADIUS*6 #starting width for hard mode

        elif score > 15 and score < 51:
            return BALL_RADIUS*5 #shorter paddle makes it harder, starting from score 16 to 50

        elif score > 50 and score < 95:
            return BALL_RADIUS*3 #shorter paddle makes it harder, starting from score 51 to 94

        elif score > 94:
            return BALL_RADIUS*2 #shortest paddle after score 95
            
    else:
        return BALL_RADIUS*2

#changes speed, depends on score and game mode
def speed_function(score, game_mode):
    #random speed adjustments to make the game harder
    #actual speed is "DELAY - speed" (since DELAY is 0.05, recommended speed is between 0.01 to 0.049)
    if game_mode == "EASY":
        if score < 3:
            speed = 0 
        elif score > 2 and score < random.randint(5,19):
            speed = random.uniform(0.040, 0.045)	
        elif score > 19 and score < random.randint(30,39):
            speed = random.uniform(0.042, 0.046)
        elif score > 39 and score < 50:
            speed = 0.047
        elif score > 49 and score < 100:
            speed = random.uniform(0.047, 0.049)
        elif score > 99:
            speed = 0.049
        else:
            speed = 0
        return speed

    elif game_mode == "HARD":
        if score < 3:
            speed = 0.030
        elif score > 2 and score < random.randint(8,12):
            speed = random.uniform(0.040, 0.045)	
        elif score > 11 and score < random.randint(30,39):
            speed = random.uniform(0.042, 0.046)
        elif score > 39 and score < 50:
            speed = 0.047
        elif score > 49 and score < 100:
            speed = random.uniform(0.047, 0.049)
        elif score > 99:
            speed = 0.049
        else:
            speed = 0
        return speed


#SHOWS TOP 5 SCORES
def high_scores(canvas, score):
    #gets the last score
    #check if there is more than 5 scores (including "0" scores)
    #if there is more than 5 scores, shows only top 5
    #sorts max 5 score values
    #create text blocks on the canvas
    
    if len(scores) > 0:
        if score > 0 and score > scores [0]:
            new_high_score_text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, anchor = "center", font_size = int(FONT_SIZE)*3, text="NEW HIGH SCORE!!!", color = random_color())

    
    scores.append(score)
    size_of_score = len(scores)
    scores.sort(reverse=True) #sorts scores from higher to lower
    
    high_score_text = canvas.create_text(CANVAS_WIDTH - (FONT_SIZE * 7), 10, font_size = int(FONT_SIZE), text='High Scores', color = "green")
    if size_of_score > 4:
        for i in range (5):
            high_score = canvas.create_text(CANVAS_WIDTH - (FONT_SIZE * 7), 10 + (i+1)*(int(FONT_SIZE) + 5), text= str(i+1) + '............ ' + str(scores[i])) 
    else:
        for i in range (size_of_score):
            high_score = canvas.create_text(CANVAS_WIDTH - (FONT_SIZE * 7), 10 + (i+1)*(int(FONT_SIZE) + 5), text= str(i+1) + '............ ' + str(scores[i]))


    #it would be nice to show --game mode-- for every score
    

if __name__ == '__main__':
    main()
