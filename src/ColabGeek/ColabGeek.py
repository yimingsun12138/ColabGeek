'''
import dependent modules.
'''
import os
import sys
import time

'''
define ColabSession class
'''
class ColabSession:
    def __init__(self,user,password,sudo = True,port = 8787,mount_GD = False,keep_busy = True):
        self.user = user
        self.password = password
        self.sudo = sudo
        self.port = port
        self.mount_GD = mount_GD
        self.keep_busy = keep_busy

        # add user
        self.add_user()

        # mount Google Drive
        self.Google_Drive()
        
        # create tmp path
        self.tmp_path()

    '''
    init methods
    '''
    # add user method
    def add_user(self):
        os.system("useradd -m -s /bin/bash" + " " + str(self.user))
        os.system("echo '" + str(self.user) + ":" + str(self.password) + "' | chpasswd")
        if self.sudo:
            os.system("usermod -G sudo" + " " + str(self.user))

    # mount Google Drive method
    def Google_Drive(self):
        if self.mount_GD:
            from google.colab import drive
            drive.mount('/content/drive')

    # create tmp path method
    def tmp_path(self):
        self.path = ((os.popen("date +%Y%m%d_%H%M%S").readlines())[0]).replace("\n","")
        os.system("sudo -u" + " " + str(self.user) + " " + "mkdir /tmp/" + str(self.path))
        
    '''
    tunnelling method
    '''
    # tunnelling with localtunnel
    def Run_localtunnel(self,port = None,host = "https://localtunnel.me",subdomain = None):
        # check param
        if (port is None):
            port = self.port

        # install localtunnel
        if(len(os.popen("which npm").readlines()) == 0):
            os.system("apt install nodejs npm -y")
        os.system("npm install -g localtunnel")

        # exec cmd
        char_cmd = "lt --port" + " " + str(port) + " " + "--host" + " " + str(host)
        if not(subdomain is None):
            char_cmd = char_cmd + " " + "--subdomain" + " " + str(subdomain)
        char_cmd = "nohup" + " " + char_cmd + " " + "> /tmp/" + str(self.path) + "/localtunnel.log 2>&1 &"

        # exec
        os.system(char_cmd)
        os.system("sleep 10")

        # return
        lt_url = os.popen("cat" + " " + "/tmp/" + str(self.path) + "/localtunnel.log" + " " + "|" + " " + "grep 'your url is:'")
        lt_url = ((lt_url.readlines())[0]).replace("\n","")
        return(lt_url)

    # tunnelling with ngrok
    def Run_ngrok(self,token = None,port = None,domain = None):
        # check param
        if (token is None):
            token = input("Input your ngrok token: ")
        if (port is None):
            port = self.port

        # install ngrok
        char_cmd = 'curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc > /dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok'
        os.system(char_cmd)

        # auth
        char_cmd = "ngrok config add-authtoken" + " " + str(token)
        os.system(char_cmd)

        # exec cmd
        char_cmd = "ngrok http" + " " + str(port)
        if not(domain is None):
            char_cmd = char_cmd + " " + "--domain" + " " + str(domain)
        char_cmd = char_cmd + " " + "--log stdout > /tmp/" + str(self.path) + "/ngrok.log &"

        # exec
        os.system(char_cmd)
        os.system("sleep 10")

        # return
        ngrok_url = os.popen("cat" + " " + "/tmp/" + str(self.path) + "/ngrok.log" + " " + "|" + " " + "grep 'started tunnel'")
        ngrok_url = ((ngrok_url.readlines())[0]).replace("\n","")
        return(ngrok_url)

    '''
    web IDE methods
    '''
    # run Rstudio server
    def Run_Rstudio_server(self,port = None,verbose = True):
        # check param
        if (port is None):
            port = self.port

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Run_Rstudio_server.sh')

        # run Rstudio server
        char_cmd = "bash" + " " + str(script_path) + " " + str(self.path) + " " + str(port)
        exec_logging = os.popen(char_cmd)
        if verbose:
            exec_logging = ''.join(exec_logging.readlines())
            print(exec_logging)

    # run code server
    def Run_code_server(self,port = None,password = None,verbose = True):
        # check param
        if (port is None):
            port = self.port
        if (password is None):
            password = self.password

        # install expect
        os.system("apt install expect -y")

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Run_code_server.exp')

        # run code server
        char_cmd = "expect" + " " + str(script_path) + " " + str(self.user) + " " + str(self.password) + " " + str(port) + " " + str(password) + " " + str(self.path)
        exec_logging = os.popen(char_cmd)
        if verbose:
            exec_logging = ''.join(exec_logging.readlines())
            print(exec_logging)
            
    '''
    proxy method
    '''
    # run shadowsocks
    def Run_shadowsocks(self,port = None,password = None,encrypt = 'aes-256-gcm'):
        # check param
        if (port is None):
            port = self.port
        if (password is None):
            password = self.password

        # install shadowsocks
        os.system("apt install shadowsocks-libev -y")

        # run shadowsocks
        char_cmd = "ss-server" + " " + "-s 0.0.0.0" + " " + "-p" + " " + str(port) + " " + "-k" + " " + str(password) + " " + "-m" + " " + str(encrypt)
        char_cmd = "nohup" + " " + char_cmd + " " + ">" + " " + "/tmp/" + str(self.path) + "/shadowsocks.log 2>&1 &"
        os.system(char_cmd)

    '''
    other method
    '''
    # keep Colab session busy
    def busy_session(self,busy = None):
        # check param
        if (busy is None):
            busy = self.keep_busy
        ii = 1

        # while loop
        while busy:
            i = "round" + " " + str(ii)
            print(i)
            ii = ii + 1
            time.sleep(60)

'''
define other method
'''
# update environment
def update_environment():
    os.system("apt update")
    os.system("apt upgrade -y")
    os.system("apt autoremove -y")