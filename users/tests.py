from django_rest_passwordreset.models import ResetPasswordToken

ResetPasswordToken.objects.create(user_id=2, user_agent="user-agent", ip_address="100.100.100.100")