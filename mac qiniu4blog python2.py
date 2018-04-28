#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, sys, ConfigParser, platform, urllib, qiniu, pyperclip, signal, threading
from mimetypes import MimeTypes
from os.path import expanduser
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


# ʹ��watchdog ����ļ����е�ͼ��
class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.jpeg", "*.jpg", "*.png", "*.bmp", "*.gif","*.tiff"]
    ignore_directories = True
    case_sensitive = False
    def process(self, event):
        if event.event_type == 'created'or event.event_type == 'modified': #����������ļ����޸ĵ��ļ�
            myThread(event.src_path, 1).start() # �����߳�
    def on_modified(self, event):
        self.process(event)
    def on_created(self, event):
        self.process(event)


# ʹ�ö��߳��ϴ�
class myThread(threading.Thread):
    def __init__(self, filePath, mode): #filePath �ļ�·�� �� �ϴ�ģʽ
        threading.Thread.__init__(self)
        self.filePath = filePath
        self.mode = mode
    def run(self):
        threadLock.acquire()
        job(self.filePath, self.mode)
        threadLock.release()


# �ϴ�ͼ�񡢸��Ƶ�ճ���塢д���ļ�
def job(file, mode):
    if mode == 1:
        url = upload_with_full_Path(file)
    if mode == 2:
        url = upload_with_full_Path_cmd(file)
    pyperclip.copy(url)
    pyperclip.paste()
    print url
    with open('MARKDOWN_FORMAT_URLS.txt', 'a') as f:
        image = '![]' + '(' + url + ')' + '\n'
        f.write(image + '\n')

#-----------------����--------------------
homedir = expanduser("~")  # ��ȡ�û���Ŀ¼
config = ConfigParser.RawConfigParser()
config.read(homedir + '/qiniu.cfg')  # ��ȡ�����ļ�
mime = MimeTypes()
threadLock = threading.Lock()


# �����˳�
def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)
    signal.signal(signal.SIGINT, exit_gracefully)

original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)

try:
    bucket = config.get('config', 'bucket')  # ����  bucket
    accessKey = config.get('config', 'accessKey')  # ����  accessKey
    secretKey = config.get('config', 'secretKey')  # ����  secretKey
    path_to_watch = config.get('config', 'path_to_watch')  # ����   ����ļ���
    enable = config.get('custom_url', 'enable')  # �����Զ���ʹ�� custom_url
    if enable == 'false':
        print 'custom_url not set'
    else:
        addr = config.get('custom_url', 'addr')
except ConfigParser.NoSectionError, err:
    print 'Error Config File:', err


# ���ñ���
def setCodeingByOS():
    if 'cygwin' in platform.system().lower():
        return 'GBK'
    elif os.name == 'nt' or platform.system() == 'Windows':
        return 'GBK'
    elif os.name == 'mac' or platform.system() == 'Darwin':
        return 'utf-8'
    elif os.name == 'posix' or platform.system() == 'Linux':
        return 'utf-8'


# ������ţ���ؽ��
def parseRet(retData, respInfo):
    if retData != None:
        for k, v in retData.items():
            if k[:2] == "x:":
                print(k + ":" + v)
        for k, v in retData.items():
            if k[:2] == "x:" or k == "hash" or k == "key":
                continue
            else:
                print(k + ":" + str(v))
    else:
        print("Upload file failed!")

# �ϴ��ļ���ʽ 1
def upload_without_key(bucket, filePath, uploadname):
    auth = qiniu.Auth(accessKey, secretKey)
    upToken = auth.upload_token(bucket, key=None)
    key = uploadname
    retData, respInfo = qiniu.put_file(upToken, key, filePath, mime_type=mime.guess_type(filePath)[0])
    parseRet(retData, respInfo)


# �ϴ��ļ���ʽ 2
def upload_with_full_Path(filePath):
    if platform.system() == 'Windows':
        fileName = "/".join("".join(filePath.rsplit(path_to_watch))[1:].split("\\"))
    else:
        fileName = "".join(filePath.rsplit(path_to_watch))[1:]
    upload_without_key(bucket, filePath, fileName.decode(setCodeingByOS()))
    if enable == 'true':
        return '![]('+addr + urllib.quote(fileName.decode(setCodeingByOS()).encode('utf-8'))+')'
    else:
        return 'http://' + bucket + '.qiniudn.com/' + urllib.quote(fileName.decode(setCodeingByOS()).encode('utf-8'))


