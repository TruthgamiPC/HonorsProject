# Code functionalities
## Code files
- [main.py](https://github.com/TruthgamiPC/HonorsProject/blob/main/app/services/main.py) - The core of my project, this is the starter script and contains the "App" class which controls the GUI, the Main Page that includes camera methods and the Settings Page.
- [vision_translate.py](https://github.com/TruthgamiPC/HonorsProject/blob/main/app/services/vision_translate.py) - File containing the GUI of both Translation and History Page.
- [improved_vision.py](https://github.com/TruthgamiPC/HonorsProject/blob/main/app/services/improved_vision.py) - Google Vision handling class with functions to translate and containing the os integration of the service key
- [file_reading.py](https://github.com/TruthgamiPC/HonorsProject/blob/main/app/services/file_reading.py) - A file containing a class which targets searching a directory.
- [structures.py](https://github.com/TruthgamiPC/HonorsProject/blob/main/app/services/structures.py) - Data holding classes used in improved_vision.py

## The extra folders
- images - folder contains the original images taken by the camera
- images_bound - folder contains the images with displayed boundaries generated post OCR methods
- text_data - folder contains the text data related to each image that was translated
