# Accident-Detection-System
This is an Accident Detection System. I will continously Monitor Your Phones Accelerometer and if an sudden impact on the Phone is detected shows dialog for confirmation and then send sms to emergency services.

You Need to use Linux OS or Google Colab(if you are windows user)

In Linux,

1. Install python 3.11
2. Intall Buildozer from Official Website. ( https://buildozer.readthedocs.io/en/latest/installation.html )
3. Download All Folders and Files.
4. Open Terminal where all files are stored.
5. Copy , Paste following Commands:
    - buildozer -v android debug
6. APK file will generate inside the bin folder.


In Windows,

1. Open Google Colab.
2. upload all files.
3. copy , paste Following Commands.
<pre>
- Create a cell and paste below commands.
    
!sudo apt update
!sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
!pip3 install --user --upgrade Cython==0.29.33 virtualenv

- Create cell 2

# git clone, for working on buildozer
!git clone https://github.com/kivy/buildozer
%cd buildozer
!python setup.py build
!pip install -e .
%cd ..

- Create cell 3
!buildozer -v android debug

</pre>
