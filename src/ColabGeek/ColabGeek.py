"""
ColabGeek helps to run useful tools on Google Colab.
Dependencies include os, sys, time, json, warnings, google.colab and jupyter_server.auth.

Classes:
 - ColabSession: Class corresponding to the current Colab session.

Exceptions:
 - RootUserError: Exception raised when the ColabSession user is root.
 - SudoPermissionError: Exception raised when the ColabSession user lacks sudo permission.

Methods:
 - update_environment: Update Ubuntu system environment.
"""

import os
import sys
import time
import json
import warnings

###############################
## define ColabSession class ##
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
        Add or modify a user in the system.
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
        Install and run Rstudio server on Colab.
    Run_code_server(port = None,password = None,verbose = True)
        Install and run code server on Colab.
    Install_code_server_extension(extension,verbose = True)
        Install code server extension.
    Config_code_server(property,value)
        Configure code server.
    Run_JupyterLab(port = None,password = None,mount_Colab = True,verbose = True)
        Install and run JupyterLab on Colab.
    Run_shadowsocks(port = None,password = None,encrypt = "aes-256-gcm",verbose = True)
        Install and run shadowsocks on Colab.
    Install_Homebrew(verbose = True)
        Install Homebrew on Colab.
    Install_rbenv(verbose = True)
        Install rbenv on Colab.
    Install_Ruby(version = None,verbose = True)
        Install Ruby on Colab.
    Install_Jekyll(Ruby_version = None,verbose = True)
        Install Jekyll on Colab.
    Run_Stable_Diffusion_WebUI(path = None,port = None,verbose = True,args = None,**kwargs)
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

        Initialize the ColabSession object by adding a new user, mounting Google Drive and setting tmp directory.

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

        self.user = str(user)
        self.password = str(password)
        self.sudo = bool(sudo)
        self.port = int(port)
        self.mount_GD = bool(mount_GD)
        self.keep_busy = bool(keep_busy)
        self.path = None

        # add user
        self.add_user()

        # mount Google Drive
        self.Google_Drive()

        # create tmp path
        self.tmp_path()

    #######################
    ## initialize method ##
    #######################

    # add user
    def add_user(self):
        """
        Add or modify a user in the system.
        """

        # check user list
        user_list = os.popen("getent passwd | awk -F: '{print $1}'").readlines()
        for i in range(0,len(user_list)):
            user_list[i] = user_list[i].replace("\n","")
        if (str(self.user) not in user_list):
            os.system(f"useradd -m -s /bin/bash {str(self.user)}")

        # change user password
        os.system(f"echo '{str(self.user)}:{str(self.password)}' | chpasswd")

        # add sudo permission
        if self.sudo:
            os.system(f"usermod -G sudo {str(self.user)}")

    # mount Google Drive
    def Google_Drive(self):
        """
        Mount Google Drive if mount_GD is set to True.

        Raises
        ------
        ImportError
            If the google.colab module is not installed.
        """

        if self.mount_GD:
            try:
                from google.colab import drive
            except ImportError as e:
                error_message = f"{e}.\n\nPlease set the `mount_GD` parameter to False and try manually mounting Google Drive. Contact the author if the problem persists."
                raise ImportError(error_message) from e
            drive.mount('/content/drive')

    # create tmp path
    def tmp_path(self):
        """
        Create a temporary directory in /tmp.
        """

        self.path = ((os.popen("date +%Y%m%d_%H%M%S").readlines())[0]).replace("\n","")
        os.system(f"sudo -u {str(self.user)} mkdir -p /tmp/{str(self.path)}")

    #######################
    ## tunnelling method ##
    #######################

    # tunnelling by localtunnel
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
            Upstream host server providing forwarding.
        subdomain : str, optional
            Request this subdomain. Do not include the "_" in the subdomain.
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
            exec_logging = os.popen("apt install -y nodejs npm")
            exec_logging = "".join(exec_logging.readlines())
            if verbose:
                print("Install nodejs and npm: \n")
                print(exec_logging)
        exec_logging = os.popen("npm install -g localtunnel")
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install localtunnel: \n")
            print(exec_logging)

        # exec cmd
        char_cmd = f"lt --port {str(port)} --host {str(host)}"
        if not(subdomain is None):
            char_cmd = f"{char_cmd} --subdomain {str(subdomain)}"
        char_cmd = f"nohup {char_cmd} > /tmp/{str(self.path)}/localtunnel.log 2>&1 &"

        # exec
        os.system(char_cmd)
        os.system("sleep 10")

        # return
        lt_url = os.popen(f"cat /tmp/{str(self.path)}/localtunnel.log | grep 'your url is:'")
        lt_url = ((lt_url.readlines())[0]).replace("\n","")
        return(lt_url)

    # tunnelling by ngrok
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
        char_cmd = 'curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc > /dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install -y ngrok'
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install ngrok: \n")
            print(exec_logging)

        # auth ngrok
        char_cmd = f"ngrok config add-authtoken {str(token)}"
        os.system(char_cmd)

        # exec cmd
        char_cmd = f"ngrok http {str(port)}"
        if not(domain is None):
            char_cmd = f"{char_cmd} --domain {str(domain)}"
        char_cmd = f"{char_cmd} --log stdout > /tmp/{str(self.path)}/ngrok.log &"

        # exec
        os.system(char_cmd)
        os.system("sleep 10")

        # return
        ngrok_url = os.popen(f"cat /tmp/{str(self.path)}/ngrok.log | grep 'started tunnel'")
        ngrok_url = ((ngrok_url.readlines())[0]).replace("\n","")
        return(ngrok_url)

    # tunnelling by cloudflared
    def Run_Cloudflare_Tunnel(self,token = None,verbose = True):
        """
        Install and run cloudflared for tunnelling.

        Apart from the Colab notebook, Google Colab prohibits any network connections to the host server.
        Therefore, a tunnelling method is required to access services installed on Colab.
        This function helps to install and run cloudflared, which is a server-side daemon for Cloudflare Tunnel.

        Parameters
        ----------
        token : str, optional
            The token of your tunnel created on Cloudflare.
        verbose : bool, optional
            Whether to show the running logs.
        """

        # check param
        if (token is None):
            token = input("Input your tunnel token: ")

        # install cloudflared
        char_cmd = f"curl -L --output /tmp/{str(self.path)}/cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
        char_cmd = f"{char_cmd} && dpkg -i /tmp/{str(self.path)}/cloudflared.deb"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install cloudflared: \n")
            print(exec_logging)

        # exec cmd
        char_cmd = f"cloudflared service install {str(token)}"
        char_cmd = f"nohup {char_cmd} > /tmp/{str(self.path)}/cloudflared.log 2>&1 &"

        # exec
        os.system(char_cmd)
        os.system("sleep 30")
        char_cmd = f"cat /tmp/{str(self.path)}/cloudflared.log"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Run cloudflared: \n")
            print(exec_logging)

    ####################
    ## web IDE method ##
    ####################

    # run Rstudio server
    def Run_Rstudio_server(self,port = None,verbose = True):
        """
        Install and run Rstudio server on Colab.

        The Colab notebook is an excellent integrated development environment for Python.
        Although it can also run the R kernel, using the Rstudio server for data analysis provides a more user-friendly experience.
        This function helps to install and run Rstudio server on Colab.

        Parameters
        ----------
        port : int, optional
            Listening port for Rstudio server.
        verbose : bool, optional
            Whether to show the running logs.
        """

        # check param
        if (port is None):
            port = self.port

        # install gdebi-core
        exec_logging = os.popen("apt install -y gdebi-core")
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install gdebi-core: \n")
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,"shell_scripts","Run_Rstudio_server.sh")

        # run Rstudio server
        char_cmd = f"bash {str(script_path)} {str(self.path)} {str(port)}"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install and run Rstudio server: \n")
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
        SudoPermissionError
            If the ColabSession user lacks sudo permission.
        """

        # check param
        if (str(self.user) == "root"):
            raise RootUserError()
        if (self.sudo == False):
            raise SudoPermissionError()
        if (port is None):
            port = self.port
        if (password is None):
            password = self.password

        # install expect
        exec_logging = os.popen("apt install -y expect")
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install expect: \n")
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,"shell_scripts","Run_code_server.exp")

        # run code server
        char_cmd = f"expect {str(script_path)} {str(self.user)} {str(self.password)} {str(port)} {str(password)} {str(self.path)}"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install and run code server: \n")
            print(exec_logging)

    # install code server extension
    def Install_code_server_extension(self,extension,verbose = True):
        """
        Install code server extension.

        The code server supports a variety of VSCode plugins.
        This function helps to install code server extension through command line.

        Parameters
        ----------
        extension : str
            The extension id or the path of the VSIX file.
        verbose : bool, optional
            Whether to show the running logs.
        """

        char_cmd = f"sudo -u {str(self.user)} code-server --install-extension {str(extension)}"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print(f"Install {str(extension)}: \n")
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
        value : any
            Specify the value for the corresponding property, can be of any type that is supported by JSON.
        """

        # check whether settings.json exists
        file_path = f"/home/{str(self.user)}/.local/share/code-server/User"
        char_cmd = f"sudo -u {str(self.user)} mkdir -p {file_path}"
        os.system(char_cmd)
        file_path = f"{file_path}/settings.json"
        if os.path.exists(file_path):
            with open(file_path,"r") as json_file:
                json_setting = json.load(json_file)
        else:
            char_cmd = f"sudo -u {str(self.user)} touch {file_path}"
            os.system(char_cmd)
            json_setting = {}

        # add property
        json_setting[str(property)] = value

        # dump json setting
        with open(file_path,"w") as json_file:
            json.dump(json_setting,json_file,indent = 4)

    # run JupyterLab
    def Run_JupyterLab(self,port = None,password = None,mount_Colab = True,verbose = True):
        """
        Install and run JupyterLab on Colab.

        JupyterLab is an online integrated development environment for interactive computing.
        This function helps to pull and run mrdoge/jupyterlab image from Docker Hub using udocker.

        Parameters
        ----------
        port : int, optional
            Listening port for JupyterLab.
        password : str, optional
            The JupyterLab login password.
        mount_Colab : bool, optional
            Whether to map the Colab /content directory to the JupyterLab container /content directory.
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
        except ImportError as e:
            error_message = f"{e}.\n\nPlease try executing `pip install jupyter_server` to fix the error. Contact the author if the problem persists."
            raise ImportError(error_message) from e

        # check param
        if (str(self.user) == "root"):
            warnings.warn(message = "Running udocker and JupyterLab under ColabSession user root may lead to unexpected issues!",category = UserWarning)
        if (port is None):
            port = self.port
        if (password is None):
            password = self.password
        password = jupyter_server.auth.passwd(str(password))

        # install udocker
        self.Install_udocker(verbose = verbose)

        # pull JupyterLab
        char_cmd = f"sudo -u {str(self.user)} udocker --allow-root pull mrdoge/jupyterlab"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Pull mrdoge/jupyterlab: \n")
            print(exec_logging)

        # run JupyterLab
        char_cmd = f"sudo -u {str(self.user)} udocker --allow-root run -p {str(port)}:8888"
        if mount_Colab:
            char_cmd = f"{char_cmd} -v /content:/content"
        char_cmd = f"{char_cmd} mrdoge/jupyterlab jupyter lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser --ServerApp.password='{str(password)}'"
        char_cmd = f"nohup {char_cmd} > /tmp/{str(self.path)}/JupyterLab.log 2>&1 &"
        os.system(char_cmd)
        os.system("sleep 120")
        char_cmd = f"cat /tmp/{str(self.path)}/JupyterLab.log"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("JupyterLab log: \n")
            print(exec_logging)

    ##################
    ## proxy method ##
    ##################

    # run shadowsocks
    def Run_shadowsocks(self,port = None,password = None,encrypt = "aes-256-gcm",verbose = True):
        """
        Install and run shadowsocks on Colab.

        This function helps to set up the shadowsocks server, which operates as a secure socks5 proxy.

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
        exec_logging = os.popen("apt install -y shadowsocks-libev")
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install shadowsocks-libev: \n")
            print(exec_logging)

        # run shadowsocks
        char_cmd = f"ss-server -s 0.0.0.0 -p {str(port)} -k {str(password)} -m {str(encrypt)}"
        char_cmd = f"nohup {char_cmd} > /tmp/{str(self.path)}/shadowsocks.log 2>&1 &"
        os.system(char_cmd)
        os.system("sleep 10")
        char_cmd = f"cat /tmp/{str(self.path)}/shadowsocks.log"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Run shadowsocks-libev: \n")
            print(exec_logging)

    ###################
    ## Jekyll method ##
    ###################

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
        SudoPermissionError
            If the ColabSession user lacks sudo permission.
        """

        # check param
        if (str(self.user) == "root"):
            raise RootUserError()
        if (self.sudo == False):
            raise SudoPermissionError()

        # install expect
        exec_logging = os.popen("apt install -y expect")
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install expect: \n")
            print(exec_logging)

        # install Homebrew dependencies
        exec_logging = os.popen("apt install -y build-essential")
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install Homebrew dependencies: \n")
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,"shell_scripts","Install_Homebrew.exp")

        # run expect script
        char_cmd = f"expect {str(script_path)} {str(self.user)} {str(self.password)} {str(self.path)}"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install Homebrew: \n")
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
        SudoPermissionError
            If the ColabSession user lacks sudo permission.
        """

        # check param
        if (str(self.user) == "root"):
            raise RootUserError()
        if (self.sudo == False):
            raise SudoPermissionError()

        # install expect
        exec_logging = os.popen("apt install -y expect")
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install expect: \n")
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,"shell_scripts","Install_rbenv.exp")

        # run expect script
        char_cmd = f"expect {str(script_path)} {str(self.user)} {str(self.password)} {str(self.path)}"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install rbenv: \n")
            print(exec_logging)

    # install Ruby
    def Install_Ruby(self,version = None,verbose = True):
        """
        Install Ruby on Colab.

        This function helps to install a specified version of Ruby on Colab by rbenv.

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
        SudoPermissionError
            If the ColabSession user lacks sudo permission.
        """

        # check param
        if (str(self.user) == "root"):
            raise RootUserError()
        if (self.sudo == False):
            raise SudoPermissionError()
        if (version is None):
            version = input("Input the Ruby version to install: ")

        # install expect
        exec_logging = os.popen("apt install -y expect")
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install expect: \n")
            print(exec_logging)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,"shell_scripts","Install_Ruby.exp")

        # run expect script
        char_cmd = f"expect {str(script_path)} {str(self.user)} {str(self.password)} {str(version)} {str(self.path)}"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install Ruby: \n")
            print(exec_logging)

    # install Jekyll
    def Install_Jekyll(self,Ruby_version = None,verbose = True):
        """
        Install Jekyll on Colab.

        Jekyll is a simple, blog-aware, static site generator suited for personal, project or organizational sites.
        This function helps to install Jekyll on Colab.

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
        SudoPermissionError
            If the ColabSession user lacks sudo permission.
        """

        # check param
        if (str(self.user) == "root"):
            raise RootUserError()
        if (self.sudo == False):
            raise SudoPermissionError()

        # install dependencies
        self.Install_Homebrew(verbose = verbose)
        self.Install_rbenv(verbose = verbose)
        self.Install_Ruby(version = Ruby_version,verbose = verbose)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,"shell_scripts","Install_Jekyll.exp")

        # run expect script
        char_cmd = f"expect {str(script_path)} {str(self.user)} {str(self.password)} {str(self.path)}"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install Jekyll: \n")
            print(exec_logging)

    #############################
    ## Stable Diffusion method ##
    #############################

    # run Stable Diffusion WebUI
    def Run_Stable_Diffusion_WebUI(self,path = None,port = None,verbose = True,args = None,**kwargs):
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
            path = f"/home/{str(self.user)}/Stable_Diffusion_WebUI"
        char_cmd = f"sudo -u {str(self.user)} mkdir -p {str(path)}"
        os.system(char_cmd)

        # install dependencies
        exec_logging = os.popen("apt install -y wget git python3 python3-venv libgl1 libglib2.0-0")
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install dependencies: \n")
            print(exec_logging)

        # install Stable Diffusion WebUI
        char_cmd = f"wget -q -O {str(path)}/webui.sh https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui/master/webui.sh"
        os.system(char_cmd)
        char_cmd = f"bash {str(path)}/webui.sh -f --port {str(port)} --exit"
        if (args is None):
            for k,v in kwargs.items():
                char_cmd = f"{char_cmd} --{str(k)}"
                if (str(v) != ""):
                    char_cmd = f"{char_cmd} {str(v)}"
        else:
            if (len(kwargs) > 0):
                warnings.warn(message = "Extra arguments will be discarded when using the args parameter!",category = UserWarning)
            char_cmd = f"{char_cmd} {str(args)}"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install Stable Diffusion WebUI: \n")
            print(exec_logging)

        # run Stable Diffusion WebUI
        char_cmd = f"bash {str(path)}/webui.sh -f --port {str(port)}"
        if (args is None):
            for k,v in kwargs.items():
                char_cmd = f"{char_cmd} --{str(k)}"
                if (str(v) != ""):
                    char_cmd = f"{char_cmd} {str(v)}"
        else:
            char_cmd = f"{char_cmd} {str(args)}"
        char_cmd = f"nohup {char_cmd} > /tmp/{str(self.path)}/Stable_Diffusion_WebUI.log 2>&1 &"
        os.system(char_cmd)
        os.system("sleep 30")
        exec_logging = f"Stable Diffusion WebUI log file: /tmp/{str(self.path)}/Stable_Diffusion_WebUI.log."
        print(exec_logging)

    ##################
    ## other method ##
    ##################

    # keep the Colab session busy
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
        i = 1

        # while loop
        while busy:
            print(f"round {str(i)}")
            i = i + 1
            time.sleep(60)

    # install Miniconda
    def Install_Miniconda(self,path = None,verbose = True):
        """
        Install Miniconda on Colab.

        Miniconda is a free and minimal installer for the conda package manager and is frequently used in scientific computing.
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
            path = f"/home/{str(self.user)}"
        char_cmd = f"sudo -u {str(self.user)} mkdir -p {str(path)}"
        os.system(char_cmd)

        # get shell script path
        script_path = os.path.dirname(__file__)
        script_path = os.path.join(script_path,"shell_scripts","Install_Miniconda.sh")

        # install Miniconda
        char_cmd = f"sudo -u {str(self.user)} bash {str(script_path)} {str(self.user)} {str(path)}"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install Miniconda: \n")
            print(exec_logging)

    # install udocker
    def Install_udocker(self,verbose = True):
        """
        Install udocker on Colab.

        udocker is a basic user tool to execute simple docker images in user space without requiring root privilege.
        udocker can also run inside a docker container, making it a perfect tool for executing docker images on Colab.

        Parameters
        ----------
        verbose : bool, optional
            Whether to show the running logs.
        """

        # install udocker
        char_cmd = f"pip install udocker && sudo -u {str(self.user)} udocker --allow-root install"
        exec_logging = os.popen(char_cmd)
        exec_logging = "".join(exec_logging.readlines())
        if verbose:
            print("Install udocker: \n")
            print(exec_logging)

#########################
## define other method ##
#########################

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
    exec_logging = "".join(exec_logging.readlines())
    if verbose:
        print("apt update: \n")
        print(exec_logging)
    exec_logging = os.popen("apt upgrade -y")
    exec_logging = "".join(exec_logging.readlines())
    if verbose:
        print("apt upgrade: \n")
        print(exec_logging)
    exec_logging = os.popen("apt autoremove -y")
    exec_logging = "".join(exec_logging.readlines())
    if verbose:
        print("apt autoremove: \n")
        print(exec_logging)

############################
## define Exception class ##
############################

# RootUserError
class RootUserError(Exception):
    """Exception raised when the ColabSession user is root."""

    def __init__(self,message = "Cannot proceed under ColabSession user root!"):
        super().__init__(message)

# SudoPermissionError
class SudoPermissionError(Exception):
    """Exception raised when the ColabSession user lacks sudo permission."""

    def __init__(self,message = "Operation requires sudo privilege from the ColabSession user!"):
        super().__init__(message)
