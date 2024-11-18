from django.shortcuts import render
from scipy.stats import binom
from django.http import JsonResponse
import json

# Create your views here.


def calculate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            probability = float(data['probability'])
            trials = int(data['trials'])
            successes = int(data['successes'])

            # Server-side validation
            if probability < 0 or probability > 1:
                return JsonResponse({'error': 'Probability must be between 0 and 1.'})
            if successes > trials:
                return JsonResponse({'error': 'Number of successes cannot exceed number of trials.'})
            if trials < 0 or successes < 0:
                return JsonResponse({'error': 'Number of trials and successes must be non-negative.'})

            # Binomial probability
            binomial_probability = binom.pmf(successes, trials, probability)

            # Cumulative probabilities
            cumulative_probability_lt = binom.cdf(
                successes - 1, trials, probability)
            cumulative_probability_lte = binom.cdf(
                successes, trials, probability)
            cumulative_probability_gt = 1 - \
                binom.cdf(successes, trials, probability)
            cumulative_probability_gte = 1 - \
                binom.cdf(successes - 1, trials, probability)

            # Return results as JSON
            return JsonResponse({
                'binomial_probability': binomial_probability,
                'cumulative_probability_lt': cumulative_probability_lt,
                'cumulative_probability_lte': cumulative_probability_lte,
                'cumulative_probability_gt': cumulative_probability_gt,
                'cumulative_probability_gte': cumulative_probability_gte,
            })

        except (ValueError, KeyError):
            return JsonResponse({'error': 'Invalid input. Please ensure all fields are filled correctly.'})


def starting_page(request):
    return render(request, 'calculator/index.html')


def tutorial(request):
    return render(request, 'calculator/tutorial.html')


def faqs(request):
    return render(request, 'calculator/faqs.html')


def members(request):
    return render(request, 'calculator/members.html')
