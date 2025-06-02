from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    time = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))
    status = db.Column(db.String, default="Pending")
    def __repr__(self):
        return f"{self.id}: {self.title}"
    
with app.app_context():
    db.create_all()
    
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        new_task = Task(title=title, desc=desc)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    
    all_tasks = Task.query.all() 
    pending_tasks = Task.query.filter_by(status="Pending").all()
    completed_tasks = Task.query.filter_by(status="Completed").all()
    return render_template("index.html", all_tasks=all_tasks, pending_tasks=pending_tasks, completed_tasks=completed_tasks)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = Task.query.get_or_404(id)
    if request.method == "POST":
        task.title = request.form['title']
        task.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", task=task)

@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/toggle/<int:id>")
def toggle(id):
    task = Task.query.get_or_404(id)
    task.status = "Completed" if task.status == "Pending" else "Pending"
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)