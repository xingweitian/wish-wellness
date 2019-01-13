import json
from watson_developer_cloud import ToneAnalyzerV3

# If service instance provides API key authentication
service = ToneAnalyzerV3(
    url='https://gateway.watsonplatform.net/tone-analyzer/api',
    version='2017-09-21',
    iam_apikey='q5ML47jd5xtVKZGVzG-sydFMoy_ud1YcTubi49imBuFm')


def tone(input):
    return json.dumps(
        service.tone(
            tone_input=input,
            content_type="text/plain").get_result(),
        indent=2)


if __name__ == '__main__':
    print(tone("Team, I know that times are tough! Product sales have been disappointing for the past three quarters."
               " We have a competitive product, but we need to do a better job of selling it!"))
