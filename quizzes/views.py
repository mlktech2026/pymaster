import json
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Max, Count, Sum
from django.utils import timezone
from django.utils.text import slugify
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Quiz, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer
from .validators import validate_question_answer

def quiz_list_view(request):
    """
    Renders quiz catalog and custom generator launchpad.
    """
    # Fetch standard published quizzes (excluding dynamic one-off quizzes)
    quizzes = Quiz.objects.filter(is_published=True, is_dynamic=False, questions__isnull=False).distinct().prefetch_related('questions')

    user_attempts = {}
    if request.user.is_authenticated:
        attempts = QuizAttempt.objects.filter(user=request.user).order_by('quiz_id', '-percentage')
        for att in attempts:
            if att.quiz_id not in user_attempts:
                user_attempts[att.quiz_id] = att

    quizzes_data = []
    for q in quizzes:
        quizzes_data.append({
            'quiz': q,
            'question_count': q.questions.filter(is_active=True).count(),
            'total_marks': q.total_marks,
            'user_attempt': user_attempts.get(q.id)
        })

    categories = list(QuizQuestion.objects.values_list('category', flat=True).distinct())

    return render(request, 'quizzes/quiz_list.html', {
        'quizzes_data': quizzes_data,
        'categories': sorted(categories),
        'total_questions_in_db': QuizQuestion.objects.filter(is_active=True).count(),
        'question_types_count': QuizQuestion.objects.values('question_type').distinct().count(),
    })


def quiz_generator_view(request):
    """
    Custom Random Quiz Generator.
    Users select category, difficulty, number of questions, and timer.
    """
    all_categories = sorted(list(QuizQuestion.objects.values_list('category', flat=True).distinct()))
    all_types = QuizQuestion.TYPE_CHOICES

    if request.method == 'POST':
        category = request.POST.get('category', 'all')
        difficulty = request.POST.get('difficulty', 'mixed')
        question_count = int(request.POST.get('question_count', 10))
        time_limit = int(request.POST.get('time_limit', 10))

        # Query questions
        query = QuizQuestion.objects.filter(is_active=True)
        if category and category != 'all':
            query = query.filter(category=category)
        if difficulty and difficulty != 'mixed':
            query = query.filter(difficulty=difficulty)

        matching_questions = list(query.order_by('?'))
        if not matching_questions:
            # Fallback if no specific filter match
            matching_questions = list(QuizQuestion.objects.filter(is_active=True).order_by('?'))

        selected_questions = matching_questions[:question_count]

        # Create temporary or dedicated dynamic quiz
        slug = f"custom-quiz-{timezone.now().strftime('%Y%m%d%H%M%S')}-{random.randint(100, 999)}"
        title_cat = "All Python Topics" if category == 'all' else category
        title = f"{title_cat} Challenge"

        quiz = Quiz.objects.create(
            title=title,
            slug=slug,
            category=category,
            difficulty=difficulty,
            description=f"Generated Quiz: {len(selected_questions)} random questions covering {title_cat} ({difficulty.capitalize()} level).",
            time_limit_mins=time_limit,
            pass_percentage=70,
            is_dynamic=True,
            is_published=True,
            total_questions_count=len(selected_questions)
        )

        # Clone and associate questions with sequential orders
        for idx, orig_q in enumerate(selected_questions, 1):
            q_clone = QuizQuestion.objects.create(
                quiz=quiz,
                question_type=orig_q.question_type,
                category=orig_q.category,
                difficulty=orig_q.difficulty,
                question_text=orig_q.question_text,
                code_snippet=orig_q.code_snippet,
                fill_blank_answer=orig_q.fill_blank_answer,
                question_data=orig_q.question_data,
                explanation=orig_q.explanation,
                marks=orig_q.marks,
                order=idx,
                is_active=True
            )
            # Clone options if any
            for opt in orig_q.options.all():
                QuizOption.objects.create(
                    question=q_clone,
                    option_text=opt.option_text,
                    is_correct=opt.is_correct,
                    order=opt.order
                )

        return redirect('quiz_take', slug=quiz.slug)

    return render(request, 'quizzes/quiz_generator.html', {
        'categories': all_categories,
        'types': all_types,
    })


