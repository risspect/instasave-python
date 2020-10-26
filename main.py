from datetime import datetime
from tqdm import tqdm
import requests
import re, sys, time, os

#Banner
os.system("clear")
logo = '''
       ____           __        _____
      /  _/___  _____/ /_____ _/ ___/____ __   _____  _____
      / // __ \/ ___/ __/ __ `/\__ \/ __ `/ | / / _ \/ ___/
    _/ // / / (__  ) /_/ /_/ /___/ / /_/ /| |/ /  __/ /
   /___/_/ /_/____/\__/\__,_//____/\__,_/ |___/\___/_/ v1.0
'''
about = '''💡 Creator : Risna Fadillah
💡 Version : 1.0 BETA
💡 Website : https://risnfd.asia
💡 Email   : email@risnfd.asia /
             risnafadillah08@gmail.com
💡 Donate  : https://saweria.co/risnfd
             https://trakteer.id/risnfd
'''

#Function to check the internet connection
#Got this from https://stackoverflow.com/a/24460981
def connection(url='http://www.google.com/', timeout=5):
    print(logo)
    print(about)
    try:
        anim = "🌕🌖🌗🌘🌑🌒🌓🌔"
        for i in range(100):
            time.sleep(0.1)
            sys.stdout.write("\r" + anim[i % len(anim)] + " Connecting..")
            sys.stdout.flush()
        req = requests.get(url, timeout=timeout)
        req.raise_for_status()
        print("\r✅ Great! Let's do it\n")
        return True
    except requests.HTTPError as e:
        print("\r❎ Checking internet connection failed, status code {0}.".format(
        e.response.status_code))
    except requests.ConnectionError:
        print("\r❎ No internet connection available.")
    return False

#Function to download an instagram photo or video
def download_image_video():
    os.system("clear")
    print(logo)
    print("Your choice is  Post Downloader")
    url = input("⛓️ Enter Post URL: ")
    x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)

    try:
        if x:
            request_image = requests.get(url)
            src = request_image.content.decode('utf-8')
            check_type = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
            check_type_f = check_type.group()
            final = re.sub('<meta name="medium" content="', '', check_type_f)

            if final == "image":
                print("\nDownloading the image...")
                extract_image_link = re.search(r'meta property="og:image" content=[\'"]?([^\'" >]+)', src)
                image_link = extract_image_link.group()
                final = re.sub('meta property="og:image" content="', '', image_link)
                _response = requests.get(final).content
                file_size_request = requests.get(final, stream=True)
                file_size = int(file_size_request.headers['Content-Length'])
                block_size = 1024
                filename = input("Filename: ")
                t=tqdm(total=file_size, unit='B', unit_scale=True, desc=filename + '.jpg', ascii=True)
                with open(filename + '.jpg', 'wb') as f:
                    for data in file_size_request.iter_content(block_size):
                        t.update(len(data))
                        f.write(data)
                t.close()
                print("✅ Image successfully downloaded")

            if final == "video":
                msg = input("You're trying to download a video. Continue? (y/N): ".lower())

                if msg == "y":
                    print("Downloading the video...")
                    extract_video_link = re.search(r'meta property="og:video" content=[\'"]?([^\'" >]+)', src)
                    video_link = extract_video_link.group()
                    final = re.sub('meta property="og:video" content="', '', video_link)
                    _response = requests.get(final).content
                    file_size_request = requests.get(final, stream=True)
                    file_size = int(file_size_request.headers['Content-Length'])
                    block_size = 1024 
                    filename = input("Filename: ")
                    t=tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
                    with open(filename + '.mp4', 'wb') as f:
                        for data in file_size_request.iter_content(block_size):
                            t.update(len(data))
                            f.write(data)
                    t.close()
                    print("✅ Video successfully downloaded")

                if msg == "n":
                    exit()
        else:
            print("Entered URL is not an instagram.com URL.")
    except AttributeError:
        print("Unknown URL")

#Function to download profile picture of instagram accounts
def pp_download():
    os.system("clear")
    print(logo)
    print("Your choice is  Profile Image Downloader")
    url = input("⛓️ Enter Profile URL: ")
    x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)
    
    if x:
        check_url1 = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com[/].*\?hl=[a-z-]{2,5}', url)
        check_url2 = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com$|^(https:)[/][/]www.([^/]+[.])*instagram.com/$', url)
        check_url3 = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com[/][a-zA-Z0-9_]{1,}$', url)
        check_url4 = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com[/][a-zA-Z0-9_]{1,}[/]$', url)

        if check_url3:
            final_url = url + '/?__a=1'

        if check_url4:
            final_url = url + '?__a=1'

        if check_url2:
            final_url = print("Please enter an URL related to a profile")
            exit()

        if check_url1:
            alpha = check_url1.group()
            final_url = re.sub('\\?hl=[a-z-]{2,5}', '?__a=1', alpha)
            
    try:
        if check_url3 or check_url4 or check_url2 or check_url1:
            req = requests.get(final_url)
            get_status = requests.get(final_url).status_code
            get_content = req.content.decode('utf-8')

            if get_status == 200:
                print("\nDownloading the image...")
                find_pp = re.search(r'profile_pic_url_hd\":\"([^\'\" >]+)', get_content)
                pp_link = find_pp.group()
                pp_final = re.sub('profile_pic_url_hd":"', '', pp_link)
                file_size_request = requests.get(pp_final, stream=True)
                file_size = int(file_size_request.headers['Content-Length'])
                block_size = 1024 
                filename = input("Filename: ")
                t=tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
                with open(filename + '.jpg', 'wb') as f:
                    for data in file_size_request.iter_content(block_size):
                        t.update(len(data))
                        f.write(data)
                t.close()
                print("✅ Profile picture successfully downloaded")

    except Exception:
        print('error')

if connection() == True:
    try:
        while True:
            a = '''[1] - Download Profile Image
[2] - Download Image/Video Post
[3] - About
[0] - Exit'''
            print(a)
            select = str(input("\nInput > ")).upper()
            try:
                if select == '1':
                    pp_download()
                if select == '2':
                    download_image_video()
                if select == '3':
                    about()
                if select == '0':
                    sys.exit()
                else:
                    sys.exit()
            except (KeyboardInterrupt):
                 print("Program Interrupted")
    except(KeyboardInterrupt):
        print("\nProgram Interrupted")
else:
    sys.exit()
