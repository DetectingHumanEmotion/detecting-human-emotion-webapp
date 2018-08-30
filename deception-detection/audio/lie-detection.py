from pyAudioAnalysis import audioTrainTest as aT
import threading
import os

EXPECTED = {"0.0":"truth" , "1.0":"lie"}

def get_files_in_directory(dir, file_extension=".wav",):
    """
    Gets all the files in a specified directory


    :param dir: the name of the directory where the files are located
    :param file_extension: the type of files in the directory. default wav
    :return: list of file_names and their paths
    """

    directory = os.fsencode(dir)
    directory = directory.decode("utf-8")
    files = []

    i = 0
    for f in os.listdir(directory):
        filename = os.fsdecode(f)

        if filename.endswith(file_extension):
            dir_and_file =  os.path.join(directory, filename)
            # print(dir_and_file)
            files.insert(i ,dir_and_file)
            i+= 1
            continue
        else:
            continue

    return files

def classify_dir(dir,trained_machine_name,trained_machine_algorithm, file_extension=".wav"):
    """
    This classifies every file within a specified directory and prints / writes results.


    :param dir: Directory that we want every file (.wav) to be specified
    :param trained_machine_name: The name of the machine that has been trained
    :param trained_machine_algorithm: The type of algorithm used to train the machine (knn,svm,extratrees,gradientboosting,randomforest)
    :param file_extension: the types of files being read. default files are .wav type
    :return: void
    """

    #get all files in the directory
    files_in_directory = get_files_in_directory(dir,file_extension)

    #clear old file
    with open(trained_machine_algorithm + "-results"+ ".txt", "w") as f:
        f.write("")

    #counts the number of correctly predicted emotions
    correct = 0

    #loop through all the files in the directory
    for file in files_in_directory:

        #classify the .wav file
        #dominate_result: dominate emotion in classification
        dominate_result, statistics, paths =aT.fileClassification(file,trained_machine_name,trained_machine_algorithm)

        #make sure dominate_result has tenth location then convert to string (this is used when finding hte key in the EMOTIONS map)
        dominate_result= str(format(dominate_result,'.1f'))

        #Conver to list
        statistics = list(statistics)

        #convert to list
        paths = list(paths)

        dominate_result = EXPECTED.get(dominate_result)

        (file,file) = file.split('\\')
        print(file.split("_"))
        (trash, expected, trash) = file.split("_")

        if expected == dominate_result:
            correct += 1


        with open(trained_machine_algorithm + "-results" +".txt","a+") as f:

            print(file)
            print("File results: " + str(trained_machine_algorithm) + ".txt")
            print("Expected: " + expected)
            print("Dominate result: "+ dominate_result)
            print("[truth,lie]")
            print(str(statistics)+"\n" )

            f.write(file + "\n")
            f.write("File results: " + str(trained_machine_algorithm) + ".txt" + "\n")
            f.write("Expected: " + expected)
            f.write("Dominate result: "+ dominate_result +"\n")
            f.write("[truth,lie]" + "\n")
            f.write(str(statistics)+"\n")
            f.write('\n')


    with open(trained_machine_algorithm + "-results" + ".txt", "a+") as f:
        print("Correct classifications: " + str(correct) + " Out of " + str(len(files_in_directory)))
        f.write("Correct classifications: " + str(correct) + " Out of " + str(len(files_in_directory)))

    print("File results: " + trained_machine_algorithm + ".txt")

def main():
    truth_audio_path = "../../training-data/deception-audio/truth_audio"
    lie_audio_path = "../../training-data/deception-audio/lie_audio"

    # train model
    aT.featureAndTrain([truth_audio_path,lie_audio_path], 1.0,1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "deceptionSvm", False)
    aT.featureAndTrain([truth_audio_path,lie_audio_path], 1.0,1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "deceptionKNN", False)
    aT.featureAndTrain([truth_audio_path,lie_audio_path], 1.0,1.0, aT.shortTermWindow, aT.shortTermStep, "randomforest", "deceptionRandomForest", False)
    aT.featureAndTrain([truth_audio_path,lie_audio_path], 1.0,1.0, aT.shortTermWindow, aT.shortTermStep, "gradientboosting", "deceptionGradientBoosting", False)
    aT.featureAndTrain([truth_audio_path,lie_audio_path], 1.0,1.0, aT.shortTermWindow, aT.shortTermStep, "extratrees", "deceptionExtraTrees", False)




    #classify wav files in directory
    # classify_dir("../deception-audio/testing_data", "deceptionSvm", "svm")
    # classify_dir("../deception-audio/testing_data", "deceptionKNN", "knn")
    # classify_dir("../deception-audio/testing_data", "deceptionRandomForest", "randomforest")
    # classify_dir("../deception-audio/testing_data", "deceptionGradientBoosting", "gradientboosting")
    # classify_dir("../deception-audio/testing_data", "deceptionExtraTrees", "extratrees")





main()