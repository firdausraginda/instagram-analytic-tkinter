from flask import Flask, render_template, Response, request, redirect, url_for
from mainProgram import mainProg

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST' and request.form['igAcc'] != '':
      igAcc = request.form['igAcc']
      if type(mainProg(igAcc, 10, 5)) != str :
         hasilScrapingComAcc, hasilAccMenByUser, hasilKomenMenarik, hasilSortLike, hasilSortComment = mainProg(igAcc, 10, 5)
         return render_template('displaySucced.html', hasilScrapingComAcc=hasilScrapingComAcc,  hasilAccMenByUser=hasilAccMenByUser,  hasilKomenMenarik=hasilKomenMenarik,  hasilSortLike=hasilSortLike,  hasilSortComment=hasilSortComment)
      else:
         return render_template('displayErr.html', msg = mainProg(igAcc, 10, 5))

   return render_template('index.html')

# @app.route('/')
# def index():
#    return 'ini harusnya jalan'

if __name__ == '__main__':
   app.run(debug = True)