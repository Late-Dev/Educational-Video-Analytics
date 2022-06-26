def build_emotion_service():
    from infrastructure.detection import RetinaTorchDetector
    from infrastructure.classification import DanClassifier
    from infrastructure.tracking.wrapper import DeepsortTracker
    from service.emotion_service import EmotionService

    detector = RetinaTorchDetector(model_path='infrastructure/retina_torch/config.json', conf_thresh=0.9)
    classifier = DanClassifier(model_path='models/classifier.pth')
    tracker = DeepsortTracker("models/mars-small128.pb")

    service = EmotionService(detector, classifier, tracker)
    return service


