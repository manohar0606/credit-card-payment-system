from django.shortcuts import render
import json
import jwt
from datetime import datetime,timezone,timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password,check_password
from  django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .authentication import get_authenticated_user
from .models import Cards, Transactions, BlacklistedToken
import csv
import re

# Create your views here.
User = get_user_model()
@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse(
            {"error":"Only POST method allowed here"},
            status=405
        )
    try:
        data = json.loads   (request.body)
        username = data.get('username')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        if not username or not email or not password:
            return JsonResponse(
                {"error":"All the fields are manditory"},
                status = 400
            )
        if not re.match(r"^[A-Za-z0-9_]+$", username):
            return JsonResponse(
                {
                    "ERROR": "Invalid Username: Username can contain only letters, numbers and underscore"
                },
                status = 400
            )
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            return JsonResponse(
        {
            "ERROR": "Invalid Email format"
        },
        status=400
    )
        if len(password) < 8:
            return JsonResponse(
                {"ERROR": "Password must contain at least 8 characters"},
                status=400
            )

        if not re.search(r"[A-Z]", password):
            return JsonResponse(
                {"ERROR": "Password must contain at least one uppercase letter"},
                status=400
            )

        if not re.search(r"[a-z]", password):
            return JsonResponse(
                {"ERROR": "Password must contain at least one lowercase letter"},
                status=400
            )

        if not re.search(r"\d", password):
            return JsonResponse(
                {"ERROR": "Password must contain at least one number"},
                status=400
    )
        
        if User.objects.filter(username= username).exists():
            return JsonResponse(
                {"error":"Username already exists"},
                status = 400
            )
        if User.objects.filter(email = email).exists():
            return JsonResponse(
                {"error":"Email already exists"},
                status = 400
            )
        user = User.objects.create(
            username= username,
            email = email,
            first_name = first_name,
            last_name = last_name,
            password=make_password(password)
        )
        return JsonResponse(
            {"message":"User created successfully",
            "User":{
                "id":user.id,
                "username":user.username,
                "email":user.email,
                "First name":user.first_name,
                "Last name":user.last_name
            }},
            status = 201
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"error":"Invalid JSON"},
            status = 400
        )
@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse(
            {"error":"Only POST method are allowed here"},
            status = 405
        )
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse(
                {"error":"Username and Password required"},
                status = 400
            )
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse(
                {"error":"User not exists"},
                status = 400
            )
        if not check_password(password,user.password):
            return JsonResponse(
                {"error":"Invalid username or password"},
                status = 400
            )
        payload = {
    "user_id": user.id,
    "username": user.username,
    "first_name": user.first_name,
    "last_name": user.last_name,
    "iat": datetime.now(timezone.utc),
    "exp": datetime.now(timezone.utc) + timedelta(hours=1)
}
        

        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm="HS256"

        )

        return JsonResponse(
            {"message":"Login Successfully",
            "access_token":token,
            "token type":"Bearer",
            "User":{
                "User id":user.id,
                "username":user.username,
                "Email":user.email
            }
            }

        )
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "Invalid JSON"
            },
            status=400
        )
