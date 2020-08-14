# Face_Mask_Detector
Detects whether a person is wearing a face mask or not. If someone is found without a mask all access is denied until he/she wears a face mask and also a picture of the culprit is saved with date and time as file name. Also an email feature can be unlocked(by uncommenting the mail section in app.py and providing your email id and password) which will alert the admin about the violation of Face Mask Policy.

## INSTRUCTIONS

1. First Download all the contents in your local drive
2. Open AnacondaPrompt
3. Change the directory to the location of the folder with the help -cd- command
4. pip install -r requirements.txt
5. python app.py
6. An image of the violator will be saved in the static/images folder with the name as "DD_MM_YYYY HH_MM_SS.jpg" when a violator is found.
7. All access will be denied until the violator wears a mask.
8. Also an email can be unlocked by uncommenting the mail-section from the code of app.py
9. To close the application press 'esc' key on the Live Video Feed.
