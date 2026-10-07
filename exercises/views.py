from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Exercise, ExerciseCategory, ExerciseTestCase, ExerciseSubmission
from practice.sandbox import execute_python_code

def exercise_list_view(request):
    categories = ExerciseCategory.objects.all()
    exercises = Exercise.objects.select_related('category').prefetch_related('test_cases').all()

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        exercises = exercises.filter(category__slug=category_slug)

    # Filter by difficulty
    difficulty = request.GET.get('difficulty')
    if difficulty in ['easy', 'medium', 'hard']:
        exercises = exercises.filter(difficulty=difficulty)

    # Search filter
    q = request.GET.get('q')
    if q:
        exercises = exercises.filter(title__icontains=q)

    # Get solved exercise IDs for authenticated user
    solved_ids = set()
    if request.user.is_authenticated:
        solved_ids = set(
            ExerciseSubmission.objects.filter(user=request.user, passed=True)
            .values_list('exercise_id', flat=True)
        )

    context = {
        'exercises': exercises,
        'categories': categories,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'search_query': q or '',
        'solved_ids': solved_ids,
        'total_count': Exercise.objects.count(),
        'solved_count': len(solved_ids),
    }
    return render(request, 'exercises/exercise_list.html', context)

def exercise_detail_view(request, slug):
    exercise = get_object_or_404(Exercise, slug=slug)
    sample_tests = exercise.test_cases.filter(is_sample=True)

    is_solved = False
    last_submission = None
    if request.user.is_authenticated:
        last_submission = ExerciseSubmission.objects.filter(
            user=request.user, exercise=exercise
        ).order_by('-created_at').first()
        is_solved = ExerciseSubmission.objects.filter(
            user=request.user, exercise=exercise, passed=True
        ).exists()
        request.user.profile.update_streak()

    initial_code = last_submission.submitted_code if last_submission else exercise.starter_code

    context = {
        'exercise': exercise,
        'sample_tests': sample_tests,
        'is_solved': is_solved,
        'initial_code': initial_code,
    }
    return render(request, 'exercises/exercise_detail.html', context)

@api_view(['POST'])
@permission_classes([AllowAny])
def run_sample_tests_api(request, slug):
    """
    Runs user code against visible sample test cases without recording permanent submission.
    """
    exercise = get_object_or_404(Exercise, slug=slug)
    code = request.data.get('code', '')

    if not code.strip():
        return Response({'status': 'error', 'message': 'Code cannot be empty.'})

    sample_tests = exercise.test_cases.filter(is_sample=True)
    if not sample_tests.exists():
        # Fallback to single run
        result = execute_python_code(code)
        return Response({
            'status': 'success',
            'results': [{
                'test_num': 1,
                'input': '',
                'expected': '',
                'actual': result.get('stdout', ''),
                'stderr': result.get('stderr', ''),
                'passed': result.get('status') == 'success'
            }],
            'all_passed': result.get('status') == 'success'
        })

    results = []
    all_passed = True

    for idx, test in enumerate(sample_tests, 1):
        res = execute_python_code(code, stdin_input=test.input_data)
        actual = (res.get('stdout') or '').strip()
        expected = (test.expected_output or '').strip()
        
        passed = (actual == expected) and (res.get('status') == 'success')
        if not passed:
            all_passed = False

        results.append({
            'test_num': idx,
            'input': test.input_data,
            'expected': expected,
            'actual': actual,
            'stderr': res.get('stderr', ''),
            'passed': passed,
            'is_sample': True
        })

    return Response({
        'status': 'success',
        'results': results,
        'all_passed': all_passed
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_exercise_api(request, slug):
    """
    Runs code against all test cases (sample + hidden) and records submission for user.
    """
    exercise = get_object_or_404(Exercise, slug=slug)
    code = request.data.get('code', '')

    if not code.strip():
        return Response({'status': 'error', 'message': 'Code cannot be empty.'})

    all_test_cases = exercise.test_cases.all()
    results = []
    passed_count = 0
    total_time = 0.0

    if not all_test_cases.exists():
        # Fallback if no test cases defined
        res = execute_python_code(code)
        passed = res.get('status') == 'success'
        results.append({
            'test_num': 1,
            'input': '',
            'expected': '',
            'actual': res.get('stdout', ''),
            'stderr': res.get('stderr', ''),
            'passed': passed,
            'is_sample': True
        })
        passed_count = 1 if passed else 0
        total_count = 1
        total_time = res.get('execution_time', 0.0)
    else:
        total_count = all_test_cases.count()
        for idx, test in enumerate(all_test_cases, 1):
            res = execute_python_code(code, stdin_input=test.input_data)
            total_time += res.get('execution_time', 0.0)
            actual = (res.get('stdout') or '').strip()
            expected = (test.expected_output or '').strip()

            case_passed = (actual == expected) and (res.get('status') == 'success')
            if case_passed:
                passed_count += 1

            results.append({
                'test_num': idx,
                'input': test.input_data if test.is_sample else '[Hidden Test Case]',
                'expected': expected if test.is_sample else '[Hidden]',
                'actual': actual if test.is_sample else ('Output match' if case_passed else 'Output mismatch or error'),
                'stderr': res.get('stderr', '') if test.is_sample else ('Error occurred' if res.get('stderr') else ''),
                'passed': case_passed,
                'is_sample': test.is_sample
            })

    all_passed = (passed_count == total_count)
    new_badges = []
    points_awarded = 0

    if request.user.is_authenticated:
        already_solved = ExerciseSubmission.objects.filter(
            user=request.user, exercise=exercise, passed=True
        ).exists()

        submission = ExerciseSubmission.objects.create(
            user=request.user,
            exercise=exercise,
            submitted_code=code,
            passed=all_passed,
            score=exercise.points if all_passed else 0,
            test_cases_passed=passed_count,
            total_test_cases=total_count,
            execution_time=round(total_time, 3),
        )

        request.user.profile.update_streak()

        if all_passed and not already_solved:
            points_awarded = exercise.points
            request.user.profile.add_xp(points_awarded)

            from progress.gamification import check_and_award_badges
            new_badges = check_and_award_badges(request.user)

    return Response({
        'status': 'success',
        'all_passed': all_passed,
        'passed_count': passed_count,
        'total_count': total_count,
        'execution_time': round(total_time, 3),
        'results': results,
        'points_awarded': points_awarded,
        'explanation': exercise.explanation if all_passed else '',
        'solution_code': exercise.solution_code if all_passed else '',
        'new_badges': [b.name for b in new_badges],
        'is_authenticated': request.user.is_authenticated
    })
