from hh_api import HeadHunterAPI
from json_saver import JSONSaver
from logger import setup_logging
from utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from vacancy import Vacancy

logger = setup_logging()


def user_interaction():
    """
    Function for user interaction.
    """
    # Create API instance
    hh_api = HeadHunterAPI()

    # Create file manager instance
    json_saver = JSONSaver("data/vacancies.json")

    # Get search query from user
    search_query = input("Введите поисковый запрос: ")

    # Get vacancies from API
    print(f"Ищем вакансии по запросу '{search_query}'...")
    hh_vacancies = hh_api.get_vacancies(search_query)

    # Convert to Vacancy objects
    vacancies_list = []
    for item in hh_vacancies:
        try:
            vacancy = Vacancy(
                name=item["name"],
                url=item["url"],
                salary=item["salary"],
                description=item["description"],
            )
            vacancies_list.append(vacancy)

            # Save to file
            json_saver.add_vacancy(item)

        except ValueError as e:
            print(f"Ошибка при создании вакансии: {e}")
            continue

    if not vacancies_list:
        print("Не найдено вакансий по данному запросу.")
        return

    # Get number of top vacancies to display
    while True:
        try:
            top_n = int(input("Введите количество вакансий для вывода в топ N: "))
            if top_n > 0:
                break
            else:
                print("Введите положительное число.")
        except ValueError:
            print("Введите корректное число.")

    # Get filter words
    filter_words_input = input("Введите ключевые слова для фильтрации вакансий (через пробел): ")
    filter_words = filter_words_input.split() if filter_words_input.strip() else []

    # Get salary range
    salary_range = input("Введите диапазон зарплат (например, 100000 - 150000): ")

    # Apply filters and sorting
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Display results
    print(f"\nНайдено {len(vacancies_list)} вакансий")
    print(f"После фильтрации найдено {len(filtered_vacancies)} вакансий")
    print(f"После фильтрации по зарплате найдено {len(ranged_vacancies)} вакансий")
    print(f"Топ {top_n} вакансий по зарплате:\n")

    print_vacancies(top_vacancies)


if __name__ == "__main__":
    logger = setup_logging()
    logger.info("Application starts....")

    user_interaction()

    logger.info("Application finished")
