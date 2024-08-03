from flask import Flask, render_template, request, redirect, url_for #Flask çerçevesinden gerekli modülleri içe aktarıyoruz. Flask uygulama oluşturmak için, render_template HTML şablonlarını render etmek için,
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.order_by(User.score.desc()).all() # Puanlarına göre azalan sırada kullanıcıları getiriyoruz
    return render_template('index.html', users=users) # Kullanıcıları 'index.html' şablonuna gönderiyoruz


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        name = request.form['name']
        score = calculate_score(request.form)  # Puanı hesaplıyor
        user = User(name=name, score=score) # Yeni bir User nesnesi oluşturuyor
        db.session.add(user) # Veritabanı oturumuna ekliyor
        db.session.commit() # Değişiklikleri kaydediyor
        return redirect(url_for('result', user_id=user.id))  # Sonuç sayfasına yönlendiriyor
    return render_template('quiz.html')

@app.route('/result/<int:user_id>')
def result(user_id):
    user = User.query.get(user_id)
    return render_template('result.html', user=user)

def calculate_score(form_data):
    score = 0
    if form_data['color'] == 'Blue':
        score += 1
    if form_data['animal'] == 'Dog':
        score += 1
    if form_data['hobbies'].strip():
        score += 1
    return score

  # Flask uygulamasını çalıştırıyoruz; debug modunu açıyoruz
if __name__ == '__main__':
    app.run(debug=True)
