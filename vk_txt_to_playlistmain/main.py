import os
import time
import configparser
from datetime import timedelta
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import winshell

cfg = configparser.ConfigParser()
path = 'config.cfg'
cfg.read(path,encoding='utf-8')
USERNAME = cfg['CONFIG']['USERNAME']
PASSWORD = cfg['CONFIG']['PASSWORD']
EXEPTWORDS = cfg['CONFIG']['EXEPTWORDS'].split(',')
PathToChromeWebDriver =cfg['CONFIG']['PATH_TO_CHROME_WEBDRIVER']
class Process:
    def __init__(self, file_name):
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/93.0.4577.63 Safari/537.36"
        )
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        #options.add_argument('headless')
        self.browser = webdriver.Chrome(PathToChromeWebDriver,options=options)
        self.url = 'https://vk.com/'
        self.username = USERNAME
        self.password = PASSWORD
        self.timeout = timedelta(seconds=30)
        self.song_list = []
        self.file_name = file_name
        self.counter = 0
        self.count = 0
        self.notFoundSongs = set()
        self.skip_song_con=False

    def main(self):
        self.get_song_list()
        self.login()
        #self.go_to_music()
        self.new_playlist()
        self.add_songs()

    def get_song_list(self):
        file_path = os.path.join(os.path.join(os.path.join
                                              (os.environ['USERPROFILE']), 'Desktop'), f'{self.file_name}.txt')

        with open(file_path, encoding='utf-8') as f:
            for i in f:

                print(i)
                if i:
                    self.song_list.append(i)

        print(f'Found {len(self.song_list)} songs!')

    def login(self):
        self.browser.get(self.url)

        start_login_button = '//*[@id="index_login"]/div/form/button[1]'
        start_login_button_element = self.__find_element(xpath=start_login_button)
        start_login_button_element.click()

        username_input = "//input[@name='login']"
        username_input_element = self.__find_element(xpath=username_input)
        username_input_element.send_keys(self.username)

        username_login_button = '//button[@class="FlatButton FlatButton--primary FlatButton--size-l FlatButton--wide VkIdForm__button VkIdForm__signInButton"]'
        username_login_button_element = self.__find_element(xpath=username_login_button)
        username_login_button_element.click()

        password_input = "//input[@name='password']"
        password_input_element = self.__find_element(password_input, timeout=20)
        password_input_element.send_keys(self.password)

        password_login_button = "//button[@type='submit']"
        password_login_button_element = self.__find_element(xpath=password_login_button)
        password_login_button_element.click()

    def go_to_music(self):
        pass

    
    def new_playlist(self):
        playlist_button = '//li[@id="l_aud"]//a'
        time.sleep(10)
        playlist_button_element = self.__find_element(playlist_button)
        playlist_button_element.click()
        playlist_button_element.click()

        playlist_button = '//*[@id="content"]/div/div[3]/div[1]/h2/ul/button[2]'
        playlist_button_element = self.__find_element(playlist_button)
        playlist_button_element.click()

        playlist_name = "//input[@id='ape_pl_name']"
        playlist_name_element = self.__find_element(playlist_name)
        playlist_name_element.send_keys(self.file_name)
        save_playlist = "//button[@class='FlatButton FlatButton--primary FlatButton--size-m']"
        save_playlist_element = self.__find_element(save_playlist)
        save_playlist_element.click()
        music_button = '/html/body/div[11]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[3]/div[1]/h2/ul/li[2]/a'
        music_button_element = self.__find_element(music_button)
        music_button_element.click()
        #music_button = '/html/body/div[11]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[3]/div[2]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/a/div[3]/div[1]/div[2]'
        #music_button_element = self.__find_element(music_button)
        #music_button_element.click()      
        self.add_songs()
        time.sleep(5)
        self.browser.quit()
    def add_songs(self):
        song_search = '//input[@id="ape_edit_playlist_search"]'
        #song_cursor = 0
        while self.counter != len(self.song_list) :
            self.count=0
            for i in range(1):

                if self.count==0:
                    try:
                        #time.sleep(3)
                    
                        music_button = '/html/body/div[11]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/a/div[3]/div[1]/div[2]'
                        music_button = '/html/body/div[11]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[3]/div[2]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/a/div[3]/div[1]/div[2]'
                        music_button_element = self.__find_element(music_button)
                        music_button_element.click()
                    except:
                        time.sleep(3)
                        music_button = '/html/body/div[11]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/a/div[3]/div[1]/div[2]'
                        music_button = '/html/body/div[11]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[3]/div[2]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/a/div[3]/div[1]/div[2]'
                        music_button_element = self.__find_element(music_button)
                        music_button_element.click()
            try:
                nums = [int(i) for i in re.findall(r'\d+',self.__find_element('/html/body/div[7]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[4][text()]').text)]
                if (self.counter!=nums[0]+len(self.notFoundSongs)) and not(self.skip_song_con):
                    self.counter=nums[0]+len(self.notFoundSongs)

            except Exception as e:
                pass           


            try:
                song_search = '//*[@id="ape_edit_playlist_search"]'
                song_search_element = self.__find_element(xpath=song_search)
                self.song_list[self.counter] = self.song_list[self.counter].replace('*',' ')
                song_search_element.send_keys(self.song_list[self.counter])
                if self.__find_element(xpath='//div[@class="ape_check--checked"]').is_displayed():
                    self.counter += 1
                    self.skip_song_con=True
                    song_search_element.clear()
                    save_playlist = "//button[@class='FlatButton FlatButton--primary FlatButton--size-m']"
                    save_playlist_element = self.__find_element(save_playlist)
                    save_playlist_element.click()
                    continue

                found_song_list = '//*[@id="box_layer"]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]'
                found_song_list_element = self.__find_element(found_song_list)

                found_song_list_element.click()
                #time.sleep(4)
                self.counter += 1
                self.skip_song_con=False
            except:
                try:
                    song_vr = self.song_list[self.counter].lower()
                    for exeptWord in EXEPTWORDS:
                        song_vr = song_vr.replace(exeptWord,'')
                    song_search_element.clear()
                    song_search_element = self.__find_element(xpath=song_search)
                    song_search_element.send_keys(song_vr)
                    if self.__find_element(xpath='//div[@class="ape_check--checked"]').is_displayed():
                        self.counter += 1
                        self.skip_song_con=True
                        song_search_element.clear()
                        save_playlist = "//button[@class='FlatButton FlatButton--primary FlatButton--size-m']"
                        save_playlist_element = self.__find_element(save_playlist)
                        save_playlist_element.click()
                        continue
                    found_song_list = '//*[@id="box_layer"]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]'
                    found_song_list_element = self.__find_element(found_song_list)
                    found_song_list_element.click()
                    self.counter+=1
                    self.skip_song_con=False
                except:
                    self.notFoundSongs.add(self.song_list[self.counter])
                    print(f'Can\'n add {self.song_list[self.counter]}')
                    #self.notFoundCounter.append(self.song_list[self.counter])
                    self.counter+=1
                    self.skip_song_con=False

            song_search_element.clear()
            save_playlist = "//button[@class='FlatButton FlatButton--primary FlatButton--size-m']"
            save_playlist_element = self.__find_element(save_playlist)
            save_playlist_element.click()

        print(f'\n\n____Added {len(self.song_list)} songs!!____')
        with open(f'{winshell.desktop()}\\notFound_{self.file_name}.txt','w', encoding='utf-8') as fp:
            fp.write('\n'.join(self.notFoundSongs))

    def __find_element(self, xpath: str, timeout: int = 10) -> WebElement or None:
        try:
            element = WebDriverWait(self.browser, timeout).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except TimeoutException:
            return None


if __name__ == '__main__':
    process = Process(FILE_NAME)
    process.main()