@csrf_exempt
def protected_test(request):

    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    user, error = get_authenticated_user(request)

    if error:
        return error

    return JsonResponse(
        {
            "message": "Authentication successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    )

@csrf_exempt
def logout(request):

    if request.method != 'POST':
        return JsonResponse(
            {"error": "Only POST method is accepted here"},
            status=405
        )

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse(
            {"error": "Authorization header is required"},
            status=401
        )

    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return JsonResponse(
            {"error": "Invalid Authorization header format"},
            status=401
        )

    token = parts[1]

    user, error = get_authenticated_user(request)

    if error:
        return error

    BlacklistedToken.objects.get_or_create(token=token)

    return JsonResponse(
        {
            "message": "Logout Successfully",
            "user": user.username
        },
        status=200
    )
@csrf_exempt
def add_card(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method is allowed"},
            status=405
        )

    user, error = get_authenticated_user(request)

    if error:
        return error

    try:
        data = json.loads(request.body)

        card_type = data.get("card_type")
        card_number = data.get("card_number")
        expiry_date = data.get("expiry_date")
        card_holder_name = data.get("card_holder_name")

        if not card_type or not card_number or not expiry_date or not card_holder_name:
            return JsonResponse(
                {"error": "All fields must be filled"},
                status=400
            )

        card_type = card_type.upper()

        if not re.match(r"^[A-Za-z]+$", card_holder_name):
            return JsonResponse(
                {
                    "error":"Card holder name can contain only latters and one space"
                }, status = 400
            )
        if not re.match(r"^(0[1-9]|1[0-2])-[0-9]{2}$", expiry_date):
            return JsonResponse(
                {
                    "ERROR": "the expiry date format is MM-YY"
                },
                status=400
            )

        if card_type not in ["CREDIT", "DEBIT"]:
            return JsonResponse(
                {"error": "Card type must be CREDIT or DEBIT"},
                status=400
            )

        card_number = card_number.replace(" ", "")

        if not card_number.isdigit():
            return JsonResponse(
                {"error": "Card number must contain only digits"},
                status=400
            )

        if len(card_number) not in [13, 14, 15, 16, 17, 18, 19]:
            return JsonResponse(
                {"error": "Invalid card number"},
                status=400
            )

        last_four_digits = card_number[-4:]

        masked_card_number = "*" * (len(card_number) - 4) + last_four_digits

        card = Cards.objects.create(
            user=user,
            card_type=card_type,
            card_number=masked_card_number,
            last_four_digit=last_four_digits,
            expiry_data=expiry_date,
            card_holder_name=card_holder_name
        )

        return JsonResponse(
            {
                "message": "Card created successfully",
                "card": {
                    "id": card.id,
                    "card_type": card.card_type,
                    "card_number": card.card_number,
                    "last_four_digit": card.last_four_digit,
                    "expiry_data": card.expiry_data,
                    "card_holder_name": card.card_holder_name
                }
            },
            status=201
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )
@csrf_exempt
def view_card(request):
    if request.method != 'GET':
        return JsonResponse(
            {
                "error":"Only get methon is allowed"
            }
        )
    user, error = get_authenticated_user(request)

    if error:
        return error

    card_list = []

    try:
        card = Cards.objects.filter(user=user)
        for i in card:
            card_list.append({
                "card Id":i.id,
                "Card Number":i.card_number,
                "Card Holder_name":i.card_holder_name,
                "Expiry Date":i.expiry_data,
                "Card_type":i.card_type
            }

            )

        return JsonResponse(
            {
                "Message":"Card Details fetched successfully",
                "card":card_list
            
        }
        ,status = 200)
    except:
        return JsonResponse(
            {
                "Error":"Invalid user or card not found "
            },
            status = 400
        )
@csrf_exempt
def Delete_card(request,card_id):
    if request.method != "DELETE":
        return JsonResponse(
            {"ERROR":"Only DELETE method will accept here"},
            status = 400
        )

    user, error = get_authenticated_user(request)

    if error:
        return error

    try:
        card = Cards.objects.filter(
            id = card_id,
            user = user
        )
    except:
        return JsonResponse(
            {
                "ERROR":"Card not found"
            },status = 400
        )
    card.delete()

    return JsonResponse(
        {"Message":"Card Deleted Successfully"},
        status = 200
    )
@csrf_exempt
def transaction_history(request):

    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    user, error = get_authenticated_user(request)

    if error:
        return error

    transactions = Transactions.objects.filter(
        user=user
    ).order_by("-timestamp")
    status_filter = request.GET.get("status")
    if status_filter:
        transactions = transactions.filter(
            status = status_filter.upper()
        )
    amount_filter = request.GET.get("amount")
    if amount_filter:
        try:
            transactions = transactions.filter(
                amount = float(amount_filter)
            )
        except ValueError:
            return JsonResponse(
                {"error":"Invalid amount"},
                status = 400
            )
    date_filter = request.GET.get("date")
    if date_filter:
        try:
            date_value = datetime.strptime(
                date_filter,
                "%Y-%m-%d"
            ).date()
            transactions = transactions.filter(
                timestamp__date=date_value
            )
        except ValueError:
            return JsonResponse(
                {
                    "error":"Invalid date. Use YYYY-MM-DD"
                },
                status = 400
            )
    transaction_list = []

    for transaction in transactions:
        transaction_list.append({
            "id": transaction.id,
            "card_id": transaction.card.id,
            "amount": float(transaction.amount),
            "status": transaction.status,
            "timestamp": transaction.timestamp
        })

    return JsonResponse({
        "transactions": transaction_list
    }, status=200)

def export_transactions_csv(request):
    if request.method != 'GET':
        return JsonResponse(
            {
                'ERROR':"Only get method is allowed here"
            }, status = 405
        )
    user, error = get_authenticated_user(request)
    if error:
        return error
    if not user.is_staff:
        return JsonResponse(
            {
                "ERROR":"Admin access required"
            },
            status = 403
        )
    transactions = Transactions.objects.all().select_related(
        "user",
        "card"
    ).order_by("-timestamp")

    response = HttpResponse(content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="transactions.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Transaction ID",
        "User",
        "Card ID",
        "Amount",
        "Status",
        "Timestamp"
    ])

    for i in transactions:
        writer.writerow([
            i.id,
            i.user.username,
            i.card.id,
            i.amount,
            i.status,
            i.timestamp

        ])
    return response
def api_documentation(request):
    return render(request,'api_docs.html')
