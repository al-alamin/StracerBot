from flask import Flask, render_template, request
import os, sys
import time

app = Flask(__name__)
print("Flask App initiated.")



class URL:
  def __init__(self, url, title):
    self.url = url
    self.title = title

urls = [URL("https://stackoverflow.com/questions/11556958/s", "Question something"), URL("https://stackoverflow.com/questions/11556958/s", "Question 2"), URL("https://stackoverflow.com/questions/11556958/s", "Question 3")]

def setup_environment():
        print("#" * 20)
        print("Expensive setup method")
        os.environ["INITIALIZED"] = "True"
        time.sleep(30)
        print("Environment setup finished")
        


def get_result(error_message):

    return urls

@app.route("/", methods=['post', 'get'])
def home():
    result = 'Welcome'
    if request.method == 'POST':
        error_message = request.form.get('error_message')  # access the data inside
        result = get_result(error_message)


    return render_template("index.html", result = result)

if __name__ == "__main__":
    print("================================> Main method")
    print(os.environ.get("INITIALIZED"))
    if os.environ.get("INITIALIZED") != "True":    
        setup_environment()
    else:
        print("The environment has been setup already")
    app.run(debug=True)