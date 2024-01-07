from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from pathlib import Path
import sys, time, random
from datetime import datetime
from rich.prompt import Prompt

class RandomizedVideoTimer():
    def __init__(self, url : str, minimum_range_sec : int, maximum_range_sec : int, optional_addons: tuple = ()):
        self.url = url
        self.minimum_range_sec = int(minimum_range_sec)
        self.maximum_range_sec = int(maximum_range_sec)

        self.w_driver = webdriver.Firefox()

        if optional_addons:
            self.addon_path = Path.cwd() / "addons"
            [self.w_driver.install_addon(addon) for addon in self.addon_path.glob("*.xpi")]

        
    
    def load_video(self):
        try:
            self.w_driver.get(self.url)
            self.w_driver.minimize_window()

            self.timeout_error = 10
            self.video_element = WebDriverWait(self.w_driver, self.timeout_error).until(EC.presence_of_element_located((By.ID, 'movie_player')))
            self.video_title = WebDriverWait(self.w_driver, self.timeout_error).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title.style-scope.ytd-video-primary-info-renderer > yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).get_attribute("innerHTML")
            self.duration = int(self.w_driver.execute_script("return document.getElementById('movie_player').getDuration()"))

        except TimeoutException:
            print("Video took too long to load", file=sys.stderr)

        except InvalidArgumentException:
            print("Incorrect URL", file=sys.stderr)

    def video_randomization(self):
        begin_randomized_video = Prompt.ask(f"[{self.video_title}] Start the video?", choices=['Y', 'N'])

        if begin_randomized_video.upper() == 'Y':
            while True:
                self.video_element.send_keys('K')

                random.seed(datetime.now().timestamp())
                self.current_wait_time = random.randint(self.minimum_range_sec, self.maximum_range_sec)
                print(f'Stopping in {self.current_wait_time} seconds')
                
                time.sleep(self.current_wait_time)

                self.current_time = int(self.w_driver.execute_script("return document.getElementById('movie_player').getCurrentTime()"))
                if self.current_time >= self.duration:
                    self.w_driver.close()
                    break

                self.video_element.send_keys('K')

                if not Prompt.ask("Do you want to continue? ", choices=['Y', 'N']) == 'Y':
                    self.w_driver.close()
                    break

        else:
            print('Exiting...')
            self.w_driver.close()