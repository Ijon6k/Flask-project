from flask import Flask, render_template, request

app = Flask(__name__)

anggota = []
database_kelompok = []


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/inputgrade')
def inputgrade():
    return render_template("inputgrade.html", anggota=anggota, database_kelompok=database_kelompok)


@app.route('/create_group', methods=['POST'])
def create_group():
    group_name = request.form.get('group_name')
    group_members = [member.strip() for member in request.form.get('group_members').split(',')]

    new_group = {'name': group_name, 'members': group_members, 'members_data': []}
    database_kelompok.append(new_group)

    return render_template('index.html', new_group=new_group)


@app.route('/list', methods=['GET'])
def list_group():
    global database_kelompok
    global anggota
    return render_template('listgrp.html', database_kelompok=database_kelompok)


@app.route('/calculate_average', methods=['POST'])
def calculate_average():
    for group in database_kelompok:
        for member_data in group['members_data']:
            nilai = request.form.get(f"{group['name']}_{member_data['name']}")
            nilai = [int(x) for x in nilai.split() if x and int(x) != 0]
            member_data['nilai'] = nilai
            member_data['average'] = sum(nilai) / len(nilai) if nilai else None

    return render_template("inputgrade.html", anggota=anggota, database_kelompok=database_kelompok, members_data=group['members_data'])


@app.route('/inputgrade', methods=['POST'])
def reset_to_index():
    return render_template('inputgrade.html')


@app.route('/list', methods=['POST'])
def reset_to_group():
    global database_kelompok
    database_kelompok = []
    return render_template('listgrp.html', anggota=anggota, database_kelompok=database_kelompok)


if __name__ == '__main__':
    app.run(debug=True)
