from abc import abstractmethod, ABC


class VideoWorkerInterface(ABC):

    @abstractmethod
    def main(self):
        """
        Main func to check for:
            - check for updates from mongo
            - download file
            - process file
            - upload preview
            - update collection in db
        """
        pass

    @abstractmethod
    def get_tasks(self):
        pass

    @abstractmethod
    def load_file(self):
        pass

    @abstractmethod
    def process_file(self):
        pass

    @abstractmethod
    def return_task(self):
        pass
