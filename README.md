# ColabGeek

ColabGeek Python package is designed to help run useful tools on Google Colab, including web IDE, port forwarding and so on. It is worth noting that this package is also compatible with other Ubuntu operating system based servers, so try this package on other platforms as well.

## Installation

```python
pip install ColabGeek
```

## Get started

First load the ColabGeek module and update all the packages and dependencies in the system.

```python
import ColabGeek

GolabGeek.update_environment()
```

Initiate the Colab session by add linux users and mount Google Drive.

```python
main = ColabGeek.ColabSession(user='Knight',password='midnight',mount_GD=True)
```

***

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

### Run Rstudio server

[Rstudio server](https://posit.co/products/open-source/rstudio-server/) is a web IDE for R programming. With Rstudio server, users can run R scripts, create and manage R projects, develop and test code, and share their work with others. Rstudio server also offers powerful features such as syntax highlighting, code completion, debugging and data visualization.

```python
# ColabGeek.Run_Rstudio_server has the following parameters:
# - port The port you want to run Rstudio on, set to None to use the default port.
# - verbose Show the running logs.

main.Run_Rstudio_server()
```

***

Google Colab does not allow any internet connections to their servers except the official web interface. So, port forwarding methods are required to proxy the web IDE installed.

### localtunnel

```python
# ColabGeek.Run_localtunnel has the following parameters:
# - port The port you want to expose to localtunnel, set to None and you will use the default port.
# - host Check the localtunnel document.
# - subdomain The customized localtunnel URL, check the localtunnel document. (Do not include '_' in the subdomain!)

main.Run_localtunnel()
```

### ngrok

```python
# ColabGeek.Run_ngrok has the following parameters:
# - token The token of your personal ngrok account. Sign up one, it is free.
# - port The port you want to expose to ngrok, set to None and you will use the default port.
# - domain The customized ngrok URL, check the ngrok document.

main.Run_ngrok()
```

For now, all the port forwarding methods built in ColabGeek only accept http protocal. I am still tring to add TCP forwarding methods to ColabGeek. If you have any good ideas and advices, leave an issue.

***

### shadowsocks

Although not allowed by Google and not recommended by myself, building a proxy server using Colab sounds pretty 'Geek'. However, due to the lack of TCP forwarding method, ColabGeek can now only install shadowsocks on Colab but have no method to help to connect it. Just use this method on your own Ubuntu servers, that should work.

```python
# ColabGeek.Run_shadowsocks has the following parameters:
# - port The server port of shadowsocks, set to None and you will use the default port.
# - password The shadowsocks password.
# - encrypt The shadowsocks encrypt method.

main.Run_shadowsocks()
```

## Statement

ColabGeek violated numerous community rules of Google Colab. But still, I developed ColabGeek, because the simple Jupyter interface just does not meet the requirements of many software applications and is not user-friendly for coding in non-Python languages. I recommend all ColabGeek users can purchase Colab Pro or Pro+ to support the excellent services provided by Google. Keep in mind, avoid misuse and Don't Be Evil.