'''
import dependent modules.
'''
import os
import sys
import time
import json
import warnings

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
        # check user list
        user_list = os.popen("getent passwd | awk -F: '{print $1}'").readlines()
        for i in range(0,len(user_list)):
            user_list[i] = user_list[i].replace("\n","")
        if (str(self.user) not in user_list):
            os.system("useradd -m -s /bin/bash" + " " + str(self.user))

        # change user passwd
        os.system("echo '" + str(self.user) + ":" + str(self.password) + "' | chpasswd")

        # add sudo permission
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
        os.system("sudo -u" + " " + str(self.user) + " " + "mkdir -p" + " " + "/tmp/" + str(self.path))
        
    '''
    tunnelling method
    '''
    # tunnelling with localtunnel
    def Run_localtunnel(self,port = None,host = "https://localtunnel.me",subdomain = None,verbose = True):
        # check param
        if (port is None):
            port = self.port

        # install localtunnel
        if(len(os.popen("which npm").readlines()) == 0):
            exec_logging = os.popen("apt install nodejs npm -y")
            exec_logging = ''.join(exec_logging.readlines())
            if verbose:
                print(exec_logging)
        exec_logging = os.popen("npm install -g localtunnel")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

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
    def Run_ngrok(self,token = None,port = None,domain = None,verbose = True):
        # check param
        if (token is None):
            token = input("Input your ngrok token: ")
        if (port is None):
            port = self.port

        # install ngrok
        char_cmd = 'curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc > /dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok'
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

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
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

    # run code server
    def Run_code_server(self,port = None,password = None,verbose = True):
        # check param
        if (str(self.user) == 'root'):
            raise RootUserError()
        if (port is None):
            port = self.port
        if (password is None):
            password = self.password

        # install expect
        exec_logging = os.popen("apt install expect -y")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Run_code_server.exp')

        # run code server
        char_cmd = "expect" + " " + str(script_path) + " " + str(self.user) + " " + str(self.password) + " " + str(port) + " " + str(password) + " " + str(self.path)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

    def Install_code_server_extension(self,extension,verbose = True):
        char_cmd = "sudo -u" + " " + str(self.user) + " " + "code-server --install-extension" + " " + str(extension)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

    def Config_code_server(self,property,value):
        # check whether settings.json exists
        file_path = "/home/" + str(self.user) + "/.local/share/code-server/User"
        char_cmd = "sudo -u" + " " + str(self.user) + " " + "mkdir -p" + " " + file_path
        os.system(char_cmd)
        file_path = file_path + "/settings.json"
        if os.path.exists(file_path):
            with open(file_path,"r") as json_file:
                json_setting = json.load(json_file)
        else:
            char_cmd = "sudo -u" + " " + str(self.user) + " " + "touch" + " " + file_path
            os.system(char_cmd)
            json_setting = {}

        # add property
        json_setting[str(property)] = value

        # dump settings
        with open(file_path,"w") as json_file:
            json.dump(json_setting,json_file,indent=4)
            
    '''
    proxy method
    '''
    # run shadowsocks
    def Run_shadowsocks(self,port = None,password = None,encrypt = 'aes-256-gcm',verbose = True):
        # check param
        if (port is None):
            port = self.port
        if (password is None):
            password = self.password

        # install shadowsocks
        exec_logging = os.popen("apt install shadowsocks-libev -y")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

        # run shadowsocks
        char_cmd = "ss-server" + " " + "-s 0.0.0.0" + " " + "-p" + " " + str(port) + " " + "-k" + " " + str(password) + " " + "-m" + " " + str(encrypt)
        char_cmd = "nohup" + " " + char_cmd + " " + ">" + " " + "/tmp/" + str(self.path) + "/shadowsocks.log 2>&1 &"
        os.system(char_cmd)

    '''
    Jekyll method
    '''
    # install Homebrew
    def Install_Homebrew(self,verbose = True):
        # check param
        if (str(self.user) == 'root'):
            raise RootUserError()

        # install expect
        exec_logging = os.popen("apt install expect -y")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Install_Homebrew.exp')

        # run expect script
        char_cmd = "expect" + " " + str(script_path) + " " + str(self.user) + " " + str(self.password) + " " + str(self.path)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

    # install rbenv
    def Install_rbenv(self,verbose = True):
        # check param
        if (str(self.user) == 'root'):
            raise RootUserError()

        # install expect
        exec_logging = os.popen("apt install expect -y")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Install_rbenv.exp')

        # run expect script
        char_cmd = "expect" + " " + str(script_path) + " " + str(self.user) + " " + str(self.password) + " " + str(self.path)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

    # install Ruby
    def Install_Ruby(self,version = None,verbose = True):
        # check param
        if (str(self.user) == 'root'):
            raise RootUserError()
        if (version is None):
            version = input("Input the Ruby version to install: ")

        # install expect
        exec_logging = os.popen("apt install expect -y")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Install_Ruby.exp')

        # run expect script
        char_cmd = "expect" + " " + str(script_path) + " " + str(self.user) + " " + str(self.password) + " " + str(version) + " " + str(self.path)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

    # install Jekyll
    def Install_Jekyll(self,version = None,verbose = True):
        # check param
        if (str(self.user) == 'root'):
            raise RootUserError()
            
        # install dependency
        if verbose:
            print("Install Homebrew: \n")
        self.Install_Homebrew(verbose = verbose)
        if verbose:
            print("Install rbenv: \n")
        self.Install_rbenv(verbose = verbose)
        if verbose:
            print("Install Ruby: \n")
        self.Install_Ruby(version = version,verbose = verbose)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Install_Jekyll.exp')

        # run expect script
        char_cmd = "expect" + " " + str(script_path) + " " + str(self.user) + " " + str(self.password) + " " + str(self.path)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install Jekyll: \n")
            print(exec_logging)

    '''
    stable diffusion method
    '''
    # run stable diffusion webui
    def Run_stable_diffusion_webui(self,path = None,port = None,verbose = True,args = None,**kwargs):
        # check param
        if (port is None):
            port = self.port
        if (path is None):
            path = "/tmp/" + str(self.path)
        else:
            char_cmd = "sudo -u" + " " + str(self.user) + " " + "mkdir -p" + " " + str(path)
            os.system(char_cmd)

        # install dependency
        exec_logging = os.popen("apt install wget git python3 python3-venv libgl1 libglib2.0-0 -y")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

        # install stable diffusion webui
        char_cmd = "wget" + " " + "-q" + " " + "-O" + " " + str(path) + "/webui.sh" + " " + "https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui/master/webui.sh"
        os.system(char_cmd)
        char_cmd = "chmod" + " " + "a+x" + " " + str(path) + "/webui.sh"
        os.system(char_cmd)
        char_cmd = str(path) + "/webui.sh" + " " + "-f" + " " + "--port" + " " + str(port) + " " + "--exit"
        if (args is None):
            for k,v in kwargs.items():
                char_cmd = char_cmd + " " + "--" + str(k)
                if (str(v) != ''):
                    char_cmd = char_cmd + " " + str(v)
        else:
            if (len(kwargs) > 0):
                warnings.warn(message = "Extra arguments will be discarded when using the args parameter!",category = UserWarning)
            char_cmd = char_cmd + " " + str(args)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print(exec_logging)

        # run stable diffusion webui
        char_cmd = str(path) + "/webui.sh" + " " + "-f" + " " + "--port" + " " + str(port)
        if (args is None):
            for k,v in kwargs.items():
                char_cmd = char_cmd + " " + "--" + str(k)
                if (str(v) != ''):
                    char_cmd = char_cmd + " " + str(v)
        else:
            char_cmd = char_cmd + " " + str(args)
        char_cmd = "nohup" + " " + char_cmd + " " + ">" + " " + "/tmp/" + str(self.path) + "/stable_diffusion_webui.log 2>&1 &"
        os.system(char_cmd)
        os.system("sleep 30")
        exec_logging = "stable diffusion webui log file" + ":" + " " + "/tmp/" + str(self.path) + "/stable_diffusion_webui.log."
        print(exec_logging)

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
def update_environment(verbose = True):
    exec_logging = os.popen("apt update")
    exec_logging = ''.join(exec_logging.readlines())
    if verbose:
        print(exec_logging)
    exec_logging = os.popen("apt upgrade -y")
    exec_logging = ''.join(exec_logging.readlines())
    if verbose:
        print(exec_logging)
    exec_logging = os.popen("apt autoremove -y")
    exec_logging = ''.join(exec_logging.readlines())
    if verbose:
        print(exec_logging)
        
'''
define Exception class
'''
# RootUserError
class RootUserError(Exception):
    """Exception raised when the user is root."""

    def __init__(self,message = 'Cannot proceed under user root!'):
        super().__init__(message)