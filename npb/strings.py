start_command_response = """
North Pole Buddy is ready, Ho ho ho

You can send directly your messages and I will answer.

I also accept pictures with your query as a caption, and location for some Christmas Fun

Use the /delcontext command to reset the LLM context
"""

context_cleared = "Context cleared"
vision_no_answer = "Oops! Looks like your picture is empty. Please send another one! 🎅"
wrong_token = "Wrong or missing secret token"
cannot_serialize = "Cannot serialize Telegram Update"

# Prompts & fragments

act_as_santa = "Act and respond in the voice and tone of Santa Claus"
add_vision_context = "Keep this message for context, don't answer it directly:\n"

location_story = """
Based on the gps coordinates provided by the user, Give me a funny christmas story about the location of the user.
When you reply, don't mention the gps coordinates. But you can mention the town name or the region name

The user localisation is: {coords}
"""

location_gifts = """
Based on the gps coordinates provided by the user, create a list of 10 christmas gift based and culture, tradition and specialty for that area.
When you reply, don't mention the gps coordinates but the town or region of the user.

The user localisation is: {coords}
"""

location_visits = """
Based on the gps coordinates provided by the user, suggest somes places to visit for that region.
Theses places must have a link to christmas
When you reply, don't mention the gps coordinates but the town or region of the user.

The user localisation is: {coords}
"""
