from flask import Flask, render_template, request # type: ignore

app = Flask(__name__)

# Data dari soal
items = [
    {'weight': 3, 'value': 6, 'max_qty': 3},   # Item 1
    {'weight': 4, 'value': 8, 'max_qty': 2},   # Item 2
    {'weight': 5, 'value': 10, 'max_qty': 2},  # Item 3
    {'weight': 6, 'value': 12, 'max_qty': 1},  # Item 4
    {'weight': 7, 'value': 14, 'max_qty': 2},  # Item 5
    {'weight': 2, 'value': 4, 'max_qty': 4},   # Item 6
    {'weight': 1, 'value': 3, 'max_qty': 5},   # Item 7
    {'weight': 9, 'value': 16, 'max_qty': 1},  # Item 8
]

max_capacity = 20  # Kapasitas maksimal ransel

# Fungsi rekursif untuk backtracking (menyimpan semua solusi valid)
def knapsack_backtracking(i, current_weight, current_value, selected_items, valid_solutions):
    if i == len(items):  # Basis rekursif, simpan kombinasi valid
        if current_weight <= max_capacity:
            valid_solutions.append((selected_items.copy(), current_value))
        return
    
    item = items[i]
    
    for qty in range(item['max_qty'] + 1):  # Pilih dari 0 hingga jumlah maksimal
        new_weight = current_weight + item['weight'] * qty
        new_value = current_value + item['value'] * qty
        
        if new_weight <= max_capacity:  # Cek apakah ransel masih cukup kapasitasnya
            selected_items[i] = qty
            knapsack_backtracking(i + 1, new_weight, new_value, selected_items, valid_solutions)
        else:
            break
    
    selected_items[i] = 0  # Backtrack dan reset

# Fungsi utama untuk memulai backtracking
def find_all_valid_combinations():
    valid_solutions = []  # Menyimpan semua solusi valid
    selected_items = [0] * len(items)  # Penyimpanan sementara jumlah item yang dipilih

    knapsack_backtracking(0, 0, 0, selected_items, valid_solutions)

    return valid_solutions

@app.route('/', methods=['GET', 'POST'])
def index():
    valid_solutions = []
    max_solution = None

    if request.method == 'POST':
        valid_solutions = find_all_valid_combinations()
        max_solution = max(valid_solutions, key=lambda x: x[1])

    return render_template('index.html', valid_solutions=valid_solutions, max_solution=max_solution)

if __name__ == '__main__':
    app.run(debug=True)
