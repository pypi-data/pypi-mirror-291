import json 
import os 
from state_implementation.state import State
from state_implementation.image_screen import ImageScreen
from state_implementation.text_screen import TextScreen
from state_implementation.black_screen import BlackScreen

        
class JsonParser:
    def __init__(self, filename) -> None:
        with open(filename, 'r') as file:
            parsed_data = json.load(file)
        
        self.black_screen_marker = parsed_data["black_screen_marker"]
        self.black_screen_duration = parsed_data["black_screen_duration"]
        self.build_state_machine(parsed_data)
    
    def get_machine_state(self) -> list:
        return self.state_machine
    
    # build the state machine from the provided json
    def build_state_machine(self, parsed_data):
        created_states = []

        for state in parsed_data["screens"]:
            if state["type"] == "TEXT":
                created_states.append(
                    State(state["duration"], None, TextScreen(texts= state["texts"]))
                )
            elif state["type"] == "IMAGE":
                created_states.extend(
                    self.open_image_path(state["duration"], state["images_path"], marker=state["marker"]
                                    , rest_between_images=state["rest_between_images"], rest_at_the_end=state["rest_at_the_end"])
                )
            elif state["type"] == "BLACK":
                created_states.append(
                    State(state["duration"],None, BlackScreen(state["marker"]))
                )


        for index in range(len(created_states) - 1):
            created_states[index].next_state = created_states[index + 1]

        self.state_machine = created_states
    
    def open_image_path(self, duration, path, marker, rest_between_images, rest_at_the_end): 
        images_full_path, images_filename = get_images_from_path(path)
        current_image_index = 0
        new_states = []
        for image_full_path, image_filename in zip(images_full_path, images_filename):
            post_hash = image_filename.split("_")
            new_states.append(
                State(duration, None, ImageScreen(image_full_path, str(current_image_index) + post_hash[len(post_hash) - 1 ] ))
            )
            if rest_between_images: 
                new_states.append(
                    State(self.black_screen_duration, None, BlackScreen(self.black_screen_marker + "_" + str(current_image_index)))
                )
            current_image_index = current_image_index + 1
            
        if rest_at_the_end and not rest_between_images: 
            new_states.append(
                State(self.black_screen_duration, None, BlackScreen(self.black_screen_marker + "_" + str(current_image_index)))
            )
        elif not rest_at_the_end and rest_between_images: 
           new_states.pop() 

        return new_states
    
    
def get_images_from_path(directory_path):
    if not os.path.exists(directory_path):
        print(f"The directory '{directory_path}' does not exist.")
        return []
    
    filenames = [element for element in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, element))]
    return list(map(lambda x: os.path.join(directory_path, x), filenames)), list(filenames)