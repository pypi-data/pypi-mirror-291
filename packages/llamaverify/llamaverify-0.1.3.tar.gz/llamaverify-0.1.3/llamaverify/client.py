# llamaverify/client.py
from huggingface_hub import InferenceClient 
import requests
from typing import List

class Client:
    def __init__(self,llamaverify_api_key):
        self.api_key_frontend=llamaverify_api_key
        return

    def callDehallucinateEndpoint(self, sources: List[str] =None , summary: str = None):

              # Define the endpoint URL
      url = 'http://127.0.0.1:5000//dehallucinate?api_key=' + self.api_key_frontend

      if summary:
          url=url+"&summary="+ summary
      if sources:
          url=url+ "&sources=" + str(sources)
          
      try:
          # Send the GET request
          response = requests.get(url)
          
          # Check if the request was successful
          if response.status_code == 200:
              # Get the response text
              data = response.text
            #   print("Data received:", data)
                 # Extract the old_score, new_score, and new_summary from the response
              old_score = float (data.split("Old Score:")[1].split("\n")[0].strip())
              new_score = float (data.split("New Score:")[1].split("\n")[0].strip())
              new_summary = data.split("Corrected Summary:")[1].strip()
              return [old_score,new_score], new_summary
          else:
              print(f"Request failed with status code: {response.status_code}")

      except requests.exceptions.RequestException as e:
          print(f"Error occurred: {e}")


if __name__ == '__main__':
    ClientInstance=Client(llamaverify_api_key='validKey2')
    scores, newSummary = ClientInstance.callDehallucinateEndpoint()
    print("Scores :    " + str(scores))
    print("New Summary :    "  + newSummary)