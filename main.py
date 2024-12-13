import csv
from collections import defaultdict


def read_csv(filename):
    answers = defaultdict(int)
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # ヘッダーをスキップ
            for row in reader:
                if len(row) == 2:
                    answer, count = row
                    answers[answer] = int(count)
    except FileNotFoundError:
        pass  # ファイルが存在しない場合は無視
    return answers


def ask_questions(questions, existing_answers):
    answers = defaultdict(int)
    for i, question in enumerate(questions):
        if i == 1 and existing_answers:
            # 既存の回答の中で最もカウントが多いデータを取得
            recommended_answer = max(existing_answers, key=existing_answers.get)
            recommendation = input(f"My recommendation is '{recommended_answer}'. Are you interested? [Yes/No] ")
            if recommendation.lower() == 'yes':
                print(f"You chose: {recommended_answer}")
                answers[recommended_answer] += 1
                continue  # 次の質問に進む
            elif recommendation.lower() == 'no':
                pass  # 通常通り質問を続ける
            else:
                print("Invalid input. Please answer with 'Yes' or 'No'.")
                continue  # 無効な入力の場合、再度質問を行う

        answer = input(question + ' ')
        print(f'Your answer is: {answer}')
        if question == 'What are your favorite things?':
            answers[answer] += 1
    return answers


def save_to_csv(filename, answers):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Answer', 'Count'])
        for answer, count in answers.items():
            writer.writerow([answer, count])


if __name__ == '__main__':
    filename = 'answers.csv'
    questions = [
        'What is your name?',
        'What are your favorite things?'
    ]

    # 既存の回答を読み込む
    existing_answers = read_csv(filename)

    # 新しい回答を収集する
    new_answers = ask_questions(questions, existing_answers)

    # 新しい回答を既存の回答に統合する
    for answer, count in new_answers.items():
        existing_answers[answer] += count

    # 統合された回答をCSVに保存する
    save_to_csv(filename, existing_answers)

    print('Thank you for your response!')
