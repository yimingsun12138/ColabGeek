# ColabGeek

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/yimingsun12138/ColabGeek/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/ColabGeek.svg)](https://badge.fury.io/py/ColabGeek)

ColabGeek Python package is designed to help run useful tools on Google Colab, including web IDE, port forwarding and so on. It is worth noting that this package is also compatible with other Ubuntu operating system based servers, so try this package on other platforms as well.

## Installation

```python
pip install ColabGeek
```

## Get started

First load the ColabGeek module and update all the packages and dependencies in the system.

```python
import ColabGeek

ColabGeek.update_environment()
```

Initiate the Colab session by add linux users and mount Google Drive.

```python
main = ColabGeek.ColabSession(user='Knight',password='midnight',mount_GD=True)
```

As a cloud computing platform based on Jupyter notebooks, Google Colab does not provide a top-notch comfortable environment for R language data analysis and other non-Python programming. Therefore, this project provides a method for quickly installing other web IDE on Google Colab, enabling it to expand its range of capabilities.

### Run code server

[code server](https://github.com/coder/code-server) is a web IDE provided by Coder that enables developers to write, run and debug code from a web browser. It is built on the open-source Visual Studio Code editor and offers many of the same features, such as code highlighting, auto completion, and debugging.

```python
# ColabGeek.Run_code_server has the following parameters:
# - port The port you want to run code server on, set to None to use the default port.
# - password The code server login password, set to None and use the linux user password by default.
# - verbose Show the running logs.

main.Run_code_server()
```

You can also install code server extension by providing extension id or the path of the VSIX file downloaded from [vscode marketplace](https://marketplace.visualstudio.com/vscode).

```python
# ColabGeek.Install_code_server_extension has the following parameters:
# - extension The extension id or the path of the VSIX file.
# - verbose Show the running logs.

main.Install_code_server_extension(extension='ms-python.anaconda-extension-pack')
```

You can also config code server through `ColabGeek.Config_code_server` method.

```python
# ColabGeek.Config_code_server has the following parameters:
# - property Matching the key in settings.json config file.
# - value Matching the value in settings.json config file.

main.Config_code_server(property='workbench.colorTheme',value='Default Dark+')
main.Config_code_server(property='editor.fontSize',value=18)
main.Config_code_server(property='terminal.integrated.fontSize',value=18)
main.Config_code_server(property='files.autoSave',value='off')
```

### Run Rstudio server

[Rstudio server](https://posit.co/products/open-source/rstudio-server/) is a web IDE for R programming. With Rstudio server, users can run R scripts, create and manage R projects, develop and test code, and share their work with others. Rstudio server also offers powerful features such as syntax highlighting, code completion, debugging and data visualization.

```python
# ColabGeek.Run_Rstudio_server has the following parameters:
# - port The port you want to run Rstudio on, set to None to use the default port.
# - verbose Show the running logs.

main.Run_Rstudio_server()
```

Google Colab does not allow any internet connections to their servers except the official web interface. So, port forwarding methods are required to proxy the web IDE installed.

### localtunnel

```python
# ColabGeek.Run_localtunnel has the following parameters:
# - port The port you want to expose to localtunnel, set to None and you will use the default port.
# - host Check the localtunnel document.
# - subdomain The customized localtunnel URL, check the localtunnel document. (Do not include '_' in the subdomain!)
# - verbose Show the running logs.

main.Run_localtunnel()
```

### ngrok

```python
# ColabGeek.Run_ngrok has the following parameters:
# - token The token of your personal ngrok account. Sign up one, it is free.
# - port The port you want to expose to ngrok, set to None and you will use the default port.
# - domain The customized ngrok URL, check the ngrok document.
# - verbose Show the running logs.

main.Run_ngrok()
```

For now, all the port forwarding methods built in ColabGeek only accept http protocal. I am still tring to add TCP forwarding methods to ColabGeek. If you have any good ideas and advices, leave an issue.

### shadowsocks

Although not allowed by Google and not recommended by myself, building a proxy server using Colab sounds pretty 'Geek'. However, due to the lack of TCP forwarding method, ColabGeek can now only install shadowsocks on Colab but have no method to help to connect it. Just use this method on your own Ubuntu servers, that should work.

```python
# ColabGeek.Run_shadowsocks has the following parameters:
# - port The server port of shadowsocks, set to None and you will use the default port.
# - password The shadowsocks password.
# - encrypt The shadowsocks encrypt method.
# - verbose Show the running logs.

main.Run_shadowsocks()
```

### Jekyll

[Jekyll](https://jekyllrb.com/) is a simple, blog-aware, static site generator that allows users to create their own websites or blogs without the need for databases or server-side programming languages. It takes text written in Markdown, processes it through a template engine, and generates a ready-to-publish static website. ColabGeek now provides a method to automatically install Jekyll and all of its dependencies. Users can easily access their Jekyll sites using tunneling methods, also provided by ColabGeek.

```python
# ColabGeek.Install_Jekyll has the following parameters:
# - version Which version of Ruby you would like to install? The latest stable version is recommended.
# - verbose Show the running logs.

main.Install_Jekyll(version='3.2.2',verbose=True)
```

### Stable Diffusion WebUI

[Stable Diffusion](https://github.com/CompVis/stable-diffusion) is a deep learning, text-to-image model released in 2022 based on diffusion techniques. It is primarily used to generate detailed images conditioned on text descriptions, though it can also be applied to other tasks such as inpainting, outpainting, and generating image-to-image translations guided by a text prompt. [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) is a browser interface for Stable Diffusion that allows to create beautiful art much more easily. Stable Diffusion WebUI can be easily installed through ColabGeek and conveniently accessed using the tunneling method also provided by ColabGeek.

```python
# ColabGeek.Run_stable_diffusion_webui has the following parameters:
# - path The installation path for Stable Diffusion WebUI, which is defaulted to /tmp.
# - port The port you want to run the browser interface on, set to None to use the default port.
# - verbose Show the running logs.
# - args Custom parameters for installing and running Stable Diffusion WebUI.
# - **kwargs Custom parameters for installing and running Stable Diffusion WebUI. Cannot be used in conjunction with the args parameter.

main.Run_stable_diffusion_webui()

# Use tunneling method built in Stable Diffusion WebUI:
# main.Run_stable_diffusion_webui(args='--share --gradio-auth username:password')
# main.Run_stable_diffusion_webui(share='')
```

## Statement

ColabGeek violated numerous community rules of Google Colab. But still, I developed ColabGeek, because the simple Jupyter interface just does not meet the requirements of many software applications and is not user-friendly for coding in non-Python languages. I recommend all ColabGeek users purchase Colab Pro or Pro+ to support the excellent services provided by Google. Keep in mind, avoid misuse and Don't Be Evil.