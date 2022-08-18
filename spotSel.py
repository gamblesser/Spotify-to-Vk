from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from vk_txt_to_playlistmain import main
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import configparser
import winshell

url = input('Введите полную ссылку на плейлист spotify\n')

def getSongsFromSpotify(url):
	cfg = configparser.ConfigParser()
	path = 'config.cfg'
	print(path)
	cfg.read(path,encoding='utf-8')
	#print([i for i in cfg.keys()])
	print(cfg['CONFIG']['PROXY'])
	proxy_ip_port =cfg['CONFIG']['PROXY']
	PathToChromeWebDriver =cfg['CONFIG']['PATH_TO_CHROME_WEBDRIVER']
	proxy = Proxy()
	proxy.proxy_type = ProxyType.MANUAL
	proxy.http_proxy = proxy_ip_port
	proxy.ssl_proxy = proxy_ip_port
	capabilities = webdriver.DesiredCapabilities.CHROME
	proxy.add_to_capabilities(capabilities)
	options = Options()
	options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
		"Chrome/93.0.4577.63 Safari/537.36")
	options.add_argument("--disable-blink-features=AutomationControlled")
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option("useAutomationExtension", False)
	options.add_argument('headless')


	with webdriver.Chrome(PathToChromeWebDriver,options=options, desired_capabilities=capabilities) as driver:
		driver.get(url)
		sleep(10)
		title = driver.find_element(By.XPATH,'//span//h1').text
		songs=driver.find_element(By.XPATH,'//div[@role="presentation"][2]')
		songCursor = 2
		height = 0
		theEnd=False
		notFound= False
		maxHeight= driver.execute_script("return document.getElementsByClassName('os-viewport')[0].scrollHeight")
		listForYoutube=[]
		listForYandex=[]
		while True:
			try:
				songs.find_element(By.XPATH,f'//div[@aria-rowindex="{songCursor}"]')
			except:
				notFound=True
			
			if notFound:
				while True:
					if theEnd:
						return listForYoutube,listForYandex,title
					if height+400>=maxHeight:
						theEnd =True
						height=maxHeight
						break
					height+=400
					driver.execute_script(f"document.getElementsByClassName('os-viewport')[0].scrollTo(0,{height})")
					sleep(2)
					songs=driver.find_element(By.XPATH,'//div[@role="presentation"][2]')
					try:
						songs.find_element(By.XPATH,f'//div[@aria-rowindex="{songCursor}"]')

					except:
						
						continue
					notFound=False
					break
			try:
				listForYoutube.append(' - '.join([title.text.replace('\n','').strip() for title in songs.find_elements(By.XPATH,f'//div[@aria-rowindex="{songCursor}"]//div[@aria-colindex="2"]/div//*[self::div or self::a]')[::-1] if title.text.replace('\n','').strip()]))
				listForYandex.append(' - '.join([title.text.replace('\n','').strip() for title in songs.find_elements(By.XPATH,f'//div[@aria-rowindex="{songCursor}"]//div[@aria-colindex="2"]/div//*[self::div or self::a]') if title.text.replace('\n','').strip()]))
				print(listForYandex,'\n',len(listForYandex))
			except Exception as e:
				print(e)
				return listForYoutube,listForYandex,title
			songCursor+=1



songsForYoutube,songsForYandex,title = getSongsFromSpotify(url)
with open(f'{winshell.desktop()}\\{title}.txt', 'w', encoding="utf-8") as fp:
	for song in songsForYoutube:

		fp.write(f"{song}\n")

with open(f'{winshell.desktop()}\\{title}_ForYandex.txt', 'w', encoding="utf-8") as fp:
	for song in songsForYandex:

		fp.write(f"{song}\n")




sleep(10)
process = main.Process(title)
process.main()