# �ϴ��ļ���ʽ 3
def upload_with_full_Path_cmd(filePath):
    if platform.system() == 'Windows':
        fileName = os.path.basename("/".join((filePath.split("\\"))))
    else:
       fileName = os.path.basename(filePath)
    upload_without_key(bucket, filePath, fileName.decode(setCodeingByOS()))
    if enable == 'true':
        return addr + urllib.quote(fileName.decode(setCodeingByOS()).encode('utf-8'))
    else:
        return 'http://' + bucket + '.qiniudn.com/' + urllib.quote(fileName.decode(setCodeingByOS()).encode('utf-8'))

#-----------------window platform---------------start
# window�µļ���ļ��б䶯��ʽ-��ȡ�����ļ�·��
def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.
    return file_paths  # Self-explanatory.

def set_clipboard(url_list):
    for url in url_list:
        pyperclip.copy(url)
        spam = pyperclip.paste()

def get_filename(url):
    return url.split("/")[-1:][0].split('.')[0]

def window_main():
    if len(sys.argv) > 1:
        url_list = []
        for i in sys.argv[1:]:
            url_list.append(upload_with_full_Path_cmd(i))
        with open('MARKDOWN_FORMAT_URLS.txt', 'a') as f:
            for url in url_list:
                image = '![]' + '(' + url + ')' + '\n'
                print url, '\n'
                f.write(image)
        print "\nNOTE: THE MARKDOWN FORMAT URLS ALREADY SAVED IN MARKDOWN_FORMAT_URLS.txt FILE"
        set_clipboard(url_list)
        sys.exit(-1)
    print "running ... ... \nPress Ctr+C to Stop"
    before = get_filepaths(path_to_watch)
    while 1:
        time.sleep(1)
        after = get_filepaths(path_to_watch)
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            url_list = []
            for i in added:
                url_list.append(upload_with_full_Path(i))
            with open('MARKDOWN_FORMAT_URLS.txt', 'a') as f:
                for url in url_list:
                    image = '![]' + '(' + url + ')' + '\n'
                    print url, '\n'
                    f.write(image)
            print "\nNOTE: THE MARKDOWN FORMAT URLS ALREADY SAVED IN MARKDOWN_FORMAT_URLS.txt FILE"
            set_clipboard(url_list)
        if removed:
            pass
        before = after


def unix_main():
    if len(sys.argv) > 1:
        url_list = []
        for i in sys.argv[1:]:
            url_list.append(upload_with_full_Path_cmd(i))
            fileFullName = os.path.basename("/".join((i.split("\\"))))
            fileName = os.path.splitext(fileFullName)[0]
            myThread(i, 2).start()
        with open('MARKDOWN_FORMAT_URLS.txt', 'a') as f:
            for url in url_list:
                image = '![]' + '(' + url + ')' + '\n'
                print 'Url:'+image, '\nFileName:'+fileFullName
                f.write(image)
  set_clipboard(url_list)
        sys.exit(-1)
    print "running ... ... \nPress Ctr+C to Stop"
    observer = Observer()
    observer.schedule(MyHandler(), path=path_to_watch if path_to_watch else '.', recursive=True)
    observer.start()
    before = get_filepaths(path_to_watch)
    while 1:
        time.sleep(1)
        after = get_filepaths(path_to_watch)
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            url_list = []
            for i in added:
                url_list.append(upload_with_full_Path(i))
              fileFullName = os.path.basename("/".join((i.split("\\"))))
                fileName = os.path.splitext(fileFullName)[0]
      with open('MARKDOWN_FORMAT_URLS.txt', 'a') as f:
                for url in url_list:
                    image = '![]' + '(' + url + ')' + '\n'
                    print url, '\n'
                    f.write(image)
            print "\nNOTE: THE MARKDOWN FORMAT URLS ALREADY SAVED IN MARKDOWN_FORMAT_URLS.txt FILE"
            set_clipboard(url_list)
        if removed:
            pass
        before = after
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

def main():
    if os.name == 'nt' or platform.system() == 'Windows':
        window_main()  #window ��ִ��
    else:
        unix_main()   #mac ��ִ��

if __name__ == "__main__":
    main()