from django.urls import path
from .views import register,login,protected_test,logout,add_card,view_card, Delete_card, transaction_history, export_transactions_csv, api_documentation

urlpatterns = [
    path("register/",register,name='register'),
    path("login/",login,name="login"),
    path("protected_test/",protected_test,name="protected_test"),
    path("logout/", logout,name="logout"),
    path("add_card/",add_card, name="add_card"),
    path("view_card/", view_card,name="view_card"),
    path("Delete_card/<int:card_id>/", Delete_card, name = "delete_card"),
    path("transactions/", transaction_history,name="transactions"),
    path("transactions/export/",export_transactions_csv,name="export_transactions_csv"),
    path("docs/",api_documentation, name="api_documentation")
]