from description import *


def happiness_score(posts):
    happiness_score = 0
    num_posts = len(posts)
    for post in posts:
        if 'caption_sentiment' in post:
            m = post['caption_sentiment']['magnitude']
            s = post['caption_sentiment']['score']
            happiness_score += s * m
    return happiness_score / num_posts


def dominent_sentiment(posts):
    sentiments = {}
    sentiments['anger'] = 0
    sentiments['joy'] = 0
    sentiments['sorrow'] = 0
    sentiments['surprised'] = 0

    num_posts = len(posts)
    for post in posts:
        for face in post['faces']:
            for key in face:
                if face[key] == 'VERY_LIKELY':
                    sentiments[key] += 1
                elif face[key] == 'LIKELY':
                    sentiments[key] += 0.8

    return sorted(sentiments, key=sentiments.get, reverse=True)


def average_num_people(posts):
    avg = 0
    num_posts = len(posts)
    for post in posts:
        avg += len(post['faces'])
    return float(avg) / num_posts


def favorite_object(posts):
    labels = {}
    for post in posts:
        for obj in post['labels']:
            if obj in labels:
                labels[obj] += 1
            else:
                labels[obj] = 1
    most_popular = sorted(labels, key=labels.get, reverse=True)[:5]

    return most_popular


def food_lover_index(posts):
    keywords = ['food', 'meal', 'lunch', 'dinner', 'cuisine', 'dessert']
    index = 0
    for post in posts:
        for obj in post['labels']:
            if obj in keywords:
                index += 1
    return float(index) / len(posts) * 100


def animal_lover_index(posts):
    keywords = {'cat', 'dog', 'animal', 'pet'}
    count = {'dog': 0, 'cat': 0}
    index = 0
    for post in posts:
        for obj in post['labels']:
            if obj in keywords:
                index += 1
                if obj in count:
                    count[obj] += 1
                else:
                    count[obj] = 1
    return (count, float(index) / len(posts) * 100)


def traveller_index(posts):
    places = {}
    for post in posts:
        if 'landmarks' in post:
            for place in post['landmarks']:
                if place in places:
                    places[place] += 1
                else:
                    places[place] = 1
    most_popular = sorted(places, key=places.get, reverse=True)[:3]

    return (most_popular, float(len(places)) / len(posts))


def metaanalysis(posts):
    des = []
    h = happiness_score(posts)
    if (h < -0.5):
        des.append(happiness[0])
    elif (h < -0.25):
        des.append(happiness[1])
    elif (h < 0):
        des.append(happiness[2])
    else:
        des.append(happiness[3])

    des.append(sentiments[dominent_sentiment(posts)[0]])

    a = average_num_people(posts)
    if a < 0.5:
        des.append(people[0])
    elif a > 2.5:
        des.append(people[1])

    o = objects
    for obj in favorite_object(posts):
        o += obj + ", "
    o = o[:-2] + '.'
    des.append(o)

    f = food_lover_index(posts)
    if f > 0.5:
        des.append(food[1])
    elif f > 0.25:
        des.append(food[0])

    an, idx = animal_lover_index(posts)
    if idx > 0.1:
        des.append(animal_lover)
    if (an['dog'] > an['cat']):
        des.append(ritual_animal + 'dog.')
    elif (an['cat'] > an['dog']):
        des.append(ritual_animal + 'cat.')

    plcs, idx = traveller_index(posts)
    if (idx > 0.1):
        des.append(traveller)
        p = places
        for plc in plcs:
            p += plc + ', '
        p = p[:-2] + '.'
        des.append(p)

    return des

##################### BODY ##########################
# with open('C:\\Users\\Admin\\Desktop\\hackathon\\agrim_analysed.json',
#           encoding='utf-16') as json_file:
#     json_data = json.load(json_file)
#
# metaanalysis(json_data)
