from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def binomial_probability(n, x, p):
    if x > n or p < 0 or p > 1:
        return 0
    coeff = math.comb(n, x)
    return coeff * (p ** x) * ((1 - p) ** (n - x))

def cumulative_probability(n, x, p, direction='lte'):
    total = 0
    if direction == 'lte':
        for i in range(x + 1):
            total += binomial_probability(n, i, p)
    elif direction == 'lt':
        for i in range(x):
            total += binomial_probability(n, i, p)
    elif direction == 'gte':
        for i in range(x, n + 1):
            total += binomial_probability(n, i, p)
    elif direction == 'gt':
        for i in range(x + 1, n + 1):
            total += binomial_probability(n, i, p)
    return total

def poisson_probability(lam, k):
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)

def cumulative_poisson(lam, k, direction='lte'):
    total = 0
    if direction == 'lte':
        for i in range(k + 1):
            total += poisson_probability(lam, i)
    elif direction == 'lt':
        for i in range(k):
            total += poisson_probability(lam, i)
    elif direction == 'gte':
        for i in range(k, int(lam * 10)):  # Approximate upper limit
            total += poisson_probability(lam, i)
    elif direction == 'gt':
        for i in range(k + 1, int(lam * 10)):
            total += poisson_probability(lam, i)
    return total

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tutorial/')
def tutorial():
    return render_template('tutorial.html')

@app.route('/faqs/')
def faqs():
    return render_template('faqs.html')

@app.route('/members/')
def members():
    return render_template('members.html')

@app.route('/other_calculators/')
def other_calculators():
    return render_template('other_calculators.html')

@app.route('/poisson/')
def poisson():
    return render_template('poisson.html')

@app.route('/calculate/', methods=['POST'])
def calculate():
    data = request.get_json()
    probability = float(data['probability'])
    trials = int(data['trials'])
    successes = int(data['successes'])

    if probability < 0 or probability > 1 or successes > trials:
        return jsonify({'error': 'Invalid input: Probability must be between 0 and 1, and successes must not exceed trials.'})

    binomial_prob = binomial_probability(trials, successes, probability)
    cumulative_lt = cumulative_probability(trials, successes, probability, 'lt')
    cumulative_lte = cumulative_probability(trials, successes, probability, 'lte')
    cumulative_gt = cumulative_probability(trials, successes, probability, 'gt')
    cumulative_gte = cumulative_probability(trials, successes, probability, 'gte')

    return jsonify({
        'binomial_probability': f'{binomial_prob:.4f}',
        'cumulative_probability_lt': f'{cumulative_lt:.4f}',
        'cumulative_probability_lte': f'{cumulative_lte:.4f}',
        'cumulative_probability_gt': f'{cumulative_gt:.4f}',
        'cumulative_probability_gte': f'{cumulative_gte:.4f}'
    })

@app.route('/calculate_poisson/', methods=['POST'])
def calculate_poisson():
    data = request.get_json()
    lam = float(data['lambda'])
    k = int(data['k'])

    if lam < 0 or k < 0:
        return jsonify({'error': 'Invalid input: Lambda and k must be non-negative.'})

    poisson_prob = poisson_probability(lam, k)
    cumulative_lt = cumulative_poisson(lam, k, 'lt')
    cumulative_lte = cumulative_poisson(lam, k, 'lte')
    cumulative_gt = cumulative_poisson(lam, k, 'gt')
    cumulative_gte = cumulative_poisson(lam, k, 'gte')

    return jsonify({
        'poisson_probability': f'{poisson_prob:.4f}',
        'cumulative_probability_lt': f'{cumulative_lt:.4f}',
        'cumulative_probability_lte': f'{cumulative_lte:.4f}',
        'cumulative_probability_gt': f'{cumulative_gt:.4f}',
        'cumulative_probability_gte': f'{cumulative_gte:.4f}'
    })

if __name__ == '__main__':
    app.run(debug=True)