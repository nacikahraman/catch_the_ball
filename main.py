import graphics
import time
import random
import math

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400
PADDLE_Y = CANVAS_HEIGHT - 30
#PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
FONT_SIZE = CANVAS_HEIGHT/25
USER_ERROR_MARGIN = 1.05

scores = []

def main():
    canvas = graphics.Canvas(CANVAS_WIDTH,CANVAS_HEIGHT-BALL_RADIUS*2)
    
    #Paddle creation
    PADDLE_WIDTH = 80
    paddle_top_x = CANVAS_WIDTH/2 - PADDLE_WIDTH/2
    paddle_top_y = PADDLE_Y
    paddle_bottom_x = paddle_top_x + PADDLE_WIDTH
    paddle_bottom_y = paddle_top_y + PADDLE_HEIGHT
    paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_bottom_x, paddle_bottom_y, "grey")

    #Ball creation
    ball_left_x = random.randint(0, CANVAS_WIDTH - BALL_RADIUS*2)
    ball = canvas.create_oval(ball_left_x, 0, ball_left_x + BALL_RADIUS*2, 0 + BALL_RADIUS*2, "green")
    
    score = 0
    speed = 0 #speed level (between 0.01 to 0.04)
    game = "ON"
    
    while game == "ON":
        canvas.move(ball, 0, 10)
        mouse_x_adjusted = canvas.get_mouse_x() - PADDLE_WIDTH/2
        canvas.moveto(paddle, mouse_x_adjusted, paddle_top_y)
        time.sleep(0.0500 - speed)

        ball_top_x = canvas.get_left_x(ball)
        ball_top_y = canvas.get_top_y(ball)
        
        paddle_top_x = canvas.get_left_x(paddle)
        #paddle_top_y = canvas.get_top_y(paddle)
        
        if ball_top_y > CANVAS_HEIGHT:
            ball_left_x = random.randint(0, CANVAS_WIDTH - BALL_RADIUS*2)
            ball = canvas.create_oval(ball_left_x, 0, ball_left_x + BALL_RADIUS*2, 0 + BALL_RADIUS*2, "green")
            if score > 0:
                canvas.delete(game_score)
            canvas.clear()
            game_over_text = canvas.create_text(10, CANVAS_HEIGHT/2, font_size = int(FONT_SIZE), text='GAME OVER!')
            game_over_score = canvas.create_text(10, CANVAS_HEIGHT/2 + int(FONT_SIZE) + 5, font_size = int(FONT_SIZE), text='Score: ' + str(score))
            game_over_note = canvas.create_text(10, CANVAS_HEIGHT - (FONT_SIZE * 3), font_size = int(FONT_SIZE), text="Press 'R' to restart...")
            high_scores (canvas, score)
            
            game = "OVER"
            while game == "OVER":
                key = canvas.get_last_key_press()
                print(key)
                if key == "R" or key == "r":
                    canvas.clear()
                    #Paddle creation
                    paddle_top_x = CANVAS_WIDTH/2 - PADDLE_WIDTH/2
                    paddle_top_y = PADDLE_Y
                    paddle_bottom_x = paddle_top_x + PADDLE_WIDTH
                    paddle_bottom_y = paddle_top_y + PADDLE_HEIGHT
                    paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_bottom_x, paddle_bottom_y, "grey")
                
                    #Ball creation
                    ball_left_x = random.randint(0, CANVAS_WIDTH - BALL_RADIUS*2)
                    ball = canvas.create_oval(ball_left_x, 0, ball_left_x + BALL_RADIUS*2, 0 + BALL_RADIUS*2, "green")
                    
                    score = 0
                    speed = 0
                    game = "ON"
            
            
        elif paddle_top_x <= (ball_top_x + BALL_RADIUS)*USER_ERROR_MARGIN and (paddle_top_x + PADDLE_WIDTH)*USER_ERROR_MARGIN >= ball_top_x + BALL_RADIUS and ball_top_y + BALL_RADIUS == paddle_top_y:
            canvas.delete(ball)
            ball_left_x = random.randint(0, CANVAS_WIDTH - BALL_RADIUS*2)
            ball = canvas.create_oval(ball_left_x, 0, ball_left_x + BALL_RADIUS*2, 0 + BALL_RADIUS*2, "green")
            if score > 0:
                canvas.delete(game_score)
            score += 1
            
            if score > 15 and score < 50:
                PADDLE_WIDTH = 60
                canvas.delete(paddle)
                paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_top_x + PADDLE_WIDTH, paddle_bottom_y, "midnightblue")
            if score > 2 and score < random.randint(5,21):
                speed = random.uniform(0.042, 0.048)	
            elif score > 20 and score < random.randint(30,40):
                speed = random.uniform(0.045, 0.049)
            elif score > 40:
                speed = 0.047
            elif score > 50 and score < 100:
                speed = random.uniform(0.047, 0.049)
                PADDLE_WIDTH = BALL_RADIUS*3
                canvas.delete(paddle)
                paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_top_x + PADDLE_WIDTH, paddle_bottom_y, "lightsteelblue")
            elif score > 100:
                speed = 0.049
                PADDLE_WIDTH = BALL_RADIUS*2
                canvas.delete(paddle)
                paddle = canvas.create_rectangle(paddle_top_x, paddle_top_y, paddle_top_x + PADDLE_WIDTH, paddle_bottom_y, "silver")
            else:
                speed = 0
            game_score = canvas.create_text(10, 10, text='Score: ' + str(score))


def high_scores(canvas, score):
    #SHOWS TOP 5 SCORES
    #get the last score
    #check if there is more than 5 scores
    #if there is more than 5 scores, shows only top 5
    #sorts max 5 score values
    #create text blocks on the canvas
    
    scores.append(score)
    size_of_score = len(scores)
    scores.sort(reverse=True)

    
    high_score_text = canvas.create_text(CANVAS_WIDTH - (FONT_SIZE * 7), 10, font_size = int(FONT_SIZE), text='High Scores', color = "green")
    if size_of_score > 4:
        for i in range (5):
            high_score = canvas.create_text(CANVAS_WIDTH - (FONT_SIZE * 7), 10 + (i+1)*(int(FONT_SIZE) + 5), text= str(i+1) + '............ ' + str(scores[i]))
    else:
        for i in range (size_of_score):
            high_score = canvas.create_text(CANVAS_WIDTH - (FONT_SIZE * 7), 10 + (i+1)*(int(FONT_SIZE) + 5), text= str(i+1) + '............ ' + str(scores[i]))

    

if __name__ == '__main__':
    main()
