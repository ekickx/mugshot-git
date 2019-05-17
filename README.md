# About
Mugshot is a lightweight user configuration utility that allows you to easily 
update personal user details. The original repo is at https://launchpad.net/mugshot

# Difference
For now the difference from recent mugshot(0.4.1) just is:
- Circle crop

![circle_crop](https://i.imgur.com/l3v5tMo.png )

# TODO
- Add feature to move cropped area
- Add feature to zoom cropped area

# Build and Install
### Dependencies: 
- chfn, 
- python3-gi, 
- python3-pexpect, 
- python3-dbus, 
- python3-cairo
- gstreamer1.0-plugins-good, (optional)
- gstreamer1.0-tools, (optional)
- gir1.2-cheese-3.0, (optional)
- gir1.2-gtkclutter-1.0, (optional)
## System Install
- First install all the dependencies
- Clone this repo
```
git clone https://github.com/ekickx/mugshot-git.git
```
- Enter directory
```
cd mugshot-git
```
- Build and install
```
python3 setup.py build
sudo python3 setup.py install
```
NOTE: If you get the following error:

(mugshot:22748): GLib-GIO-ERROR **: Settings schema 'apps.mugshot' is not installed

be sure to copy data/glib-2.0/schemas/apps.mugshot.gschema.xml to either:
/usr/share/glib-2.0/schemas, or
/usr/local/share/glib-2.0/schemas

and run glib-compile-schemas on that directory before running.
## Virtual Environment Install (Recommended)
Virtualenv is a tool which allows us to make isolated python environments. It prevents `mugshot` to break your system if something goes wrong
- First install virtualenv and pip
```
sudo apt install virtualenv python3-virtualenv python3-pip
```
- Clone this repo
```
git clone https://github.com/ekickx/mugshot-git.git
```
- Enter directory
```
cd mugshot-git
```
- Create and activate virtualenv
```
virtualenv -p python3 virtual_env
source virtual_env/bin/activate
```
- Install the dependency(distutils)
```
wget https://launchpadlibrarian.net/236120080/python-distutils-extra-2.39.tar.gz
tar -xvzf python-distutils-extra-2.39.tar.gz
python python-distutils-extra-2.39/setup.py
rm -r python-distutils-extra-2.39
```
- Install the rest dependencies
```
pip install pygobject pexpect dbus-python
```
- Build and install
```
python setup.py build
python setup.py install
```
- To run the program type 
```
/path_to_virtualenv/bin/mugshot
```
