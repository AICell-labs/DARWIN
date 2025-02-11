import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from openai import OpenAI

# Set your OpenAI API key
client = OpenAI(api_key='sk-xxx')

# Gender ratio (Added more gender options)
gender_ratio = [0.351, 0.636, 0.013]
genders = ['female', 'male', 'non-binary']

# Age ratio (Adjusted age group distribution)
age_ratio = [0.05, 0.39, 0.31, 0.11, 0.03, 0.11]
age_groups = ['13-17', '18-24', '25-34', '35-49', '50-64', '65+']

# MBTI ratio
p_mbti = [
    0.12625, 0.11625, 0.02125, 0.03125, 0.05125, 0.07125, 0.04625, 0.04125,
    0.04625, 0.06625, 0.07125, 0.03625, 0.10125, 0.11125, 0.03125, 0.03125
]
mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP",
    "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# Country ratio (Expanded country list and proportions)
country_ratio = [0.35, 0.08, 0.07, 0.05, 0.04, 0.04, 0.04, 0.03, 0.03, 0.27]
countries = ["US", "UK", "Canada", "Australia", "Germany", "France", "Japan", "India", "Brazil", "Other"]

# Profession ratio (Expanded professional categories)
p_professions = [0.08] * 12 + [0.04] * 4
professions = [
    "Technology & Software Development",
    "Healthcare & Medicine",
    "Education & Research",
    "Business & Finance",
    "Creative Arts & Design",
    "Media & Communication",
    "Engineering & Architecture",
    "Science & Research",
    "Sales & Marketing",
    "Legal & Law",
    "Social Services & Community",
    "Entrepreneurship & Startups",
    "Trades & Construction",
    "Food & Hospitality",
    "Transportation & Logistics",
    "Environmental & Sustainability"
]

# Education level ratio (Updated education level distribution)
education_ratio = [0.02, 0.10, 0.35, 0.35, 0.15, 0.03]
education_levels = [
    "Some High School",
    "High School Graduate",
    "Some College",
    "Bachelor's Degree",
    "Master's Degree",
    "Doctorate/Professional Degree"
]

# Language proficiency ratio (Updated language proficiency distribution)
language_ratio = [0.35, 0.40, 0.15, 0.10]
language_counts = [1, 2, 3, "4+"]
available_languages = [
    "English", "Spanish", "Mandarin", "Hindi", "Arabic",
    "French", "Japanese", "German", "Korean", "Italian",
    "Portuguese", "Russian", "Turkish", "Dutch", "Vietnamese"
]

# Social media activity level ratio (Refined activity levels)
activity_ratio = [0.15, 0.25, 0.30, 0.20, 0.10]
activity_levels = [
    "Super Active (Daily poster)",
    "Very Active (Several times/week)",
    "Moderately Active (Weekly)",
    "Occasionally Active (Monthly)",
    "Rarely Active (Few times/year)"
]

# Hobby categories (Expanded hobby categories)
hobby_ratio = [0.09] * 11 + [0.01]
hobby_categories = [
    "Sports & Fitness",
    "Arts & Creativity",
    "Technology & Gaming",
    "Travel & Adventure",
    "Food & Cooking",
    "Reading & Writing",
    "Music & Entertainment",
    "Photography & Visual Arts",
    "Nature & Outdoors",
    "Science & Learning",
    "DIY & Crafts",
    "Collecting & Antiques"
]

# Personality traits (Expanded personality trait dimensions)
personality_dimensions = {
    "Openness": ["Curious", "Creative", "Open-minded", "Traditional", "Conservative"],
    "Conscientiousness": ["Organized", "Responsible", "Careless", "Spontaneous", "Flexible"],
    "Extraversion": ["Outgoing", "Energetic", "Reserved", "Thoughtful", "Independent"],
    "Agreeableness": ["Friendly", "Cooperative", "Direct", "Competitive", "Leadership-oriented"],
    "Neuroticism": ["Stable", "Calm", "Sensitive", "Reactive", "Adaptable"]
}

# Topics of interest (Expanded interest topics)
topic_dict = {
    '1': 'Economics & Finance',
    '2': 'Technology & Innovation',
    '3': 'Culture & Society',
    '4': 'News & Current Events',
    '5': 'Politics & Government',
    '6': 'Business & Entrepreneurship',
    '7': 'Entertainment & Media',
    '8': 'Science & Research',
    '9': 'Health & Wellness',
    '10': 'Environment & Sustainability',
    '11': 'Education & Learning',
    '12': 'Sports & Recreation'
}

def get_random_gender():
    return random.choices(genders, gender_ratio)[0]


def get_random_age():
    group = random.choices(age_groups, age_ratio)[0]
    if group == 'underage':
        return random.randint(10, 17)
    elif group == '18-29':
        return random.randint(18, 29)
    elif group == '30-49':
        return random.randint(30, 49)
    elif group == '50-64':
        return random.randint(50, 64)
    else:
        return random.randint(65, 100)


def get_random_mbti():
    return random.choices(mbti_types, p_mbti)[0]


def get_random_country():
    country = random.choices(countries, country_ratio)[0]
    if country == "Other":
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "Select a real country name randomly:"
            }])
        return response.choices[0].message.content.strip()
    return country


def get_random_profession():
    return random.choices(professions, p_professions)[0]


def get_random_education():
    return random.choices(education_levels, education_ratio)[0]


