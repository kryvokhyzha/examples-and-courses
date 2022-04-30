from parser_service.service import FaceParserService

if __name__ == "__main__":
    service = FaceParserService(serving=True)
    service.save()
