from flask import Flask
from flask import render_template;

app = Flask(__name__)

# home pacage
@app.route("/", methods = ['GET', 'POST'])
def home():
    return render_template("index.html")


if __name__ == '__main__':
  '''
  sinfo = py_sinfo()
  print("sinfo:\n", sinfo)
  sjob = ("sjob", py_job("terencelau"))
  print("your tasks/jobs:\n", sjob)
  '''
  #app.run()
  app.run(host="0.0.0.0", port=8076, debug=True)
