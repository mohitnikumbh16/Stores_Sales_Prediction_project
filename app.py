from flask import Flask
from bigmart.logger import logging
from bigmart.exception import BigmartException
import sys

app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    try:
        raise Exception("We are testing custom exception")
    except Exception as e:
        bigmart=BigmartException(e,sys)
        logging.info(bigmart.error_message)
        logging.info("We are testing logging module")
    return "ci/cd pipeline created"

if __name__== "__main__":
    app.run(debug=True)
    