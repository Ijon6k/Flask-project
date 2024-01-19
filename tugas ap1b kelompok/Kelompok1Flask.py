from flask import Flask, render_template, request

app = Flask(__name__)

# Ubah list anggota pada kode Flask
anggota = []
database_kelompok = []


@app.route('/index')
def index():
    # Sertakan data kelompok pada laman utama
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

    # Cetak data anggota dan kelompok
    print("Data anggota:", anggota)
    print("Database kelompok:", database_kelompok)

    return render_template('index.html', new_group=new_group)


@app.route('/list', methods=['GET'])
def list_group():
    global database_kelompok
    global anggota
    # Sertakan data kelompok pada laman daftar grup
    return render_template('listgrp.html', database_kelompok=database_kelompok)

@app.route('/calculate_average', methods=['POST'])
def calculate_average():
    nilai_anggota = {}

    # Iterasi kelompok dan data anggota
    for group in database_kelompok:
        for member_data_item in group['members_data']:
            scores_key = f"{group['name']}_{member_data_item['name']}"
            scores_str = request.form.get(scores_key, "")
            scores = [int(x) for x in scores_str.split() if x.isdigit()]
            member_data_item['nilai'] = scores
            nilai_anggota.setdefault(group['name'], {})[member_data_item['name']] = member_data_item['nilai']

    # Iterasi nilai_anggota untuk menghitung rata-rata dan menyimpannya di nilai_anggota
    for group_name, members_data in nilai_anggota.items():
        group_scores = [sum(scores) / len(scores) if scores else None for scores in members_data.values()]
        nilai_anggota[group_name]['rata_rata'] = sum(group_scores) / len(group_scores) if group_scores else None

    rata_rata_kelompok = {group_name: nilai_anggota[group_name]['rata_rata'] for group_name in nilai_anggota}

    print("request.form:", request.form)
    print("nilai_anggota:", nilai_anggota)
    print("rata_rata_kelompok:", rata_rata_kelompok)

    return render_template("inputgrade.html", anggota=anggota, database_kelompok=database_kelompok, members_data=True, nilai_anggota=nilai_anggota, rata_rata_kelompok=rata_rata_kelompok)

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/inputgrade', methods=['POST'])
def reset_to_index():
    return render_template('inputgrade.html')


@app.route('/list', methods=['POST'])
def reset_to_group():
    global database_kelompok
    # Reset database_kelompok ke list kosong
    database_kelompok = []
    return render_template('listgrp.html', anggota=anggota, database_kelompok=database_kelompok)


if __name__ == '__main__':
    app.run(debug=True)
