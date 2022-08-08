from feedback.models import Token
from operations import validate_token

print(type(validate_token("283F-F5DD")) is Token)