def get_random_languages():
    count = int(random.choices(language_counts, language_ratio)[0].replace("+", ""))
    languages = ["English"]  # Default language is English
    if count > 1:
        additional = random.sample(available_languages, count - 1)
        languages.extend(additional)
    return languages


def get_random_activity_level():
    return random.choices(activity_levels, activity_ratio)[0]


def get_random_hobbies():
    num_hobbies = random.randint(2, 4)
    return random.sample(hobby_categories, num_hobbies)


def get_personality_traits():
    traits = {}
    for dimension, trait_list in personality_dimensions.items():
        # 为每个维度随机选择一个特征值，并附加一个0.1-1.0的强度分数
        selected_trait = random.choice(trait_list)
        intensity = round(random.uniform(0.1, 1.0), 2)
        traits[dimension] = {
            "trait": selected_trait,
            "intensity": intensity
        }
    return traits


def get_interested_topics(mbti, age, gender, country, profession):
    prompt = f"""Based on the provided personality traits, age, gender and profession, please select 2-4 topics of interest from the given list.
    Input:
        Personality Traits: {mbti}
        Age: {age}
        Gender: {gender}
        Country: {country}
        Profession: {profession}
    Available Topics:
        1. Economics & Finance: Markets, investments, financial planning, economic trends and analysis.
        2. Technology & Innovation: Latest tech trends, digital transformation, emerging technologies, and innovation.
        3. Culture & Society: Arts, lifestyle, social trends, cultural phenomena, and societal issues.
        4. News & Current Events: Breaking news, global affairs, local news, and trending stories.
        5. Politics & Government: Political discourse, policy making, governance, and civic engagement.
        6. Business & Entrepreneurship: Startups, business strategy, management, and entrepreneurial insights.
        7. Entertainment & Media: Movies, TV shows, music, celebrity news, and digital media.
        8. Science & Research: Scientific discoveries, research breakthroughs, and academic developments.
        9. Health & Wellness: Physical health, mental wellbeing, fitness, and healthcare.
        10. Environment & Sustainability: Climate change, conservation, sustainable living, and eco-friendly practices.
        11. Education & Learning: Educational trends, learning resources, skill development, and academic topics.
        12. Sports & Recreation: Sports news, outdoor activities, recreational pursuits, and athletic achievements.
    Output:
    [list of topic numbers]
    Ensure your output could be parsed to **list**, don't output anything else."""

    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "system",
                                                  "content": prompt
                                              }])

    topics = response.choices[0].message.content.strip()
    return json.loads(topics)


def generate_user_profile(age, gender, mbti, profession, topics):
    prompt = f"""Please generate a detailed social media user profile based on the provided personal information. Create a realistic and coherent persona that reflects all given characteristics.
    Input:
        age: {age}
        gender: {gender}
        mbti: {mbti}
        profession: {profession}
        interested topics: {topics}
        
    Requirements for the output:
    1. realname: Should match the gender and be culturally appropriate
    2. username: Should be creative and potentially reflect their interests or personality
    3. bio: Write a compelling 2-3 sentence bio that reflects their personality and interests
    4. persona: Create a detailed background story (3-4 sentences) that includes:
       - Their professional journey and aspirations
       - Their personality traits and how they interact with others
       - Their typical online behavior and content preferences
       - Their life philosophy or values
       
    Output format:
    {{
        "realname": "str",
        "username": "str",
        "bio": "str",
        "persona": "str"
    }}
    
    Ensure the output can be directly parsed to **JSON**, do not output anything else."""

    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "system",
                                                  "content": prompt
                                              }])

    profile = response.choices[0].message.content.strip()
    return json.loads(profile)


def index_to_topics(index_lst):
    result = []
    for index in index_lst:
        topic = topic_dict[str(index)]
        result.append(topic)
    return result


def create_user_profile():
    while True:
        try:
            gender = get_random_gender()
            age = get_random_age()
            mbti = get_random_mbti()
            country = get_random_country()
            profession = get_random_profession()
            education = get_random_education()
            languages = get_random_languages()
            activity_level = get_random_activity_level()
            hobbies = get_random_hobbies()
            personality_traits = get_personality_traits()
            
            topic_index_lst = get_interested_topics(mbti, age, gender, country, profession)
            topics = index_to_topics(topic_index_lst)
            profile = generate_user_profile(age, gender, mbti, profession, topics)
            
            # 添加新的属性
            profile.update({
                'age': age,
                'gender': gender,
                'mbti': mbti,
                'country': country,
                'profession': profession,
                'education': education,
                'languages': languages,
                'activity_level': activity_level,
                'hobbies': hobbies,
                'personality_traits': personality_traits,
                'interested_topics': topics
            })
            return profile
        except Exception as e:
            print(f"Profile generation failed: {e}. Retrying...")


def generate_user_data(n):
    user_data = []
    start_time = datetime.now()
    max_workers = 100  # Adjust according to your system capability
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(create_user_profile) for _ in range(n)]
        for i, future in enumerate(as_completed(futures)):
            profile = future.result()
            user_data.append(profile)
            elapsed_time = datetime.now() - start_time
            print(f"Generated {i+1}/{n} user profiles. Time elapsed: "
                  f"{elapsed_time}")
    return user_data


def save_user_data(user_data, filename):
    with open(filename, 'w') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    N = 10000  # Target user number
    user_data = generate_user_data(N)
    output_path = 'experiment_dataset/user_data/user_data_10000.json'
    save_user_data(user_data, output_path)
    print(f"Generated {N} user profiles and saved to {output_path}")
