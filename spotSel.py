from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from time import sleep
from vk_txt_to_playlistmain import main
import configparser
import winshell

class CollectTrecksFromSpotify:


	def __init__(self,config='config.cfg',options=None):
		if options == None:
			options = Options()
			options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
			"Chrome/93.0.4577.63 Safari/537.36")
			options.add_argument("--disable-blink-features=AutomationControlled")
			options.add_experimental_option("excludeSwitches", ["enable-automation"])
			options.add_experimental_option("useAutomationExtension", False)
			#options.add_argument('headless')

		self.url=url
		self.listForYoutube=[]
		self.listForYandex=[]

		cfg = configparser.ConfigParser()
		path = config
		cfg.read(path,encoding='utf-8')
		proxy_ip_port =cfg['CONFIG']['PROXY']
		self.pathToChromeWebDriver =cfg['CONFIG']['PATH_TO_CHROME_WEBDRIVER']

		self.options = options

		proxy = Proxy()
		proxy.proxy_type = ProxyType.MANUAL
		proxy.http_proxy = proxy_ip_port
		proxy.ssl_proxy = proxy_ip_port
		self.capabilities = webdriver.DesiredCapabilities.CHROME
		proxy.add_to_capabilities(self.capabilities)


	def __call__(self,url):
		self.browser = webdriver.Chrome(self.pathToChromeWebDriver,options=self.options,desired_capabilities=self.capabilities)
		self.getSongsFromSpotify()
		self.__writeToFile()
		self.browser.quit()
		return self.title


	def getSongsFromSpotify(self):
		songCursor = 2
		height = 0
		theEnd=False
		notFound= False

		self.browser.get(self.url)

		self.title =self.__find_element('//span/h1').text

		songs=self.__find_element('//div[@role="presentation"][2]')

		maxHeight= self.browser.execute_script("return document.getElementsByClassName('os-viewport')[0].scrollHeight")

		while True:
			try:

				self.__find_element(f'//div[@aria-rowindex="{songCursor}"]',songs,timeout=2)

			except:
				notFound=True
			
			if notFound:
				while True:
					if theEnd:
						print("All uploads trecks:")
						print('\n'.join(self.listForYoutube))
						print("Length: ",len(self.listForYoutube))

						return self.listForYoutube,self.listForYandex,self.title

					if height+400>=maxHeight:
						theEnd =True
						height=maxHeight
						break

					height+=400

					self.browser.execute_script(f"document.getElementsByClassName('os-viewport')[0].scrollTo(0,{height})")
					songs=self.__find_element('//div[@role="presentation"][2]',timeout=2)

					try:
						self.__find_element(f'//div[@aria-rowindex="{songCursor}"]',songs,timeout=2)

					except:
						continue

					notFound=False
					break
			try:

				self.listForYoutube.append(' - '.join([title.text.replace('\n','').strip() for title in songs.find_elements(By.XPATH,f'//div[@aria-rowindex="{songCursor}"]//div[@aria-colindex="2"]/div//*[self::div or self::a]')[::-1] if title.text.replace('\n','').strip()]))
				self.listForYandex.append(' - '.join([title.text.replace('\n','').strip() for title in songs.find_elements(By.XPATH,f'//div[@aria-rowindex="{songCursor}"]//div[@aria-colindex="2"]/div//*[self::div or self::a]') if title.text.replace('\n','').strip()]))
			
			except:
				print("All uploads trecks:")
				print('\n'.join(self.listForYoutube))
				print("Length: ",len(self.listForYoutube))

				return self.listForYoutube,self.listForYandex,self.title

			songCursor+=1



	def __writeToFile(self):

		with open(f'{winshell.desktop()}\\{self.title}.txt', 'w', encoding="utf-8") as fp:
			for song in self.listForYoutube:

				fp.write(f"{song}\n")

		with open(f'{winshell.desktop()}\\{self.title}_ForYandex.txt', 'w', encoding="utf-8") as fp:
			for song in self.listForYandex:

				fp.write(f"{song}\n")


	def __find_element(self, xpath: str,node=None, timeout: int = 15) -> WebElement or None:
		try:
			node = self.browser
			if node:
				node =node
			element = WebDriverWait(node, timeout).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
			return element
		except TimeoutException:
			raise TimeoutException



if __name__ == '__main__':
	url = input('Enter full spotify url\n')
	print("Collect trecks from spotify")
	title= CollectTrecksFromSpotify()(url)
	print('Import To VK')
	main.Process(title).main()