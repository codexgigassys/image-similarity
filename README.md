[![Image Similarity](https://circleci.com/github/codexgigassys/image-similarity.svg?style=svg)](https://circleci.com/github/codexgigassys/image-similarity)

# imageSimilarity
`imageSimilarity` is a tool that divides a group of images according to their similarity grade between them which goes between 0 and 1. 0 means not similar and 1 means that those images are equal. It uses the SSIM method. Just a interesting fact, the relation of similarity is considered to be **transitive**, **symmetric**, and **reflexive**. It's a key concept utilized when images dividing comes.

    > python .\imageSimilarity.py
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

 1. [Contents](#getting-started)
 2. [Prerequisites](#prerequisites)
 3. [Running](#running)
 4. [Run with docker](#run-with-docker)
 5. [APIs](#apis)
 6. [Get Help](#get-help)

# Getting Started
To get the repository, run:

     git clone https://github.com/codexgigassys/imageSimilarity.git

# Prerequisites
To install all Python (3.9 <= ) required modules, please run:

     pip install -r requirements.txt
   
# Running
First, you need a directory with images. You can save them inside `images `directory or you can create your own folder outside the script main folder. In case you do the later option, when you run the script, you pass the argument `--imagesDirectory pathToImages` (it works with relative and absolute paths).

Once the script is done, you have the result inside `output` directory or you can create your own folder passing the argument `--outputDirectory pathToSaveOutput`. If the folder doesn't exist, the script will create it.

Remember that similarity grade goes between 0 and 1. By default, this value is 0.95. In case you want to use another value, pass the argument `--similarityGrade valueBetween0And1`.

A complete script running is:

    python .\imageSimilarity.py --similarityGrade aValidValue --imagesDirectory pathToImages --
    outputDirectory pathToSaveOutput 

If you wish to log imageSimilarity activities, add `--logging` or just `-l`. All logging related information may be in *imageSimilarity.log*.

# Run with Docker
All you have to do is

    docker-compose up
API of below will be working
# APIs
The script can create a server to hold an API that receives images and then returns a list of lists with similar images hashes. A use case could be (it's exampleCode.py):

    import requests
    import json

    filesDictionary = {
        '01.jpeg': open('images/01.jpeg', 'rb'),
        '02.jpeg': open('images/02.jpeg', 'rb'),
        '05.jpeg': open('images/05.jpeg', 'rb'),
    }

    response = requests.post("http://localhost:9082/api/imageSimilarityByHash",files=filesDictionary,params={'similarity_grade':0.75})

    hashes = json.loads(response.text)['lists']

If you print hashes you can obtain:

    [["52d57c19cc025fe44827e0970fa35d8ba5a5441f", "39e25885c9c11ab8299668569c1162ff610868e9"], ["4dedb7caab44c5b65ba0692cc54a5f2735dee5f4"]]

If you don't pass 'similarity_grade', it will be 0.95.

To run the server, just type:

    python .\imageSimilarity.py --runServer

# Get Help
To get help:

    python .\imageSimilarity.py --help
