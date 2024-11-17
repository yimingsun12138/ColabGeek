# ColabGeek

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/yimingsun12138/ColabGeek/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/ColabGeek.svg)](https://badge.fury.io/py/ColabGeek)

ColabGeek is designed to help run useful tools on Google Colab, including web IDE, port forwarding and so on. It is worth noting that this package is also compatible with other Ubuntu operating system based servers, so try this package on other platforms as well.

## Version info

Version: 1.3.8

Platform: Ubuntu 22.04 LTS

Update: 2024/10/24

## Installation

```python
pip install ColabGeek
```

## Get started

First import ColabGeek and update all the packages and dependencies in the system (Please run under root privilege).

```python
import ColabGeek

ColabGeek.update_environment()
```

Initialize the Colab session by adding a new user (or changing the password for the existing user) and mounting Google Drive.

```python
main = ColabGeek.ColabSession(user = "knight",password = "midnight",mount_GD = True)
```

## Web IDE method

As a cloud computing platform based on Jupyter notebook, Google Colab does not provide a top-notch user-friendly environment for R language data mining and other non-Python programming. Therefore, this project aims to provide methods for quickly installing other web IDEs on Google Colab, enabling it to expand its range of capabilities.

### code server

[code server](https://github.com/coder/code-server) is a web IDE provided by Coder that enables developers to write, run and debug code from a web browser. It is built on the open-source Visual Studio Code editor and offers many of the same features, such as code highlighting, auto completion, and debugging.

```python
# ColabSession.Run_code_server has the following parameters:
# - port Listening port for code server, set to None to use the default port.
# - password The code server login password, set to None to use the ColabSession user password.
# - verbose Whether to show the running logs.

main.Run_code_server()
```

You can also install code server extension by providing extension id or the path of the VSIX file downloaded from [VSCode marketplace](https://marketplace.visualstudio.com/vscode).

```python
# ColabSession.Install_code_server_extension has the following parameters:
# - extension The extension id or the path of the VSIX file.
# - verbose Whether to show the running logs.

main.Install_code_server_extension(extension = "ms-python.anaconda-extension-pack")
```

You can also configure code server through `ColabSession.Config_code_server` method.

```python
# ColabSession.Config_code_server has the following parameters:
# - property Specify the property to be added or updated in the settings.json file.
# - value Specify the value for the corresponding property, can be of any type that is supported by JSON.

main.Config_code_server(property = "workbench.colorTheme",value = "Default Dark+")
main.Config_code_server(property = "editor.fontSize",value = 18)
main.Config_code_server(property = "terminal.integrated.fontSize",value = 18)
main.Config_code_server(property = "files.autoSave",value = "off")
```

### Rstudio server

[Rstudio server](https://posit.co/products/open-source/rstudio-server/) is a web IDE for R programming. With Rstudio server, users can run R scripts, create and manage R projects, develop and test code, and share their work with others. Rstudio server also offers powerful features such as syntax highlighting, code completion, debugging and data visualization.

```python
# ColabSession.Run_Rstudio_server has the following parameters:
# - port Listening port for Rstudio server, set to None to use the default port.
# - verbose Whether to show the running logs.

main.Run_Rstudio_server()
```

### JupyterLab
[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/index.html) is a flexible and extensible web IDE designed to support the entire workflow in data science, scientific computing, and machine learning projects. ColabGeek pulls the [mrdoge/jupyterlab docker image](https://hub.docker.com/r/mrdoge/jupyterlab) from Docker Hub and executes using [udocker](https://github.com/indigo-dc/udocker). Notice that it is not recommended to run udocker and JupyterLab under ColabSession user root.

```python
# ColabSession.Run_JupyterLab has the following parameters:
# - port Listening port for JupyterLab, set to None to use the default port.
# - password The JupyterLab login password, set to None to use the ColabSession user password.
# - mount_Colab Whether to map the Colab /content directory to the JupyterLab container /content directory.
# - verbose Whether to show the running logs.

main.Run_JupyterLab()
```

## Tunnelling method

Google Colab does not allow any internet connections to their host servers except the official web interface. Therefore, a tunnelling method is required to access services installed on Colab.

### localtunnel

```python
# ColabSession.Run_localtunnel has the following parameters:
# - port Listening port for localtunnel, set to None to use the default port.
# - host Upstream host server providing forwarding.
# - subdomain Request this subdomain. Do not include the "_" in the subdomain.
# - verbose Whether to show the running logs.

main.Run_localtunnel()
```

### ngrok

```python
# ColabSession.Run_ngrok has the following parameters:
# - token The token of your personal ngrok account.
# - port Listening port for ngrok, set to None to use the default port.
# - domain Request this domain.
# - verbose Whether to show the running logs.

main.Run_ngrok(token = "replace with your own ngrok token!")
```

### Cloudflare Tunnel

```python
# ColabSession.Run_Cloudflare_Tunnel has the following parameters:
# - token The token of your tunnel created on Cloudflare.
# - verbose Whether to show the running logs.

main.Run_Cloudflare_Tunnel(token = "replace with your own tunnel token!")
```

## Other method

### shadowsocks

Although not allowed by Google and not recommended by myself, building a proxy server using Colab sounds pretty "Geek". However, this function only helps to install and run shadowsocks on Colab, and I have no clue how to connect to the shadowsocks server. Just use this method on your own Ubuntu servers, that should work. If you have any good ideas, leave an issue please!

```python
# ColabSession.Run_shadowsocks has the following parameters:
# - port Listening port for shadowsocks server, set to None to use the default port.
# - password The shadowsocks server password, set to None to use the ColabSession user password.
# - encrypt The encryption method for shadowsocks server.
# - verbose Whether to show the running logs.

main.Run_shadowsocks()
```

### Jekyll

[Jekyll](https://jekyllrb.com/) is a simple, blog-aware, static site generator that allows users to create their own websites or blogs without the need for databases or server-side programming languages. It takes text written in Markdown, processes it through a template engine, and generates a ready-to-publish static website. ColabGeek provides a method to automatically install Jekyll and all of its dependencies. Users can easily access their Jekyll websites using tunnelling methods also provided by ColabGeek.

```python
# ColabSession.Install_Jekyll has the following parameters:
# - Ruby_version The version number of Ruby to install.
# - verbose Whether to show the running logs.

main.Install_Jekyll(Ruby_version = "3.3.5",verbose = True)
```

### Stable Diffusion WebUI

[Stable Diffusion](https://github.com/CompVis/stable-diffusion) is a deep learning, text-to-image model released in 2022 based on diffusion techniques. It is primarily used to generate detailed images conditioned on text descriptions, though it can also be applied to other tasks such as inpainting, outpainting, and generating image-to-image translations guided by a text prompt. [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) is a browser interface for Stable Diffusion that allows to create beautiful art much more easily. Stable Diffusion WebUI can be easily installed through ColabGeek and conveniently accessed by the tunnelling methods also provided by ColabGeek.

```python
# ColabSession.Run_Stable_Diffusion_WebUI has the following parameters:
# - path The directory to install Stable Diffusion WebUI. The default path is located in the home of the ColabSession user.
# - port Listening port for Stable Diffusion WebUI, set to None to use the default port.
# - verbose Whether to show the running logs.
# - args Additional arguments to pass to the Stable Diffusion WebUI setup script.
# - **kwargs Additional arguments to pass to the Stable Diffusion WebUI setup script. Cannot be used in conjunction with the args parameter.

main.Run_Stable_Diffusion_WebUI()

# Use tunnelling method built in Stable Diffusion WebUI:
# main.Run_Stable_Diffusion_WebUI(args = "--share --gradio-auth username:password")
# main.Run_Stable_Diffusion_WebUI(share = "")
```

## Statement

ColabGeek has violated numerous community rules of Google Colab. Therefore, users should consider carefully before using ColabGeek, as the author assumes no responsibility for any potential risks. All ColabGeek users are encouraged to consider subscribing Colab Pro or Pro+ to support the excellent services provided by Google. Keep in mind, avoid misuse and Don't Be Evil.
