from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # Sets the default type for auto-created primary key fields
    name = 'accounts' # Define the name of the application
