import json
from nlp import get_slides_images

# f'data/images/resized/{idx[i]}_{nums[i]}.jpg'

image_url = "https://aff5fa4925746bf9c161-fb36f18ca122a30f6899af8eef8fa39b.ssl.cf5.rackcdn.com/images/Masthead_Toad.17345b1513ac044897cfc243542899dce541e8dc.9afde10b.png"

def create_slide(image)
    slide = {
            "objectId": gen_uuid,
            "pageType": SLIDE,
            "pageElements": [],
            }

    picture = {
            "objectId": gen_uuid,
            "size": {
                    "width": 1920,
                    "height": 1080
                },
            "image": {
                    "contentUrl": image_url
                }
            }

    slide["pageElements"].append(picture)

    return slide


def create_presentation(presentationId)
    presentation = {
            "presentationId": presentationId,
            "slides": [],
            "title": "wumbo presentation"
            }

    for data in get_slides_images():
        idx = data[0]
        nums = data[1]
        presentation["slides"].append(create_slide())

    return presentation

    
    
