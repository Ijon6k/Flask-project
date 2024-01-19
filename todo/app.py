from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')

# Ganti struktur data todos
todos = {
    'Muhammad An Ghafari (50423858)': [],
    'Astrela Nydia Hutasuhut (50423220)': [],
    'Adam Febriansyah (50423032)': [],
    'Zulfitrah Fajar (51423510)': []
}

# Jika ingin membuat secara dinamis dengan nama default 'member'
# todos = {'member' + str(i): [] for i in range(1, 21)}

# Contoh print keys
print(list(todos.keys()))


@app.route('/')
def index():
    return render_template('index.html', todos=todos)

# Ubah fungsi add untuk menambahkan tugas ke anggota kelompok yang bersangkutan
@app.route('/add', methods=['POST'])
def add():
    todo = request.form['todo']
    member = request.form['member']
    todos[member].append({'task': todo, 'done': False})
    return redirect(url_for('index'))

# Ubah fungsi edit untuk mengedit tugas anggota kelompok yang bersangkutan
@app.route('/edit/<member>/<int:index>', methods=['GET', 'POST'])
def edit(member, index):
    todo = todos[member][index]
    if request.method == 'POST':
        todo['task'] = request.form['todo']
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', todo=todo, index=index, member=member)

# Ubah fungsi check untuk menandai tugas sebagai selesai untuk anggota kelompok yang bersangkutan
@app.route('/check/<member>/<int:index>')
def check(member, index):
    todos[member][index]['done'] = not todos[member][index]['done']
    return redirect(url_for('index'))


@app.route('/delete/<member>/<int:index>')
def delete(member, index):
    del todos[member][index]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
