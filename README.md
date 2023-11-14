<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/MIMUSA-test/UI">
    <!-- <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
  </a>

<h3 align="center">PROJECT MIMUSA</h3>

  <p align="center">
    project_description
    <br />
    <!-- <a href="https://github.com/MIMUSA-test/Project-MiMuSA"><strong>Explore the docs »</strong></a> -->
    <br />
    <br />
    <a href="https://mimusa-test.github.io/Project-MiMuSA/">View Demo</a>
    <!-- · -->
    <!-- <a href="https://github.com/MIMUSA-test/Project-MiMuSA/issues">Report Bug</a> -->
    <!-- · -->
    <!-- <a href="https://github.com/MIMUSA-test/Project-MiMuSA/issues">Request Feature</a> -->
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#current-deployment">Current Deployment</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#setup">Setup</a></li>
        <li><a href="#project-maintenance">Project Maintenance</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

<!-- Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `MIMUSA-test`, `Project-MiMuSA`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description` -->
<Add description here>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Vue][Vue.js]][Vue-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Install the required python libraries with pip
* pip
    ```sh
    cd model
    pip install -r requirements.txt
    ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/MIMUSA-test/Project-MiMuSA.git
   ```
2. Install python packages
    ```sh
    cd model
    pip install -r requirements.txt
   ```
3. Use the local URLs in `config.js`
    ```js
    const model1 = "http://127.0.0.1:8080/generate"
    const model2 = "http://127.0.0.1:8080/generate2"
    ```
4. Run the app
    ```sh
    cd model
    python app.py
    ```
5. Open the `index.html` file in your browser

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Setup -->
## Current Deployment

Below is the documentation of how this project was setup and is currently used as an online version.

### Prerequisites

#### Amazon Cloud Services [(AWS)](https://aws.amazon.com/) EC2 instance with Ubuntu 20.04 LTS
1. Create an EC2 instance with Ubuntu 20.04 LTS for Web Server connection
2. Create a security group with the following inbound rules:
    * HTTPS TCP 443
3. Repeat steps 2 and 3 for a second EC2 instance for the Python server

<br/>

#### [GoDaddy](https://www.godaddy.com/en-sg) domain service
1. Purchase a domain name
2. Create a A record with the following settings for a subdomain:
    * Name: model
    * Data: [EC2 Web Server instance public IPv4 address]
    * TTL: 1200 seconds

<br/>



### Setup

#### EC2 Web Server instance
1. Connect/SSH into the EC2 Web Server instance
2. Install [Nginx](https://www.nginx.com/) web server
    ```sh
    sudo apt update
    sudo apt install nginx
    ```
3. Install [Certbot](https://certbot.eff.org/) for HTTPS
    ```sh
    sudo apt install certbot python3-certbot-nginx
    ```
4. Obtain HTTPS certificate
    ```sh
    sudo certbot --nginx -d <YOUR-DOMAIN-NAME> -d <YOUR-SUB-DOMAIN-NAME>
    ```
5. Configure Nginx
    ```sh
    sudo nano /etc/nginx/sites-available/website
    ```
    * Ensure the following settings are configured
        ```sh
        server {
            server_name <YOUR-SUB-DOMAIN-NAME>;

            location / {
                proxy_pass http://<EC2 Python Server Private IPv4 addresses>:8080;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }

            location /generate {
                proxy_pass http://<EC2 Python Server Private IPv4 addresses>:8080;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }

            location /generate2 {
                proxy_pass http://<EC2 Python Server Private IPv4 addresses>:8080;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }

            listen 443 ssl; # managed by Certbot
            ssl_certificate /etc/letsencrypt/live/model.socialopinionanalytics.net/fullchain.pem; # managed by Certbot
            ssl_certificate_key /etc/letsencrypt/live/model.socialopinionanalytics.net/privkey.pem; # managed by Certbot
            include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
            ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
        }

        server {
            if ($host = <YOUR-SUB-DOMAIN-NAME>) {
                return 301 https://$host$request_uri;
            } # managed by Certbot


            listen 80;
            server_name <YOUR-SUB-DOMAIN-NAME>;
            return 404; # managed by Certbot
        }
        ```
    * Run check to ensure no errors
        ```sh
        sudo nginx -t
        ```
5. Restart Nginx
    ```sh
    sudo systemctl restart nginx
    ```

<br/>

#### EC2 Python Server instance
1. Connect/SSH into the EC2 Python Server instance
2. Install [Python](https://www.python.org/) and [pip](https://pypi.org/project/pip/)
    ```sh
    sudo apt install python3-pip
    ```
3. Clone the repo
   ```sh
   git clone https://github.com/MIMUSA-test/Project-MiMuSA.git
   ```
4. Install python packages
    ```sh
    cd model
    pip install -r requirements.txt
    ```
5. Run the app in the background
    ```sh
    cd model
    nohup python3 app.py > app.log 2>&1 &
    ```

<br/>

#### Repo `config.js`
1. Change the `model1` and `model2` URLs to your domain name
    ```js
    const model1 = "https://YOUR-SUB-DOMAIN-NAME/generate"
    const model2 = "https://YOUR-SUB-DOMAIN-NAME/generate2"
    ```

<br/>

#### Github pages
1. Go to the repo settings
2. Under the `GitHub Pages` section, select the `main` branch and `/docs` folder
3. Click `Save`

Demo is now available at https://mimusa-test.github.io/Project-MiMuSA/

<br/>

### Project maintenance

#### HTTPS certificate renewal
1. Connect/SSH into the EC2 Web Server instance
2. Renew HTTPS certificate
    ```sh
    sudo certbot renew
    ```
3. Restart Nginx
    ```sh
    sudo systemctl restart nginx
    ```

<br/>

Setup auto renewal of HTTPS certificate
1. Connect/SSH into the EC2 Web Server instance
2. Create a cron job
    ```sh
    sudo crontab -e
    ```
3. Add the following line to the end of the file (Renews every 3 months)
    ```sh
    0 0 1 */3 * certbot renew
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Glen Low - [@GlenLow](https://t.me/GlenLow) - glen.low.2021@scis.smu.edu.sg

Seah Yok Sim - [@yok_ys](https://t.me/yok_ys) - yoksim.seah.2021@scis.smu.edu.sg

Project Link: [https://github.com/MIMUSA-test/Project-MiMuSA](https://github.com/MIMUSA-test/Project-MiMuSA)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This research was supported by SMU under IS470 Guided Research in Computing as well as the Undergraduate Research (UResearch) in Computing Programme.
<br/>
The authors would like to thank WANG Zhaoxia in her guidance and sharing of resources and ideas; SUN Jun for his assistance and guidance in the entire research process.

MiMuSA reference paper can be found here: https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=8956&context=sis_research
<br/>
MiMuSA 2 paper has yet to be published.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/MIMUSA-test/Project-MiMuSA.svg?style=for-the-badge
[contributors-url]: https://github.com/mimusa-test/Project-MiMuSA/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/MIMUSA-test/Project-MiMuSA.svg?style=for-the-badge
[forks-url]: https://github.com/MIMUSA-test/Project-MiMuSA/network/members
[stars-shield]: https://img.shields.io/github/stars/MIMUSA-test/Project-MiMuSA.svg?style=for-the-badge
[stars-url]: https://github.com/MIMUSA-test/Project-MiMuSA/stargazers
[issues-shield]: https://img.shields.io/github/issues/MIMUSA-test/Project-MiMuSA.svg?style=for-the-badge
[issues-url]: https://github.com/MIMUSA-test/Project-MiMuSA/issues
[license-shield]: https://img.shields.io/github/license/MIMUSA-test/Project-MiMuSA.svg?style=for-the-badge
[license-url]: https://github.com/MIMUSA-test/Project-MiMuSA/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com