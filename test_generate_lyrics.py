from model.model_class import LyricGenerationModel
import config
model = LyricGenerationModel()
model.load(config.current_model)
print(model.generate_text())