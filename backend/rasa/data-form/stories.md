## story_0
* request_story
  - story_form
  - form{"name": "story_form"}
  - form{"name": null}
  - utter_read_story

## story_1
* greet
  - utter_greet
* request_story
  - story_form
  - form{"name": "story_form"}
  - form{"name": null}
  - utter_read_story

## story_2
* request_story
  - story_form
  - form{"name": "story_form"}
* give_time
  - story_form
  - form{"name": null}
  - utter_read_story

## story_3
* request_story
  - story_form
  - form{"name": "story_form"}
* give_time
  - story_form
  - slot{"requested_slot": "time"}
* give_time
  - story_form
  - form{"name": null}
  - utter_read_story

## story_4
* greet
  - utter_greet
* request_story
  - story_form
  - form{"name": "story_form"}
* give_time
  - story_form
  - slot{"requested_slot": "time"}
* give_time
  - story_form
  - form{"name": null}
  - utter_read_story

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
