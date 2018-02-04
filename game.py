import numpy as np
import time

class Game:

    def __init__(self, vision, controller):
        self.vision = vision
        self.controller = controller
        self.state = 'not started'

    def run(self):
        while True:
            self.vision.refresh_frame()
            if self.state == 'not started' and self.round_starting('bison'):
                print('Round needs to be started, launching bison')
                self.launch_player('bison')
                self.state = 'started'
            if self.state == 'not started' and self.round_starting('pineapple'):
                print('Round needs to be started, launching pineapple')
                try:
                    self.launch_player('pineapple')
                    self.state = 'started'
                except Exception as ex:
                    print('Failed to find pineapple character')
            elif self.state == 'started' and self.found_pinata():
                print('Found a pinata, attempting to skip')
                self.click_cancel()
            elif self.state == 'started' and self.round_finished():
                print('Round finished, clicking to continue')
                self.click_to_continue()
                self.state = 'mission_finished'
            elif self.state == 'started' and self.has_full_rocket():
                print('Round in progress, has full rocket, attempting to use it')
                self.use_full_rocket()
            elif self.state == 'mission_finished' and self.can_start_round():
                print('Mission finished, trying to restart round')
                self.start_round()
                self.state = 'not started'
            else:
                print('Not doing anything')
            time.sleep(1)

    def round_starting(self, player):
        matches = self.vision.find_template('%s-health-bar' % player)
        return np.shape(matches)[1] >= 1

    def launch_player(self, player):
        matches = self.vision.scaled_find_template('left-goalpost', threshold=0.75, scales=[1.05, 1.04, 1.03, 1.02, 1.01, 1.0, 0.99, 0.98, 0.97, 0.96, 0.95])
        print(matches)
        x = matches[1][0]
        y = matches[0][0]

        self.controller.left_mouse_drag(
            (x, y),
            (x-200, y+30)
        )

        time.sleep(0.5)

    def round_finished(self):
        matches = self.vision.find_template('tap-to-continue')
        return np.shape(matches)[1] >= 1

    def click_to_continue(self):
        matches = self.vision.find_template('tap-to-continue')

        x = matches[1][0]
        y = matches[0][0]

        self.controller.move_mouse(x+50, y+30)
        self.controller.left_mouse_click()

        time.sleep(0.5)

    def can_start_round(self):
        matches = self.vision.find_template('next-button')
        return np.shape(matches)[1] >= 1

    def start_round(self):
        matches = self.vision.find_template('next-button')

        x = matches[1][0]
        y = matches[0][0]

        self.controller.move_mouse(x+100, y+30)
        self.controller.left_mouse_click()

        time.sleep(0.5)

    def has_full_rocket(self):
        matches = self.vision.find_template('full-rocket', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def use_full_rocket(self):
        matches = self.vision.find_template('full-rocket')

        x = matches[1][0]
        y = matches[0][0]

        self.controller.move_mouse(x, y)
        self.controller.left_mouse_click()

        time.sleep(0.5)

    def found_pinata(self):
        matches = self.vision.find_template('filled-with-goodies', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def click_cancel(self):
        matches = self.vision.find_template('cancel-button')

        x = matches[1][0]
        y = matches[0][0]

        self.controller.move_mouse(x, y)
        self.controller.left_mouse_click()

        time.sleep(0.5)