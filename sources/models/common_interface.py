import json

class BaseTest:
    """This class helps in transforming its sub-classes to json easily. 
    It also helps in creating the object back from those stored jsons."""

    def to_dict(self):
        """Automatically convert attributes to a dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, BaseTest):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                # If the attribute is a list, serialize its items recursively
                result[key] = [item.to_dict() if isinstance(item, BaseTest) else item for item in value]
            else:
                result[key] = value
        return result

    def to_json(self):
        """Convert the object to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_dict(cls, data):
        """Instantiate an object from a dictionary."""
        obj = cls.__new__(cls)  # Create a new instance without calling __init__
        for key, value in data.items():
            attr_type = getattr(cls, key, None)  # Get the type of the attribute if defined
            
            if isinstance(value, dict):
                # If value is a dictionary, recursively create an object
                nested_class = getattr(cls, key, BaseTest)  # Default to BaseTest if no specific type is defined
                setattr(obj, key, nested_class.from_dict(value))
            elif isinstance(value, list):
                # If value is a list, check if it's a list of nested objects
                list_items = []
                for item in value:
                    if isinstance(item, dict):
                        # Assume nested objects should be of BaseTest or derived type
                        nested_item_class = getattr(cls, key, [BaseTest])[0]
                        list_items.append(nested_item_class.from_dict(item))
                    else:
                        list_items.append(item)
                setattr(obj, key, list_items)
            else:
                # Set the value directly for simple types
                setattr(obj, key, value)
        return obj

    @classmethod
    def from_json(cls, json_input):
        """Instantiate an object from a JSON string or a dictionary."""
        # Check if the input is already a dictionary
        if isinstance(json_input, dict):
            data = json_input
        elif isinstance(json_input, str):
            data = json.loads(json_input)
        else:
            raise TypeError("Input to from_json must be a JSON string or a dictionary.")
        
        return cls.from_dict(data)