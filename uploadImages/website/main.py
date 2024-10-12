from distutils.log import debug 
from fileinput import filename 
from flask import *  
import os

app = Flask(__name__)   
  
@app.route('/')   
def main():   
    return render_template("index.html")   
  
@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        file_path = os.path.join("/website/images", f.filename)
        
        f.save(file_path)   

        return render_template("index.html", name = f.filename)   
  
if __name__ == '__main__':   
    app.run(host="0.0.0.0", debug=True)