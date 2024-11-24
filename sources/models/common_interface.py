import json

class BaseTest:
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
        obj = cls.__new__(cls)  # Bypass __init__
        for key, value in data.items():
            # If the attribute is a nested Serializable object, deserialize it
            if isinstance(getattr(cls, key, None), type) and issubclass(getattr(cls, key), BaseTest):
                setattr(obj, key, getattr(cls, key).from_dict(value))
            elif isinstance(getattr(cls, key, None), list):
                # If it's a list, deserialize each item if it's a Serializable object
                setattr(obj, key, [getattr(cls, key)[0].from_dict(item) if isinstance(getattr(cls, key)[0], BaseTest) else item for item in value])
            else:
                setattr(obj, key, value)
        return obj

    @classmethod
    def from_json(cls, json_string):
        """Instantiate an object from a JSON string."""
        print(json_string)
        data = json.loads(json_string)
        return cls.from_dict(data)