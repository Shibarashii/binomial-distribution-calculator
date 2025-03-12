document.getElementById('poisson-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const lambda = document.getElementById('lambda').value;
    const k = document.getElementById('k-events').value;

    fetch('/calculate_poisson/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lambda, k })
    })
    .then(response => response.json())
    .then(data => {
        const errorMessage = document.getElementById('error-message');
        if (data.error) {
            errorMessage.innerText = data.error;
        } else {
            errorMessage.innerText = '';
            document.getElementById('poisson-probability').value = data.poisson_probability;
            document.getElementById('cumulative-probability-1').value = data.cumulative_probability_lt;
            document.getElementById('cumulative-probability-2').value = data.cumulative_probability_lte;
            document.getElementById('cumulative-probability-3').value = data.cumulative_probability_gt;
            document.getElementById('cumulative-probability-4').value = data.cumulative_probability_gte;
        }
    })
    .catch(error => console.error('Error:', error));
});