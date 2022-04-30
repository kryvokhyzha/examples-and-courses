# serving face_parser with different model servers

### Install face_parser as package
```
python setup.py install
```

### Serve BentoML
```
python make_service.py
bentoml serve FaceParserService:latest
```

## Torchserve

### Create torchserve mar file
```
torch-model-archiver -f --model-name rainnet --version 1.0 --serialized-file models/rainnet/weights/rainnet_netG_latest.ts --handler models/rainnet/rainnet_handler.py --export-path model_store
```

### Start torchserve
```
torchserve --start --model-store model_store/ --models faceparser=faceparser.mar --ncs
```

### Run prediction
```
curl http://127.0.0.1:8080/predictions/faceparser -F "image=@data/images/musk.jpg"
```

