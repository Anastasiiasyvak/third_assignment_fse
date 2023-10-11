import requests
from datetime import datetime, timedelta
import pytz

timezone = pytz.timezone("Europe/Kyiv")

languagees = {
    'eng': {
        'just_now': 'just now',
        'less_than_a_minute_ago': 'less than a minute ago',
        'couple_of_minutes_ago': 'couple of minutes ago',
        'hour_ago': 'hour ago',
        'today': 'today',
        'yesterday': 'yesterday',
        'this_week': 'this week',
        'long_time_ago': 'long time ago'
    },
    'ukr': {
        'just_now': 'щойно',
        'less_than_a_minute_ago': 'менше хвилини тому',
        'couple_of_minutes_ago': 'декілька хвилин тому',
        'hour_ago': 'годину тому',
        'today': 'сьогодні',
        'yesterday': 'вчора',
        'this_week': 'цього тижня',
        'long_time_ago': 'давно'
    },

        'it': {
        'just_now': 'proprio ora',
        'less_than_a_minute_ago': 'meno di un minuto fa',
        'couple_of_minutes_ago': 'alcuni minuti fa',
        'hour_ago': "un'ora fa",
        'today': 'oggi',
        'yesterday': 'ieri',
        'this_week': 'questa settimana',
        'long_time_ago': 'molto tempo fa'
    },
    'fr': {
        'just_now': 'juste maintenant',
        'less_than_a_minute_ago': 'il y a moins d une minute',
        'couple_of_minutes_ago': 'il y a quelques minutes',
        'hour_ago': 'il y a une heure',
        'today': 'aujourd hui',
        'yesterday': 'hier',
        'this_week': 'cette semaine',
        'long_time_ago': 'il y a longtemps'
    }
}

def last_seen_task(last_seen, selected_language):
    now = datetime.now(timezone)
    last_seen = last_seen.split(".")[0]
    last_time_online = datetime.fromisoformat(last_seen)
    last_time_online = last_time_online.replace(tzinfo=pytz.UTC)
    last_time_online = last_time_online.astimezone(timezone)
    time = now - last_time_online

    if time < timedelta(seconds=30):
        return languagees[selected_language]['just_now']
    elif time < timedelta(minutes=1):
        return languagees[selected_language]['less_than_a_minute_ago']
    elif time < timedelta(minutes=60):
        return languagees[selected_language]['couple_of_minutes_ago']
    elif time < timedelta(minutes=120):
        return languagees[selected_language]['hour_ago']
    elif time < timedelta(hours=24):
        return languagees[selected_language]['today']
    elif time < timedelta(hours=48):
        return languagees[selected_language]['yesterday']
    elif time < timedelta(days=7):
        return languagees[selected_language]['this_week']
    else:
        return languagees[selected_language]['long_time_ago']


def fetch_user_data(offset):
    url = f'https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        return []


def get_user_data():
    offset = 0
    user_data = []

    while True:
        users = fetch_user_data(offset)

        if not users:
            break

        user_data.extend(users)
        offset += len(users)

    return user_data


def main():
    selected_language = input("Choose language (ukr, eng, it, fr): ")

    user_data = get_user_data()

    for user in user_data:
        username = user.get('nickname', 'unknown user')
        last_seen = user.get('lastSeenDate', None)
        if last_seen:
            time_of_visit = last_seen_task(last_seen, selected_language)
            print(f"{username} was online {time_of_visit}")
        else:
            print(f"{username} now online")


if __name__ == '__main__':
    main()
