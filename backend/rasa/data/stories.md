## story_0
* request_story{"time": "bedtime"}
  - action_story_time
* give_time{"time": "10pm"}
  - action_story_time

## story_1
* request_story{"time": null}
  - action_story_time
* give_time{"time": "10pm"}
  - action_story_time

## story_2
* request_story{"time": null}
  - action_story_time
* give_time{"time": "bedtime"}
  - action_story_time
* give_time{"time": "10pm"}
  - action_story_time

## interactive_story_1
* request_story
    - action_story_time
    - slot{"time": null}
* give_time{"time": "10pm"}
    - slot{"time": "10pm"}
    - action_story_time
    - slot{"time": null}

## interactive_story_2
* request_story
    - action_story_time
    - slot{"time": null}
* request_story{"time": "bedtime"}
    - slot{"time": "bedtime"}
    - action_story_time
    - slot{"time": null}
* give_time{"time": "10pm"}
    - slot{"time": "10pm"}
    - action_story_time
    - slot{"time": null}

## interactive_story_3
* request_story{"time": "10pm"}
    - slot{"time": "10pm"}
    - action_story_time
    - slot{"time": null}

## interactive_story_4
* request_story{"time": "8am"}
    - slot{"time": "8am"}
    - action_story_time
    - slot{"time": null}

## interactive_story_1
* request_story
    - action_story_time
    - slot{"time": null}
* give_time{"time": "bedtime"}
    - slot{"time": "bedtime"}
    - action_story_time
    - slot{"time": null}
* give_time{"time": "10pm"}
    - slot{"time": "10pm"}
    - action_story_time
    - slot{"time": null}
