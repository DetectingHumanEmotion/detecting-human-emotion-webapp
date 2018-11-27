"""
Created by tybruno

This file contains all the parsing functions
"""


def parse_emotion_audio_result(results):
    """
    developed by tybruno

    Parses the data received from the emotion classification
    :param results: the raw results given from classification
    :return: list with parsed results
    """
    AUDIO_EMOTION_DOMINATE_RESULT = {0: "Neatural", 1: "Calm", 2: "Happy", 3: "Sad", 4: "Angry", 5: "Fear",
                                     6: "Disgust",
                                     8: "Surprise"}

    dominate_result_int, result_statistics, paths = results
    dominate_result = AUDIO_EMOTION_DOMINATE_RESULT.get(dominate_result_int)

    new_statistics = []
    for result in result_statistics:
        temp_string = "{:.1%}".format(result)
        new_statistics.append(temp_string)

    #dominate_result is the result that was dominate. i.e. sad
    #new_statistics shows the percentages of each of the classification. i.e. sad: 70% happy: 10% angry: 20%
    return [dominate_result, new_statistics]


def parse_deception_audio_result(results):
    """
    developed by tybruno

    Parses the raw results obtained from the deception audio classification.
    :param results: Raw results from classification
    :return: the parsed results as a list.
    """
    AUDIO_DECEPTION_DOMINATE_RESULT = {0: "Truth", 1: "Lie"}

    dominate_result_int, result_statistics, paths = results
    dominate_result = AUDIO_DECEPTION_DOMINATE_RESULT.get(dominate_result_int)

    new_statistics = []
    for result in result_statistics:
        temp_string = "{:.1%}".format(result)
        new_statistics.append(temp_string)


    #dominate_result is the result that was dominate. i.e. truth
    #new_statistics shows the percentages of each of the classification. i.e. truth: 80% lie: 20%
    return [dominate_result, new_statistics]


def pretty_results_deception(results):
    dominate_result = results[0]
    statistics = results[1]

    pretty_results = f'Dominate Trait: {dominate_result}  \nTruth: {statistics[0]} Lie: {statistics[1]}\n'

    return pretty_results
def pretty_results_emotion(results):
    dominate_result = results[0]
    statistics = results[1]

    pretty_results = f'Dominate Trait: {dominate_result}  \nNeutral: {statistics[0]}, Calm: {statistics[1]}, Happy: {statistics[2]}, Sad: {statistics[3]}, Angry: {statistics[4]}, Fear: {statistics[5]}, Disgust: {statistics[6]}\n'
    return pretty_results

def _printing_tester():
    ugly = ['Lie', ['0.3%', '99.7%']]
    print(pretty_results_deception(ugly))

    ugly_emotion = ['Calm', ['6.0%', '20.6%', '16.8%', '17.0%', '15.4%', '9.2%', '11.2%', '3.8%']]
    print(pretty_results_emotion(ugly_emotion))