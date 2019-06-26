To run GE-FSG on Linux, particularly Ubuntu 18.04, please follow the below instruction:

1. Install Mono (https://www.mono-project.com/download/stable/#download-lin) to run C# code on Ubuntu
```
    sudo apt install gnupg ca-certificates
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
    echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
    sudo apt update
    
    sudo apt install mono-devel
```
2. Run "python main.py"
