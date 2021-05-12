# image-similarity
`image-similarity` is a tool that divides a group of images according to their similarity grade between them which goes between 0 and 1. 0 means not similar and 1 means that those images are equal. It uses the SSIM method.

    > python .\image-similarity.py
         _____
        |_   _|
          | | _ __ ___   __ _  __ _  ___
          | || '_ ` _ \ / _` |/ _` |/ _ \
         _| || | | | | | (_| | (_| |  __/
         \___/_| |_| |_|\__,_|\__, |\___|
                               __/ |
                              |___/
         _____ _           _ _            _ _
        /  ___(_)         (_) |          (_) |
        \ `--. _ _ __ ___  _| | __ _ _ __ _| |_ _   _
         `--. \ | '_ ` _ \| | |/ _` | '__| | __| | | |
        /\__/ / | | | | | | | | (_| | |  | | |_| |_| |
        \____/|_|_| |_| |_|_|_|\__,_|_|  |_|\__|\__, |
                                                 __/ |
                                                |___/
        
        Loading images from 'images'...
        Dividing images in batches according to similarity (0.95)...
        Saving images in 'output'...
        Done.
# Getting Started
To get the repository, run:

     git clone https://github.com/codexgigassys/image-similarity.git

# Prerequisites
To install all Python (3.9 <= ) required modules, please run:

     pip install -r requirements.txt
   
# Running
First, you need a directory with images. You can save them inside `images `directory or you can create your own folder outside the script main folder. In case you do the later option, when you run the script, you pass the argument `--imagesDirectory pathToImages` (it works with relative and absolute paths).

Once the script is done, you have the result inside `output` directory or you can create your own folder passing the argument `--outputDirectory pathToSaveOutput`. If the folder doesn't exist, the script will create it.

Remember that similarity grade goes between 0 and 1. By default, this value is 0.95. In case you want to use another value, pass the argument `--similarityGrade valueBetween0And1`.

A complete script running is:

    python .\image-similarity.py --similarityGrade aValidValue --imagesDirectory pathToImages --outputDirectory pathToSaveOutput 

# Get Help
To get help:

    python .\image-similarity.py --help