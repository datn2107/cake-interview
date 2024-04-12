from pydantic import BaseModel

class MongoDbBaseModel(BaseModel):
    @classmethod
    def model_validate_mongodb(cls, data: dict | None) -> BaseModel:
        if data is None:
            return None
        
        data["id"] = data.pop("_id").__str__()
        return cls.model_validate(data)
