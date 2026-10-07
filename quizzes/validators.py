"""
Validation and scoring engine for all 20 Python Quiz question types.
"""

from practice.sandbox import execute_python_code

def validate_question_answer(question, raw_user_value):
    """
    Validates user submitted answer for any question type.
    Returns dict:
    {
        'is_correct': bool,
        'is_skipped': bool,
        'marks_earned': float,
        'user_display': str,
        'correct_display': str,
        'selected_option': QuizOption or None,
        'text_answer': str,
        'user_answer_json': dict or list,
    }
    """
    q_type = question.question_type
    marks = question.marks
    data = question.question_data or {}

    # Check for empty / skipped answer
    if raw_user_value is None or raw_user_value == "" or raw_user_value == [] or raw_user_value == {}:
        # Format correct display for skipped questions
        correct_display = get_correct_display_text(question)
        return {
            'is_correct': False,
            'is_skipped': True,
            'marks_earned': 0.0,
            'user_display': '(Skipped)',
            'correct_display': correct_display,
            'selected_option': None,
            'text_answer': '',
            'user_answer_json': {},
        }

    # 1. MCQ, Code Output, Find Error, Scenario Based, Identify Output, Diagram Question, Code Comparison
    if q_type in ['mcq', 'code_output', 'find_error', 'scenario_based', 'identify_output', 'diagram_question', 'code_comparison', 'true_false']:
        selected_opt = None
        is_corr = False
        user_disp = str(raw_user_value)

        try:
            opt_id = int(raw_user_value)
            selected_opt = question.options.filter(id=opt_id).first()
            if selected_opt:
                user_disp = selected_opt.option_text
                is_corr = selected_opt.is_correct
        except (ValueError, TypeError):
            # Might be literal text value for true/false
            matched_opt = question.options.filter(option_text__iexact=str(raw_user_value).strip()).first()
            if matched_opt:
                selected_opt = matched_opt
                user_disp = matched_opt.option_text
                is_corr = matched_opt.is_correct

        correct_opt = question.options.filter(is_correct=True).first()
        correct_disp = correct_opt.option_text if correct_opt else ''

        return {
            'is_correct': is_corr,
            'is_skipped': False,
            'marks_earned': float(marks) if is_corr else 0.0,
            'user_display': user_disp,
            'correct_display': correct_disp,
            'selected_option': selected_opt,
            'text_answer': user_disp,
            'user_answer_json': {'option_id': selected_opt.id if selected_opt else None},
        }

    # 2. Multiple Select (Checkboxes)
    elif q_type == 'multiple_select':
        user_ids = []
        if isinstance(raw_user_value, list):
            user_ids = [int(x) for x in raw_user_value if str(x).isdigit()]
        elif isinstance(raw_user_value, str):
            user_ids = [int(x.strip()) for x in raw_user_value.split(',') if x.strip().isdigit()]

        correct_options = list(question.options.filter(is_correct=True))
        correct_ids = set(o.id for o in correct_options)
        user_id_set = set(user_ids)

        is_corr = (user_id_set == correct_ids)
        user_opt_texts = list(question.options.filter(id__in=user_ids).values_list('option_text', flat=True))
        correct_opt_texts = [o.option_text for o in correct_options]

        return {
            'is_correct': is_corr,
            'is_skipped': False,
            'marks_earned': float(marks) if is_corr else 0.0,
            'user_display': ", ".join(user_opt_texts) if user_opt_texts else '(None selected)',
            'correct_display': ", ".join(correct_opt_texts),
            'selected_option': None,
            'text_answer': ", ".join(user_opt_texts),
            'user_answer_json': {'selected_ids': user_ids},
        }

    # 3. Fill in the Blank, Code Completion, Predict Variable, Short Answer
    elif q_type in ['fill_blank', 'code_completion', 'predict_variable', 'short_answer']:
        user_str = str(raw_user_value).strip()
        expected = question.fill_blank_answer.strip()
        accepted = [a.strip().lower() for a in (data.get('accepted_answers') or [expected])]
        if expected.lower() not in accepted:
            accepted.append(expected.lower())

        is_corr = user_str.lower() in accepted

        return {
            'is_correct': is_corr,
            'is_skipped': False,
            'marks_earned': float(marks) if is_corr else 0.0,
            'user_display': user_str,
            'correct_display': expected,
            'selected_option': None,
            'text_answer': user_str,
            'user_answer_json': {'text': user_str},
        }

    # 4. Drag and Drop Blank
    elif q_type == 'drag_drop_blank':
        user_token = str(raw_user_value).strip()
        correct_token = data.get('correct_token', question.fill_blank_answer).strip()
        is_corr = (user_token == correct_token)

        return {
            'is_correct': is_corr,
            'is_skipped': False,
            'marks_earned': float(marks) if is_corr else 0.0,
            'user_display': user_token,
            'correct_display': correct_token,
            'selected_option': None,
            'text_answer': user_token,
            'user_answer_json': {'token': user_token},
        }

    # 5. Arrange the Code, Code Ordering, Order / Sequence Steps
    elif q_type in ['arrange_code', 'code_ordering', 'order_sequence']:
        user_order = raw_user_value if isinstance(raw_user_value, list) else []
        correct_order = data.get('correct_order') or data.get('correct_sequence') or []

        # Standardize items to strings
        user_items = [str(x).strip() for x in user_order]
        target_items = [str(x).strip() for x in correct_order]

        is_corr = (user_items == target_items)

        return {
            'is_correct': is_corr,
            'is_skipped': False,
            'marks_earned': float(marks) if is_corr else 0.0,
            'user_display': "\n".join(user_items),
            'correct_display': "\n".join(target_items),
            'selected_option': None,
            'text_answer': "; ".join(user_items),
            'user_answer_json': {'order': user_items},
        }

    # 6. Match the Following
    elif q_type == 'match_following':
        # Expecting dict like: { "list": "Mutable sequence", "tuple": "Immutable sequence", ... }
        user_pairs = raw_user_value if isinstance(raw_user_value, dict) else {}
        correct_pairs = data.get('correct_pairs', {})

        is_corr = True
        if not user_pairs or len(user_pairs) != len(correct_pairs):
            is_corr = False
        else:
            for k, v in correct_pairs.items():
                if user_pairs.get(k) != v:
                    is_corr = False
                    break

        user_disp = ", ".join([f"{k} → {v}" for k, v in user_pairs.items()])
        correct_disp = ", ".join([f"{k} → {v}" for k, v in correct_pairs.items()])

        return {
            'is_correct': is_corr,
            'is_skipped': False,
            'marks_earned': float(marks) if is_corr else 0.0,
            'user_display': user_disp,
            'correct_display': correct_disp,
            'selected_option': None,
            'text_answer': user_disp,
            'user_answer_json': user_pairs,
        }

    # 7. Debug the Code & Mini Coding Challenge
    elif q_type in ['debug_code', 'mini_challenge']:
        code_sub = str(raw_user_value).strip()
        expected_output = data.get('expected_output', '').strip()
        test_cases = data.get('test_cases', [])

        is_corr = False
        res = execute_python_code(code_sub)

        if test_cases:
            all_passed = True
            for tc in test_cases:
                tc_res = execute_python_code(code_sub, stdin_input=tc.get('input', ''))
                actual = (tc_res.get('stdout') or '').strip()
                exp = str(tc.get('output', '')).strip()
                if actual != exp or tc_res.get('status') != 'success':
                    all_passed = False
                    break
            is_corr = all_passed
        elif expected_output:
            actual = (res.get('stdout') or '').strip()
            is_corr = (actual == expected_output and res.get('status') == 'success')
        else:
            is_corr = (res.get('status') == 'success')

        return {
            'is_correct': is_corr,
            'is_skipped': False,
            'marks_earned': float(marks) if is_corr else 0.0,
            'user_display': code_sub,
            'correct_display': data.get('solution_code') or expected_output or 'Correct runnable code',
            'selected_option': None,
            'text_answer': code_sub,
            'user_answer_json': {
                'code': code_sub,
                'stdout': res.get('stdout', ''),
                'stderr': res.get('stderr', ''),
                'status': res.get('status', '')
            },
        }

    # Fallback default
    return {
        'is_correct': False,
        'is_skipped': False,
        'marks_earned': 0.0,
        'user_display': str(raw_user_value),
        'correct_display': '',
        'selected_option': None,
        'text_answer': str(raw_user_value),
        'user_answer_json': {},
    }


def get_correct_display_text(question):
    """Helper to generate human-readable correct answer text."""
    q_type = question.question_type
    data = question.question_data or {}

    if q_type in ['mcq', 'code_output', 'find_error', 'scenario_based', 'identify_output', 'diagram_question', 'code_comparison', 'true_false']:
        corr = question.options.filter(is_correct=True).first()
        return corr.option_text if corr else ''
    elif q_type == 'multiple_select':
        return ", ".join(question.options.filter(is_correct=True).values_list('option_text', flat=True))
    elif q_type in ['fill_blank', 'code_completion', 'predict_variable', 'short_answer']:
        return question.fill_blank_answer
    elif q_type == 'drag_drop_blank':
        return data.get('correct_token', question.fill_blank_answer)
    elif q_type in ['arrange_code', 'code_ordering', 'order_sequence']:
        order = data.get('correct_order') or data.get('correct_sequence') or []
        return "\n".join([str(x) for x in order])
    elif q_type == 'match_following':
        pairs = data.get('correct_pairs', {})
        return ", ".join([f"{k} → {v}" for k, v in pairs.items()])
    elif q_type in ['debug_code', 'mini_challenge']:
        return data.get('solution_code') or data.get('expected_output') or 'Working solution code'
    return ''
