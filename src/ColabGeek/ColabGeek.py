"""
ColabGeek helps to run useful tools on Google Colab.
Dependencies include os, sys, time, json and warnings.

Classes:
 - ColabSession: Class corresponding to the current Colab session.

Exceptions:
 - RootUserError: Raise exception when the ColabSession user is root.

Methods:
 - update_environment: Update Ubuntu system environment.
"""

import os
import sys
import time
import json
import warnings

###############################
## define ColabSession Class ##
###############################

class ColabSession:
    """
    Class corresponding to the current Colab session.

    Initialize Colab session and provide methods to run useful tools on Colab.

    Attributes
    ----------
    user : str
        User name.
    password : str
        User password.
    sudo : bool
        Whether to give sudo permission to the user.
    port : int
        Which port to use for tunnelling.
    mount_GD : bool
        Whether to mount Google Drive.
    keep_busy : bool
        Whether to keep the Colab session busy to prevent termination.
    path : str
        Path to a temporary directory.

    Methods
    -------
    add_user()
        Add or modify a user to the system.
    Google_Drive()
        Mount Google Drive if mount_GD is set to True.
    tmp_path()
        Create a temporary directory in /tmp.
    Run_localtunnel(port = None,host = "https://localtunnel.me",subdomain = None,verbose = True)
        Install and run localtunnel for tunnelling.
    Run_ngrok(token = None,port = None,domain = None,verbose = True)
        Install and run ngrok for tunnelling.
    Run_Cloudflare_Tunnel(token = None,verbose = True)
        Install and run cloudflared for tunnelling.
    Run_Rstudio_server(port = None,verbose = True)
        Install and run Rstudio Server on Colab.
    Run_code_server(port = None,password = None,verbose = True)
        Install and run code server on Colab.
    Install_code_server_extension(extension,verbose = True)
        Install code server extensions.
    Config_code_server(property,value)
        Configure code server.
    Run_JupyterLab(port = None,password = None,mount_Colab = True,verbose = True)
        Install and run JupyterLab on Colab.
    Run_shadowsocks(port = None,password = None,encrypt = 'aes-256-gcm',verbose = True)
        Install and run shadowsocks on Colab.
    Install_Homebrew(verbose = True)
        Install Homebrew on Colab.
    Install_rbenv(verbose = True)
        Install rbenv on Colab.
    Install_Ruby(version = None,verbose = True)
        Install Ruby on Colab.
    Install_Jekyll(Ruby_version = None,verbose = True)
        Install and run Jekyll on Colab.
    Run_stable_diffusion_webui(path = None,port = None,verbose = True,args = None,**kwargs)
        Install and run Stable Diffusion WebUI on Colab.
    busy_session(busy = None)
        Keep the Colab session active.
    Install_Miniconda(path = None,verbose = True)
        Install Miniconda on Colab.
    Install_udocker(verbose = True)
        Install udocker on Colab.
    """
    
    def __init__(self,user,password,sudo = True,port = 8787,mount_GD = False,keep_busy = True):
        """
        Initialize the ColabSession object.

        Initialize the ColabSession object by adding the system user, mounting Google Drive and setting temp directory.

        Parameters
        ----------
        user : str
            User name.
        password : str
            User password.
        sudo : bool, optional
            Whether to give sudo permission to the user.
        port : int, optional
            Which port to use for tunnelling.
        mount_GD : bool, optional
            Whether to mount Google Drive.
        keep_busy : bool, optional
            Whether to keep the Colab session busy to prevent termination.
        """

        self.user = user
        self.password = password
        self.sudo = sudo
        self.port = port
        self.mount_GD = mount_GD
        self.keep_busy = keep_busy
        self.path = None

        # add user
        self.add_user()

        # mount Google Drive
        self.Google_Drive()
        
        # create tmp path
        self.tmp_path()

    ##################
    ## init methods ##
    ##################

    # add user method
    def add_user(self):
        """
        Add or modify a user to the system.
        """

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
        """
        Mount Google Drive if mount_GD is set to True.
        """

        if self.mount_GD:
            from google.colab import drive
            drive.mount('/content/drive')

    # create tmp path method
    def tmp_path(self):
        """
        Create a temporary directory in /tmp.
        """

        self.path = ((os.popen("date +%Y%m%d_%H%M%S").readlines())[0]).replace("\n","")
        os.system("sudo -u" + " " + str(self.user) + " " + "mkdir -p" + " " + "/tmp/" + str(self.path))

    ########################
    ## tunnelling methods ##
    ########################

    # tunnelling with localtunnel
    def Run_localtunnel(self,port = None,host = "https://localtunnel.me",subdomain = None,verbose = True):
        """
        Install and run localtunnel for tunnelling.

        Apart from the Colab notebook, Google Colab prohibits any network connections to the host server.
        Therefore, a tunnelling method is required to access services installed on Colab.
        This function helps to install and run localtunnel for tunnelling.

        parameters
        ----------
        port : int, optional
            Listening port for localtunnel.
        host : str, optional
            Upstream server providing forwarding.
        subdomain : str, optional
            Request this subdomain. Do not include the '_' in the subdomain.
        verbose : bool, optional
            Whether to show the running logs.

        Returns
        -------
        str
            The localtunnel forwarding url.
        """

        # check param
        if (port is None):
            port = self.port

        # install localtunnel
        if(len(os.popen("which npm").readlines()) == 0):
            exec_logging = os.popen("apt install nodejs npm -y")
            exec_logging = ''.join(exec_logging.readlines())
            if verbose:
                print("Install nodejs and npm: \n")
                print(exec_logging)
        exec_logging = os.popen("npm install -g localtunnel")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install localtunnel: \n")
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
        """
        Install and run ngrok for tunnelling.

        Apart from the Colab notebook, Google Colab prohibits any network connections to the host server.
        Therefore, a tunnelling method is required to access services installed on Colab.
        This function helps to install and run ngrok for tunnelling.

        Parameters
        ----------
        token : str, optional
            The token of your personal ngrok account.
        port : int, optional
            Listening port for ngrok.
        domain : str, optional
            Request this domain.
        verbose : bool, optional
            Whether to show the running logs.

        Returns
        -------
        str
            The ngrok forwarding url.
        """

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
            print("Install ngrok: \n")
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

    # tunnelling with cloudflared
    def Run_Cloudflare_Tunnel(self,token = None,verbose = True):
        """
        Install and run cloudflared for tunnelling.

        Apart from the Colab notebook, Google Colab prohibits any network connections to the host server.
        Therefore, a tunnelling method is required to access services installed on Colab.
        This function helps to install and run cloudflared, which is a server-side daemon for Cloudflare Tunnel.

        Parameters
        ----------
        token : str, optional
            The token of your tunnels created on Cloudflare.
        verbose : bool, optional
            Whether to show the running logs.
        """

        # check param
        if (token is None):
            token = input("Input your tunnel token: ")

        # install cloudflared
        char_cmd = "curl -L --output" + " " + "/tmp/" + str(self.path) + "/cloudflared.deb" + " " + "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
        char_cmd = char_cmd + " " + "&&" + " " + "dpkg -i" + " " + "/tmp/" + str(self.path) + "/cloudflared.deb"
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install cloudflared: \n")
            print(exec_logging)

        # exec cmd
        char_cmd = "cloudflared service install" + " " + str(token)
        char_cmd = "nohup" + " " + char_cmd + " " + "> /tmp/" + str(self.path) + "/cloudflared.log 2>&1 &"

        # exec
        os.system(char_cmd)
        os.system("sleep 30")
        char_cmd = "cat" + " " + "/tmp/" + str(self.path) + "/cloudflared.log"
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Run cloudflared: \n")
            print(exec_logging)

    #####################
    ## web IDE methods ##
    #####################

    # run Rstudio server
    def Run_Rstudio_server(self,port = None,verbose = True):
        """
        Install and run Rstudio Server on Colab.

        The Colab notebook is an excellent integrated development environment for Python.
        Although it can also run the R kernel, using the Rstudio Server for data analysis provides a more comfortable experience.
        This function helps to install and run Rstudio Server on Colab.

        Parameters
        ----------
        port : int, optional
            Listening port for Rstudio Server.
        verbose : bool, optional
            Whether to show the running logs.
        """

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
            print("Install Rstudio Server: \n")
            print(exec_logging)

    # run code server
    def Run_code_server(self,port = None,password = None,verbose = True):
        """
        Install and run code server on Colab.

        The code server is an online integrated development environment with a VSCode style.
        It supports development in multiple languages and a variety of VSCode plugins.
        This function helps to install and run code server on Colab.

        Parameters
        ----------
        port : int, optional
            Listening port for code server.
        password : str, optional
            The code server login password.
        verbose : bool, optional
            Whether to show the running logs.

        Raises
        ------
        RootUserError
            If the ColabSession user is root.
        """

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
            print("Install expect: \n")
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Run_code_server.exp')

        # run code server
        char_cmd = "expect" + " " + str(script_path) + " " + str(self.user) + " " + str(self.password) + " " + str(port) + " " + str(password) + " " + str(self.path)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install code server: \n")
            print(exec_logging)

    # install code server plugins
    def Install_code_server_extension(self,extension,verbose = True):
        """
        Install code server extensions.

        The code server supports a variety of VSCode plugins.
        This function helps to install code server extensions through command line.

        Parameters
        ----------
        extension : str
            The extension id or the path of the VSIX file.
        verbose : bool, optional
            Whether to show the running logs.
        """

        char_cmd = "sudo -u" + " " + str(self.user) + " " + "code-server --install-extension" + " " + str(extension)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install" + " " + str(extension) + ": \n")
            print(exec_logging)

    # configure code server
    def Config_code_server(self,property,value):
        """
        Configure code server.

        This function updates the `settings.json` file for the code server instance by adding a specified property-value pair.

        Parameters
        ----------
        property : str
            Specify the property to be added or updated in the `settings.json` file.
        value : str
            Specify the value for the corresponding property.
        """

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

    # run JupyterLab
    def Run_JupyterLab(self,port = None,password = None,mount_Colab = True,verbose = True):
        """
        Install and run JupyterLab on Colab.

        JupyterLab is a web IDE for working with Jupyter Notebooks, providing a powerful environment for interactive computing.
        This function helps to install and run mrdoge/jupyterlab container from Docker Hub using udocker.

        Parameters
        ----------
        port : int, optional
            Listening port for JupyterLab.
        password : str, optional
            The JupyterLab login password.
        mount_Colab : bool, optional
            Whether map the Colab /content directory to the JupyterLab container /content directory.
        verbose : bool, optional
            Whether to show the running logs.

        Raises
        ------
        ImportError
            If the jupyter_server.auth module is not installed.
        """

        # import dependency
        try:
            import jupyter_server.auth
        except ImportError:
            print("jupyter_server.auth does not exist, try execute `pip install jupyter_server`.")
            return(None)

        # check param
        if (str(self.user) == 'root'):
            warnings.warn(message = "Running udocker and JupyterLab as root may lead to unexpected issues!",category = UserWarning)
        if (port is None):
            port = self.port
        if (password is None):
            password = self.password
        password = jupyter_server.auth.passwd(str(password))

        # install udocker
        self.Install_udocker(verbose = verbose)

        # pull JupyterLab
        char_cmd = "sudo -u" + " " + str(self.user) + " " + "udocker --allow-root pull mrdoge/jupyterlab"
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Pull mrdoge/jupyterlab: \n")
            print(exec_logging)

        # run JupyterLab
        char_cmd = "sudo -u" + " " + str(self.user) + " " + "udocker --allow-root run -p" + " " + str(port) + ":" + "8888"
        if mount_Colab:
            char_cmd = char_cmd + " " + "-v /content:/content"
        char_cmd = char_cmd + " " + "mrdoge/jupyterlab" + " " + "jupyter lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser" + " " + "--ServerApp.password" + "=" + "'" + str(password) + "'"
        char_cmd = "nohup" + " " + char_cmd + " " + ">" + " " + "/tmp/" + str(self.path) + "/JupyterLab.log 2>&1 &"
        os.system(char_cmd)
        os.system("sleep 120")
        char_cmd = "cat" + " " + "/tmp/" + str(self.path) + "/JupyterLab.log"
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("JupyterLab log: \n")
            print(exec_logging)

    ###################
    ## proxy methods ##
    ###################

    # run shadowsocks
    def Run_shadowsocks(self,port = None,password = None,encrypt = 'aes-256-gcm',verbose = True):
        """
        Install and run shadowsocks on Colab.

        This function is used to set up the shadowsocks server, which is a secure socks5 proxy.

        Parameters
        ----------
        port : int, optional
            Listening port for shadowsocks server.
        password : str, optional
            The shadowsocks server password.
        encrypt : str, optional
            The encryption method for shadowsocks server.
        verbose : bool, optional
            Whether to show the running logs.
        """

        # check param
        if (port is None):
            port = self.port
        if (password is None):
            password = self.password

        # install shadowsocks
        exec_logging = os.popen("apt install shadowsocks-libev -y")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install shadowsocks-libev: \n")
            print(exec_logging)

        # run shadowsocks
        char_cmd = "ss-server" + " " + "-s 0.0.0.0" + " " + "-p" + " " + str(port) + " " + "-k" + " " + str(password) + " " + "-m" + " " + str(encrypt)
        char_cmd = "nohup" + " " + char_cmd + " " + ">" + " " + "/tmp/" + str(self.path) + "/shadowsocks.log 2>&1 &"
        os.system(char_cmd)

    ####################
    ## Jekyll methods ##
    ####################

    # install Homebrew
    def Install_Homebrew(self,verbose = True):
        """
        Install Homebrew on Colab.

        Homebrew is a package manager for macOS and Linux. This function helps to install Homebrew on Colab.

        Parameters
        ----------
        verbose : bool, optional
            Whether to show the running logs.

        Raises
        ------
        RootUserError
            If the ColabSession user is root.
        """

        # check param
        if (str(self.user) == 'root'):
            raise RootUserError()

        # install expect
        exec_logging = os.popen("apt install expect -y")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install expect: \n")
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Install_Homebrew.exp')

        # run expect script
        char_cmd = "expect" + " " + str(script_path) + " " + str(self.user) + " " + str(self.password) + " " + str(self.path)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print('Install Homebrew: \n')
            print(exec_logging)

    # install rbenv
    def Install_rbenv(self,verbose = True):
        """
        Install rbenv on Colab.

        The rbenv is a Ruby version manager, which allows for easy installation of multiple versions of Ruby.
        This function helps to install rbenv on Colab by Homebrew.

        Parameters
        ----------
        verbose : bool, optional
            Whether to show the running logs.

        Raises
        ------
        RootUserError
            If the ColabSession user is root.
        """

        # check param
        if (str(self.user) == 'root'):
            raise RootUserError()

        # install expect
        exec_logging = os.popen("apt install expect -y")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install expect: \n")
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Install_rbenv.exp')

        # run expect script
        char_cmd = "expect" + " " + str(script_path) + " " + str(self.user) + " " + str(self.password) + " " + str(self.path)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install rbenv: \n")
            print(exec_logging)

    # install Ruby
    def Install_Ruby(self,version = None,verbose = True):
        """
        Install Ruby on Colab.

        This function helps to install a specified version of Ruby using rbenv.

        Parameters
        ----------
        version : str, optional
            The version number of Ruby to install.
        verbose : bool, optional
            Whether to show the running logs.

        Raises
        ------
        RootUserError
            If the ColabSession user is root.
        """

        # check param
        if (str(self.user) == 'root'):
            raise RootUserError()
        if (version is None):
            version = input("Input the Ruby version to install: ")

        # install expect
        exec_logging = os.popen("apt install expect -y")
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install expect: \n")
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Install_Ruby.exp')

        # run expect script
        char_cmd = "expect" + " " + str(script_path) + " " + str(self.user) + " " + str(self.password) + " " + str(version) + " " + str(self.path)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install Ruby: \n")
            print(exec_logging)

    # install Jekyll
    def Install_Jekyll(self,Ruby_version = None,verbose = True):
        """
        Install and run Jekyll on Colab.

        Jekyll is a simple, blog-aware, static site generator suited for personal, project or organizational sites.
        This function helps to install and run Jekyll on Colab.

        Parameters
        ----------
        Ruby_version : str, optional
            The version number of Ruby to install.
        verbose : bool, optional
            Whether to show the running logs.

        Raises
        ------
        RootUserError
            If the ColabSession user is root.
        """

        # check param
        if (str(self.user) == 'root'):
            raise RootUserError()
            
        # install dependency
        self.Install_Homebrew(verbose = verbose)
        self.Install_rbenv(verbose = verbose)
        self.Install_Ruby(version = Ruby_version,verbose = verbose)

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

    ##############################
    ## stable diffusion methods ##
    ##############################

    # run stable diffusion webui
    def Run_stable_diffusion_webui(self,path = None,port = None,verbose = True,args = None,**kwargs):
        """
        Install and run Stable Diffusion WebUI on Colab.

        Stable Diffusion WebUI is a browser interface for Stable Diffusion that allows to generate AI art more easily.
        This function helps to install and run Stable Diffusion WebUI on Colab.

        Parameters
        ----------
        path : str, optional
            The directory to install Stable Diffusion WebUI.
        port : int, optional
            Listening port for Stable Diffusion WebUI.
        verbose : bool, optional
            Whether to show the running logs.
        args : str, optional
            Additional arguments to pass to the Stable Diffusion WebUI setup script.
        **kwargs : dict, optional
            Additional arguments to pass to the Stable Diffusion WebUI setup script.
            Cannot be used in conjunction with the `args` parameter.

        Returns
        -------
        str
            The path for the Stable Diffusion WebUI log file.
        """

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
            print("Install dependency: \n")
            print(exec_logging)

        # install Stable Diffusion WebUI
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
            print("Install Stable Diffusion WebUI: \n")
            print(exec_logging)

        # run Stable Diffusion WebUI
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
        exec_logging = "Stable Diffusion WebUI log file" + ":" + " " + "/tmp/" + str(self.path) + "/stable_diffusion_webui.log."
        print(exec_logging)

    ###################
    ## other methods ##
    ###################

    # keep Colab session busy
    def busy_session(self,busy = None):
        """
        Keep the Colab session active.

        This function helps to keep the Colab session busy to prevent termination.

        Parameters
        ----------
        busy : bool, optional
            Whether to keep the Colab session busy.
        """

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

    # install Miniconda
    def Install_Miniconda(self,path = None,verbose = True):
        """
        Install Miniconda on Colab.

        Miniconda is a free and minimal installer for the conda package manager and frequently used in scientific computing.
        This function helps to install Miniconda on Colab.

        Parameters
        ----------
        path : str, optional
            The directory to install Miniconda.
        verbose : bool, optional
            Whether to show the running logs.
        """

        # check param
        if (path is None):
            path = "/home/" + str(self.user)
        else:
            char_cmd = "sudo -u" + " " + str(self.user) + " " + "mkdir -p" + " " + str(path)
            os.system(char_cmd)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,'shell_scripts','Install_Miniconda.sh')

        # install Miniconda
        char_cmd = "sudo -u" + " " + str(self.user) + " " + "bash" + " " + str(script_path) + " " + str(self.user) + " " + str(path)
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install Miniconda: \n")
            print(exec_logging)

    # install udocker
    def Install_udocker(self,verbose = True):
        """
        Install udocker on Colab.

        udocker is a basic user tool to execute simple docker containers in user space without requiring root privileges.
        udocker can also run inside a docker container, making it a perfect tool for executing containers on Colab.

        Parameters
        ----------
        verbose : bool, optional
            Whether to show the running logs.
        """

        # install udocker
        char_cmd = "pip install udocker" + " " + "&&" + " " + "sudo -u" + " " + str(self.user) + " " + "udocker --allow-root install"
        exec_logging = os.popen(char_cmd)
        exec_logging = ''.join(exec_logging.readlines())
        if verbose:
            print("Install udocker: \n")
            print(exec_logging)

##########################
## define other methods ##
##########################

# update environment
def update_environment(verbose = True):
    """
    Update Ubuntu system environment.

    This function helps to update Ubuntu system environment.

    Parameters
    ----------
    verbose : bool, optional
        Whether to show the running logs.
    """

    exec_logging = os.popen("apt update")
    exec_logging = ''.join(exec_logging.readlines())
    if verbose:
        print("apt update: \n")
        print(exec_logging)
    exec_logging = os.popen("apt upgrade -y")
    exec_logging = ''.join(exec_logging.readlines())
    if verbose:
        print("apt upgrade: \n")
        print(exec_logging)
    exec_logging = os.popen("apt autoremove -y")
    exec_logging = ''.join(exec_logging.readlines())
    if verbose:
        print("apt autoremove: \n")
        print(exec_logging)

############################
## define Exception Class ##
############################

# RootUserError
class RootUserError(Exception):
    """Exception raised when the ColabSession user is root."""

    def __init__(self,message = 'Cannot proceed under ColabSession user root!'):
        super().__init__(message)