def quiz_take_view(request, slug):
    """
    Renders the modern, interactive step-by-step quiz taker interface.
    """
    quiz = get_object_or_404(Quiz, slug=slug, is_published=True)
    questions = quiz.questions.filter(is_active=True).prefetch_related('options').order_by('order', 'id')

    if request.user.is_authenticated:
        request.user.profile.update_streak()

    return render(request, 'quizzes/quiz_take.html', {
        'quiz': quiz,
        'questions': questions,
        'total_questions': questions.count(),
        'total_marks': quiz.total_marks,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def quiz_submit_api(request, slug):
    """
    Validates and grades submitted answers across all 20 question types.
    """
    quiz = get_object_or_404(Quiz, slug=slug)
    user_answers = request.data.get('answers', {})
    time_taken = int(request.data.get('time_taken_seconds', 0))

    questions = quiz.questions.filter(is_active=True).prefetch_related('options').order_by('order', 'id')
    
    total_marks = 0.0
    earned_score = 0.0
    correct_count = 0
    wrong_count = 0
    skipped_count = 0
    detailed_answers = []

    for q in questions:
        total_marks += float(q.marks)
        user_val = user_answers.get(str(q.id))

        validation = validate_question_answer(q, user_val)

        if validation['is_skipped']:
            skipped_count += 1
        elif validation['is_correct']:
            correct_count += 1
            earned_score += validation['marks_earned']
        else:
            wrong_count += 1

        detailed_answers.append({
            'question': q,
            'selected_option': validation['selected_option'],
            'text_answer': validation['text_answer'],
            'user_answer_json': validation['user_answer_json'],
            'is_correct': validation['is_correct'],
            'is_skipped': validation['is_skipped'],
            'marks_earned': validation['marks_earned'],
        })

    percentage = round((earned_score / total_marks * 100), 1) if total_marks > 0 else 0.0
    passed = percentage >= quiz.pass_percentage

    attempt_id = None
    new_badges = []

    if request.user.is_authenticated:
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=round(earned_score, 1),
            total_marks=round(total_marks, 1),
            percentage=percentage,
            passed=passed,
            time_taken_seconds=time_taken,
        )
        attempt_id = attempt.id

        answer_objs = [
            QuizAnswer(
                attempt=attempt,
                question=item['question'],
                selected_option=item['selected_option'],
                text_answer=item['text_answer'],
                user_answer_json=item['user_answer_json'],
                is_correct=item['is_correct'],
                is_skipped=item['is_skipped'],
                marks_earned=item['marks_earned'],
            )
            for item in detailed_answers
        ]
        QuizAnswer.objects.bulk_create(answer_objs)

        # Gamification
        xp_gain = 35 if passed else 10
        request.user.profile.add_xp(xp_gain)
        request.user.profile.update_streak()

        from progress.gamification import check_and_award_badges
        new_badges = check_and_award_badges(request.user)

    return Response({
        'status': 'success',
        'attempt_id': attempt_id,
        'score': earned_score,
        'total_marks': total_marks,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'skipped_count': skipped_count,
        'percentage': percentage,
        'passed': passed,
        'time_taken_seconds': time_taken,
        'new_badges': [b.name for b in new_badges],
        'redirect_url': f"/quizzes/{quiz.slug}/result/{attempt_id}/" if attempt_id else None
    })


def quiz_result_view(request, slug, attempt_id):
    """
    Renders modern score report with circular gauge, statistics, and detailed explanation review.
    """
    quiz = get_object_or_404(Quiz, slug=slug)
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, quiz=quiz)
    answers = attempt.answers.select_related('question', 'selected_option').order_by('question__order', 'id')

    # Format answers for template display
    reviewed_answers = []
    for ans in answers:
        q = ans.question
        data = q.question_data or {}
        
        # Calculate human-friendly displays
        user_display = ans.text_answer or '(Skipped)'
        correct_display = ''

        if q.question_type in ['mcq', 'code_output', 'find_error', 'scenario_based', 'identify_output', 'diagram_question', 'code_comparison', 'true_false']:
            corr = q.options.filter(is_correct=True).first()
            correct_display = corr.option_text if corr else ''
        elif q.question_type == 'multiple_select':
            correct_display = ", ".join(q.options.filter(is_correct=True).values_list('option_text', flat=True))
        elif q.question_type in ['fill_blank', 'code_completion', 'predict_variable', 'short_answer']:
            correct_display = q.fill_blank_answer
        elif q.question_type == 'drag_drop_blank':
            correct_display = data.get('correct_token', q.fill_blank_answer)
        elif q.question_type in ['arrange_code', 'code_ordering', 'order_sequence']:
            order = data.get('correct_order') or data.get('correct_sequence') or []
            correct_display = "\n".join([str(x) for x in order])
            if ans.user_answer_json and 'order' in ans.user_answer_json:
                user_display = "\n".join([str(x) for x in ans.user_answer_json['order']])
        elif q.question_type == 'match_following':
            pairs = data.get('correct_pairs', {})
            correct_display = ", ".join([f"{k} → {v}" for k, v in pairs.items()])
        elif q.question_type in ['debug_code', 'mini_challenge']:
            correct_display = data.get('solution_code') or data.get('expected_output') or 'Working solution'

        reviewed_answers.append({
            'answer': ans,
            'question': q,
            'user_display': user_display,
            'correct_display': correct_display,
            'explanation': q.explanation,
        })

    # Time formatting
    mins = attempt.time_taken_seconds // 60
    secs = attempt.time_taken_seconds % 60
    time_taken_str = f"{mins:02d}:{secs:02d}"

    return render(request, 'quizzes/quiz_result.html', {
        'quiz': quiz,
        'attempt': attempt,
        'reviewed_answers': reviewed_answers,
        'time_taken_str': time_taken_str,
    })


@login_required
def quiz_dashboard_view(request):
    """
    Dedicated Quiz Performance Dashboard.
    """
    user = request.user
    attempts = QuizAttempt.objects.filter(user=user).select_related('quiz').order_by('-completed_at')

    total_quizzes = attempts.count()
    avg_score = attempts.aggregate(Avg('percentage'))['percentage__avg']
    avg_score = round(avg_score, 1) if avg_score is not None else 0.0

    best_score = attempts.aggregate(Max('percentage'))['percentage__max']
    best_score = round(best_score, 1) if best_score is not None else 0.0

    user_answers = QuizAnswer.objects.filter(attempt__user=user)
    questions_answered = user_answers.count()
    correct_answers = user_answers.filter(is_correct=True).count()
    accuracy_pct = round((correct_answers / questions_answered * 100), 1) if questions_answered > 0 else 0.0

    # Recent attempts for performance chart
    recent_attempts = list(attempts[:10])
    chart_data = [
        {'title': a.quiz.title[:15], 'score': a.percentage, 'date': a.completed_at.strftime('%b %d')}
        for a in reversed(recent_attempts)
    ]

    return render(request, 'quizzes/quiz_dashboard.html', {
        'total_quizzes': total_quizzes,
        'avg_score': avg_score,
        'best_score': best_score,
        'questions_answered': questions_answered,
        'correct_answers': correct_answers,
        'accuracy_pct': accuracy_pct,
        'quiz_streak': user.profile.current_streak,
        'attempts': attempts[:15],
        'chart_data': chart_data,
    })
