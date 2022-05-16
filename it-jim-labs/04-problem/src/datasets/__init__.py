import warnings
warnings.filterwarnings("ignore")


def prepare_data_for_disc_model(image, transform,):
    return transform(image).unsqueeze(0)


def prepare_data_for_autoencoder_model(image, transform,):
    return transform(image).unsqueeze(0)
