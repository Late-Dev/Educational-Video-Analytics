from abc import abstractmethod, ABC

from pydantic import BaseModel


class S3Interface(ABC):

    @abstractmethod
    def load_file(self, url: str):
        pass

    @abstractmethod
    def upload_file(self, url: str):
        pass


class BaseConnector(ABC):

    @abstractmethod
    def connect(self, url: str):
        pass

    @abstractmethod
    def update(self, datamodel: BaseModel):
        pass

    @abstractmethod
    def get_collection(self):
        pass
