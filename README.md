# Moving Light GUI

**_This project is still in BETA. Use at your own risk. Please report all bugs without annoying me:)_**

## What? (is this)

This is a script that can be used as "add-on" for QLC+ or every other Light Controller that uses ArtNet. This "add-on" controls the pan and tilt values of every light.

## Why? (did you do this/do I need it)

I didn't find any tool that did what I want, and now you can use/modify/criticize my script. Very likely, such scripts already exist on the Internet, but probably they do not meet my requirements or are chargeable.

## How? (do I use it)

1. measure the dimensions of the room
2. measure the positions of the moving lights
3. create a event.json
4. create an image with important points marked (.png)
5. start MovingLightGUI.py
   * if you don't add arguments you can choose your files with a filedialog
   * if you need help with command line arguments add --help

any problems? write a message or look ot the "Notes.pdf"

Note on "Notes.pdf": There is a mistake on page 2. (you can compare Notes.pdf and Calculator.py)

### Requirements

To use this tool, a few values must be given:
* Python 3.8 or higher
* Libraries from requirements.txt
* Dimensions of the room (width * height)
* position and orientation of the lights in relation to the room (x,y,z)
* Information about the light (max. pan/tilt angle)
* (optional) some orientation points (also in relation to the room)

## Who? (did this)

TL;DR: Jakob Felix Rieckers

My Name is Jakob Felix Rieckers. I am a licensed amateur radio operator, and I like programming. Together with my brother Janfred (Jan-Frederik Rieckers) we sometimes operate some lights.

My (relevant) social media platforms are:
* Twitter (X): [@DO2JFR](https://twitter.com/DO2JFR)
* Mastodon: [@do2jfr@radiosocial.de ](https://radiosocial.de/@do2jfr)
* Reddit: [u/ham_jaky](https://www.reddit.com/user/ham_jaky/)
* Github: [ham-jaky](github.com/ham-jaky)

## License

MIT License

Copyright (c) 2023 Jakob Felix Rieckers