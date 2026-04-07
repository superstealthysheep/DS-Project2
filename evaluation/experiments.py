import score_all_questions as saq

def main():
    print("Step 1: ingesting full corpus")
    total_vectors: int = saq.ingest_full_corpus(saq.CORPUS_FILE)

    print("\nStep 2: loading all scored questions")
    questions: list[dict] = saq.load_questions(saq.QUESTIONS_FILE)

    print("Step 3: evaluating all questions")
    results: list[dict] = saq.evaluate_all_questions(questions, total_vectors)

    saq.print_summary(results, total_vectors)

if __name__ == "__main__":
    main()