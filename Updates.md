# Will update this file with all changes and used it for process track

## Updates through the entirety of March until 26/03/2022

# 1. Key systems were re-planned in sections 2-4 covering all key idea shifts and changes implemented

# 2. The GUI
- GUI implementation was found problematic over the early stages and now have chosen to commit to a more simplistic version which operates smoothly for photo taking and is worked on to work on image listing and translation formats
- This is left for last so final updates expected by mid-April potentially
- Styles are done on whiteboard, will create 'Figma prototypes' in close time to show design (not for scale)

# 3. The core of API's
- During March explored different ways to implement the API calls to the GUI but didn't find any success with it so re-structured the background processes to work independently which is more logical and fitting but required a change of structure
- the 'improved_vision.py' is the entirety of all the API operations, this will have an alternative version in the 'OLD' folder where references to changes can be found.

# 4. File handling
- Initial structure was planned to be focused on using "json" files for but facing issues with translation functions and the full implementation is causing too many issues so for the time being will stick to using simple text files with proper encoding.
- Currently have a good version which works well for the save and contains all the correct information
- On task: working on reading the files in as there are some mechanical difficulties presenting a challenge currently but solution is planned for testing.
