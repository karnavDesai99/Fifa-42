from settings import *
from const import ACT, FORM
from teams.agent import Agent
from teams.team import Team

class HumanAgent(Agent):
    """ Agents controlled by humans """
    def draw(self, win, team_id, selected=False, debug=False):
        if debug:
            pygame.draw.rect(win, (255,255,255), (self.pos.x-PLAYER_RADIUS, self.pos.y-PLAYER_RADIUS,PLAYER_RADIUS*2,PLAYER_RADIUS*2))
        if selected:
            pygame.draw.circle(win, (255, 0, 0), (self.pos - P(0,1.5)*P(0,PLAYER_RADIUS)).val, 5) # mid circle
        win.blit(RUN[team_id][self.walk_dir][self.walk_count//WALK_DELAY], (self.pos - PLAYER_CENTER).val)

    def move(self, state, reward):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            return 'SHOOT_A'
        elif keys[pygame.K_d]:
            return 'SHOOT_D'
        elif keys[pygame.K_w]:
            return 'SHOOT_W'
        elif keys[pygame.K_x]:
            return 'SHOOT_X'
        elif keys[pygame.K_q]:
            return 'SHOOT_Q'
        elif keys[pygame.K_c]:
            return 'SHOOT_C'
        elif keys[pygame.K_e]:
            return 'SHOOT_E'
        elif keys[pygame.K_z]:
            return 'SHOOT_Z'
        elif keys[pygame.K_LEFT]:
            return 'MOVE_L'
        elif keys[pygame.K_RIGHT]:
            return 'MOVE_R'
        elif keys[pygame.K_UP]:
            return 'MOVE_U'
        elif keys[pygame.K_DOWN]:
            return 'MOVE_D'
        else:
            return 'NOTHING'

class HumanTeam(Team):
    """A team of human players"""
    def draw(self,win, debug=False):
        for i,player in enumerate(self.players):
            if i == self.selected:
                player.draw(win, team_id=self.id, selected=True, debug=debug)
            else:
                player.draw(win, team_id=self.id, debug=debug)

    def update(self, action, ball):
        self.select_player(ball)
        super().update(action,ball)

    def select_player(self, ball):
        """
        Select the player that is controlled by the keyboard
            - If ball is near the D-area, keeper gets automatic control
            - Otherwise the player nearest to the ball has control (ties are broken randomly)
        """
        dists = [player.pos.dist(ball.pos) + player.rnd for player in self.players]
        self.selected = np.argmin(dists) # Default - Ball goes to nearest player

        if min(dists) > PLAYER_RADIUS + BALL_RADIUS and abs(ball.pos.x - self.goal_x) < W//5:
            # If the ball is within the D and is not very near to any other player, give control to the keeper
            self.selected = 0


    def set_players(self):
        self.players = []
        for i in range(NUM_TEAM):
            self.players.append(HumanAgent(id=i, team_id=self.id, pos=FORM[self.formation][self.dir][i]))

        self.selected = NUM_TEAM//2

    def formation_dir(self, id):
        """ Send player with given id to his designated place in the formation """
        player = self.players[id]
        min_dist = 2

        """
        If player is in-line (horizontally or vertically), move directly towards original point (U/L/D/R)
        Otherwise choose 2 directions that take you closer to the original point and choose one of them randomly (UL/UR/DL/DR)
        """
        if abs(player.pos.x - FORM[self.formation][self.dir][id].x) <= min_dist and abs(player.pos.y - FORM[self.formation][self.dir][id].y) <= min_dist:
            player.walk_count = 0
            return 'NOTHING'
        elif abs(player.pos.x - FORM[self.formation][self.dir][id].x) <= min_dist:
            if (player.pos.y - FORM[self.formation][self.dir][id].y) > min_dist:
                return 'MOVE_U'
            else:
                return 'MOVE_D'
        elif abs(player.pos.y - FORM[self.formation][self.dir][id].y) <= min_dist:
            if (player.pos.x - FORM[self.formation][self.dir][id].x) > min_dist:
                return 'MOVE_L'
            else:
                return 'MOVE_R'
        elif (player.pos.x - FORM[self.formation][self.dir][id].x) > min_dist:
            if (player.pos.y - FORM[self.formation][self.dir][id].y) > min_dist:
                return np.random.choice(['MOVE_L', 'MOVE_U'])
            else:
                return np.random.choice(['MOVE_L', 'MOVE_D'])
        elif (player.pos.x - FORM[self.formation][self.dir][id].x) < - min_dist:
            if (player.pos.y - FORM[self.formation][self.dir][id].y) > min_dist:
                return np.random.choice(['MOVE_R', 'MOVE_U'])
            else:
                return np.random.choice(['MOVE_R', 'MOVE_D'])
        else:
            return 'NOTHING'

    def move(self, state, reward):
        """
        Move a human team
            * Player nearest to the ball moves through keyboard
            * All other players return to their original positions (if maintain_formation is set)
        """
        actions = []
        for i,player in enumerate(self.players):
            if i == self.selected:
                actions.append(player.move(state, reward))
            elif self.maintain_formation:
                actions.append(self.formation_dir(i))
            else:
                player.walk_count = 0
                actions.append('NOTHING')
        return actions