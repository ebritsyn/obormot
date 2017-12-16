[![Build Status](https://travis-ci.org/ebritsyn/obormot.svg?branch=master)](https://travis-ci.org/ebritsyn/obormot)
[![codecov](https://codecov.io/gh/ebritsyn/obormot/branch/master/graph/badge.svg)](https://codecov.io/gh/ebritsyn/obormot)

# Obormot

Obormot is a telegram bot that receives a picture, detects faces in that 
picture and predicts if they are smiling or neutral. It obtains faces 
bounding boxes, draws them in the input image and sets corresponding 
labels (emojis :smiling: and :neutral:) on found faces 

### Prerequisites

You need to install the following python libraries to run the bot on your machine

```
numpy
python-telegram-bot
opencv-python
dlib
```

## Running the tests

To run tests do the following steps in console:

```
python setup.py test
```

## Versioning

TBD 

## Authors

* **Eugene Britsyn** - *Initial work* - [ebritsyn](https://github.com/ebritsyn/)
* **Artemiy Luzyanin** - *Initial work* - [artemluzyanin](https://github.com/artemluzyanin)
* **Sergey Rassolov** - *Initial work* - [RassolovSerg](https://github.com/RassolovSerg)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
