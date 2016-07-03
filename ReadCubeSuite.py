#!/usr/bin/env python
import ConfigParser
from webdriverwrapper import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from time import time, sleep
import multiprocessing
import zmq
from render_notes import render_notes
import sys

# loading config
parser = ConfigParser.SafeConfigParser()
parser.read('settings.ini')

user = parser.get('auth', 'user')
pw = parser.get('auth', 'password')
user_id = parser.get('auth', 'user_id')

# setting up queue:
port = "tcp://127.0.0.1:5680"
# publisher
context = zmq.Context()
sender = context.socket(zmq.PUB)
sender.bind(port)


def setup_chromedriver(mode):
    # configuring chromedriver:
    # my screen res: 1366*768:

    # activate for verbose logging:
    # service_log_path = "chromedriver.log"
    # service_args = ['--verbose']



    chrome_options = Options()

    if mode is 'primary':
        chrome_options.add_argument("--restore-last-session")
        chrome_options.add_argument("user-data-dir=master_profile")
        chrome_options.add_argument("--window-size={},{}".format(1000, 800))
        chrome_options.add_argument("--window-position={},{}".format(1, 1))

    elif mode is 'tertiary':
        chrome_options.add_argument("--window-size={},{}".format(200, 800))
        chrome_options.add_argument("--window-position={},{}".format(1050, 1))

    # get rid off: --ignore-certificate-errors command-line flag warning:
    chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    chrome_options.add_argument("--disable-infobars")  # add command line flags

    chrome = Chrome(chrome_options=chrome_options,
                    # service_args=service_args,
                    # service_log_path=service_log_path
                    )

    # log in if not already:
    if 'readcube.com/session/new' in chrome.current_url and mode is 'primary':
        chrome.get('https://app.readcube.com/#/library/collection/~/items')
        # logging in via email / password
        for i in range(5):
            try:
                sleep(3)
                chrome.find_element_by_id('email').send_keys(user)
                chrome.find_element_by_id('password').send_keys(pw)
                chrome.find_element_by_class_name('submit-button').click()
            except Exception as e:
                sleep(1.5)
                # print e
            else:
                break

    # returns driver:
    return chrome

# 1 - starting main window:
driver = setup_chromedriver(mode='primary')


# 2 - notes_window:
def note_window():
    tert_driver = setup_chromedriver(mode='tertiary')
    tert_driver.get('about:blank')

    # receiver queue for item_ids:
    context3 = zmq.Context()
    sock3 = context3.socket(zmq.SUB)
    sock3.setsockopt(zmq.SUBSCRIBE, "")
    sock3.connect(port)

    poller = zmq.Poller()
    poller.register(sock3, zmq.POLLIN)

    while True:
        # item_id = sock3.recv()
        socks_rec = dict(poller.poll(30))
        if socks_rec:
            if socks_rec.get(sock3) == zmq.POLLIN:
                msg = sock3.recv(zmq.NOBLOCK)
                if msg == 'SENTINEL':
                    print 'Slave received sentinel.'
                    tert_driver.quit()
                    break
                else:
                    item_id = msg
                    print 'Slave received: ', item_id
                    try:
                        txt = open('note_dir/' + item_id + '.html', 'r')
                        source = txt.read()
                        tert_driver.get("data:text/html;charset=utf-8," + source)
                        tert_driver.refresh()  # inelegant but works as troubleshoot
                        tert_driver.execute_script("window.document.title = 'NOTES'")
                        txt.close()
                    except IOError:
                        driver.get('about:blank')

slave = multiprocessing.Process(target=note_window)
slave.start()

# tab issue / other java script ideas:
# https://stackoverflow.com/questions/1760250/how-to-tell-if-browser-tab-is-active  |||| blur and focus
# https://stackoverflow.com/questions/20813760/how-to-find-current-active-tab-id
# https://stackoverflow.com/questions/12336124/how-to-get-active-tab-index-from-tabcontainer
js2 = """if (!document.hidden) {
    return 1;
} else {
    return 0;
}"""

# 3 - item id check loop (main window):
delimiter = 'itemId='
item_id_past = ''
timestamp = 0
sent = False  # Bool to prevent to double send same item_id
notes_source_past = ''
while True:
    try:
        # switch driver to manually opened active tab, as it doesn't do it by itself:
        tabs = []
        tabs = driver.window_handles
        for i, t in enumerate(tabs):
            # print 'i: ', i
            driver.switch_to_window(driver.window_handles[i])
            result = driver.execute_script(js2)
            if result == 1:
                break

        url_now = driver.current_url
        # library view:
        if delimiter in url_now:
            item_id_now = url_now.split(delimiter)[-1]
            if item_id_now != item_id_past:
                item_id_past = item_id_now
                timestamp = time()
                sent = False
            elif item_id_now == item_id_past and time() - timestamp > 0.2 and not sent:
                ''' if item_id remained same for 0.2 sec submit to slave process,
                the short time delay is to prevent opening too many windows when selection
                is just wandering over list of articles '''
                print 'Library view - Sending: ', item_id_now
                sender.send(str(item_id_now))
                sent = True
        # article view:
        elif 'www.readcube.com/library/' in url_now:
            item_id_now = url_now.split(':')[-1]
            try:
                xp = "/html/body/ui-view/div/ng-include[4]"
                notes_source = driver.find_element_by_xpath(xp).get_attribute('innerHTML')
            except:
                pass

            if notes_source != notes_source_past:
                with open('note_dir/' + item_id_now + '.html', 'w') as html_f:
                    html_f.write(render_notes(notes_source))
                print 'html getter refreshed file'
                print 'Article view - Sending: ', item_id_now
                sender.send(str(item_id_now))

            notes_source_past = notes_source

    except (NoSuchWindowException, WebDriverException):
        '''detects closing of window'''
        break

    except Exception as e:
        print e


# closing secondary window:
print 'Sending sentinel'
sender.send('SENTINEL')
sleep(2)
slave.terminate()
sys.exit(0)
