document.getElementById('binomial-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const probability = document.getElementById('p-success').value;
    const trials = document.getElementById('n-trials').value;
    const successes = document.getElementById('x-successes').value;

    fetch('/calculate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ probability, trials, successes })
    })
    .then(response => response.json())
    .then(data => {
        const errorMessage = document.getElementById('error-message');
        if (data.error) {
            errorMessage.innerText = data.error;
        } else {
            errorMessage.innerText = '';
            document.getElementById('binomial-probability').value = data.binomial_probability;
            document.getElementById('cumulative-probability-1').value = data.cumulative_probability_lt;
            document.getElementById('cumulative-probability-2').value = data.cumulative_probability_lte;
            document.getElementById('cumulative-probability-3').value = data.cumulative_probability_gt;
            document.getElementById('cumulative-probability-4').value = data.cumulative_probability_gte;
        }
    })
    .catch(error => console.error('Error:', error));
});