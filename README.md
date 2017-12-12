[![Build Status](https://travis-ci.org/ebritsyn/obormot.svg?branch=master)](https://travis-ci.org/ebritsyn/obormot)
[![codecov](https://codecov.io/gh/ebritsyn/obormot/branch/master/graph/badge.svg)](https://codecov.io/gh/ebritsyn/obormot)

# Obormot

Obormot is a telegram bot that receives a picture, detects faces in that 
picture and predicts if they are smiling or neutral. It obtains faces 
bounding boxes, draws them on the input image and set corresponding 
labels (emojis :smiling: and :neutral:) on found faces 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need following python libraries to use the bot

```
numpy
python-telegram-bot
opencv-python
dlib
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

To run tests do following steps in console:

```
cd tests
python setup.py test
```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds


## Versioning

TBD 

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

TBD
* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
