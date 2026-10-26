# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

# # class OrderHealthCheckView(APIView):
# #     def get(self, request):
# #         return Response({"message": "Orders API module is ready"})


# # # Create your views here.


# class OrderHealthCheckView(APIView):
#     # Sirf valid JWT token wale user ko access milega
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response(
#             {
#                 "message": f"Hello {request.user.username}, you are authenticated!",
#                 "user_id": request.user.id,
#             }
#         )


# import uuid
# from decimal import Decimal
# from django.db import transaction
# from django.utils import timezone
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from vouchers.models import Voucher
# from vouchers.crypto_utils import decrypt_voucher_code
# from .models import Order, IdempotencyLog, Wallet


# class WalletDetailView(APIView):
#     """
#     User ka fake balance check aur top-up karne ka endpoint
#     """

#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         wallet, _ = Wallet.objects.get_or_create(
#             user=request.user, defaults={"balance": 5000.00}
#         )
#         return Response(
#             {
#                 "username": request.user.username,
#                 "wallet_balance": str(wallet.balance),
#                 "currency": "INR (Test Fake Money)",
#             }
#         )

#     def post(self, request):
#         add_amount = Decimal(request.data.get("amount", 1000.00))
#         wallet, _ = Wallet.objects.get_or_create(
#             user=request.user, defaults={"balance": 5000.00}
#         )
#         wallet.balance += add_amount
#         wallet.save()
#         return Response(
#             {
#                 "message": f"Successfully credited ₹{add_amount} fake money!",
#                 "new_balance": str(wallet.balance),
#             }
#         )


# class VoucherCheckoutView(APIView):
#     """
#     Atomic Checkout: Concurrency Lock + Wallet Deduction + Decryption
#     """

#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         voucher_id = request.data.get("voucher_id")
#         idempotency_key = request.headers.get("X-Idempotency-Key") or request.data.get(
#             "idempotency_key"
#         )

#         if not voucher_id:
#             return Response(
#                 {"error": "voucher_id is required."}, status=status.HTTP_400_BAD_REQUEST
#             )

#         # 1. Idempotency Check (Duplicate double-click prevention)
#         if idempotency_key:
#             existing_log = IdempotencyLog.objects.filter(
#                 idempotency_key=idempotency_key
#             ).first()
#             if existing_log:
#                 return Response(
#                     existing_log.response_body, status=existing_log.status_code
#                 )

#         try:
#             with transaction.atomic():
#                 # 2. Concurrency Lock: Database row-level lock lagana
#                 voucher = (
#                     Voucher.objects.select_for_update()
#                     .filter(id=voucher_id, status="AVAILABLE")
#                     .first()
#                 )
#                 if not voucher:
#                     return Response(
#                         {"error": "Voucher is out of stock or already claimed."},
#                         status=status.HTTP_409_CONFLICT,
#                     )

#                 wallet, _ = Wallet.objects.select_for_update().get_or_create(
#                     user=request.user, defaults={"balance": 5000.00}
#                 )

#                 # 3. Wallet Balance Check
#                 if wallet.balance < voucher.sale_price:
#                     return Response(
#                         {
#                             "error": "Insufficient fake wallet balance.",
#                             "current_balance": str(wallet.balance),
#                             "voucher_price": str(voucher.sale_price),
#                         },
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )

#                 # 4. Deduct Fake Money
#                 wallet.balance -= voucher.sale_price
#                 wallet.save()

#                 # 5. Decrypt Voucher Code (AES-256)
#                 plain_code = decrypt_voucher_code(voucher.encrypted_code)

#                 # 6. Update Voucher Status
#                 voucher.status = "CLAIMED"
#                 voucher.claimed_by = request.user
#                 voucher.claimed_at = timezone.now()
#                 voucher.save()

#                 # 7. Create Order Record
#                 order = Order.objects.create(
#                     order_id=f"ORD-{uuid.uuid4().hex[:10].upper()}",
#                     user=request.user,
#                     voucher=voucher,
#                     amount_paid=voucher.sale_price,
#                     status="COMPLETED",
#                     idempotency_key=idempotency_key or str(uuid.uuid4()),
#                 )

#                 response_data = {
#                     "order_id": order.order_id,
#                     "status": "COMPLETED",
#                     "payment_method": "In-App Fake Wallet",
#                     "brand": voucher.brand,
#                     "title": voucher.title,
#                     "amount_deducted": str(voucher.sale_price),
#                     "remaining_wallet_balance": str(wallet.balance),
#                     "revealed_voucher_code": plain_code,
#                     "claimed_at": voucher.claimed_at.isoformat(),
#                 }

#                 # 8. Cache response for idempotency
#                 if idempotency_key:
#                     IdempotencyLog.objects.create(
#                         idempotency_key=idempotency_key,
#                         user=request.user,
#                         response_body=response_data,
#                         status_code=status.HTTP_201_CREATED,
#                     )

#                 return Response(response_data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response(
#                 {"error": f"Transaction failed: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

import uuid
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from vouchers.models import Voucher
from vouchers.crypto_utils import decrypt_voucher_code
from .models import Order, IdempotencyLog, Wallet


class OrderHealthCheckView(APIView):
    """
    JWT authentication verify karne ke liye health check
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "message": f"Hello {request.user.username}, you are authenticated!",
                "user_id": request.user.id,
            }
        )


class WalletDetailView(APIView):
    """
    User ka fake wallet balance check aur recharge karne ka endpoint
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(
            user=request.user, defaults={"balance": 5000.00}
        )
        return Response(
            {
                "username": request.user.username,
                "wallet_balance": str(wallet.balance),
                "currency": "INR (Test Fake Money)",
            }
        )

    def post(self, request):
        add_amount = Decimal(request.data.get("amount", 1000.00))
        wallet, _ = Wallet.objects.get_or_create(
            user=request.user, defaults={"balance": 5000.00}
        )
        wallet.balance += add_amount
        wallet.save()
        return Response(
            {
                "message": f"Successfully credited ₹{add_amount} fake money!",
                "new_balance": str(wallet.balance),
            }
        )


class VoucherCheckoutView(APIView):
    """
    Atomic Checkout: Concurrency Lock + Fake Wallet Deduction + AES-256 Decryption
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        voucher_id = request.data.get("voucher_id")
        idempotency_key = request.headers.get("X-Idempotency-Key") or request.data.get(
            "idempotency_key"
        )

        if not voucher_id:
            return Response(
                {"error": "voucher_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Idempotency Check (Duplicate order prevention)
        if idempotency_key:
            existing_log = IdempotencyLog.objects.filter(
                idempotency_key=idempotency_key
            ).first()
            if existing_log:
                return Response(
                    existing_log.response_body, status=existing_log.status_code
                )

        try:
            with transaction.atomic():
                # 2. Concurrency Lock: Database row par digital taala
                voucher = (
                    Voucher.objects.select_for_update()
                    .filter(id=voucher_id, status="AVAILABLE")
                    .first()
                )
                if not voucher:
                    return Response(
                        {"error": "Voucher is out of stock or already claimed."},
                        status=status.HTTP_409_CONFLICT,
                    )

                wallet, _ = Wallet.objects.select_for_update().get_or_create(
                    user=request.user, defaults={"balance": 5000.00}
                )

                # 3. Balance Check
                if wallet.balance < voucher.sale_price:
                    return Response(
                        {
                            "error": "Insufficient fake wallet balance.",
                            "current_balance": str(wallet.balance),
                            "voucher_price": str(voucher.sale_price),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # 4. Wallet Deduct
                wallet.balance -= voucher.sale_price
                wallet.save()

                # 5. Voucher Code Decrypt (AES-256)
                plain_code = decrypt_voucher_code(voucher.encrypted_code)

                # 6. Status Update
                voucher.status = "CLAIMED"
                voucher.claimed_by = request.user
                voucher.claimed_at = timezone.now()
                voucher.save()

                # 7. Order Create
                generated_order_id = f"ORD-{uuid.uuid4().hex[:10].upper()}"
                order = Order.objects.create(
                    order_id=generated_order_id,
                    user=request.user,
                    voucher=voucher,
                    amount_paid=voucher.sale_price,
                    status="COMPLETED",
                    idempotency_key=idempotency_key or str(uuid.uuid4()),
                )

                # 8. Success Response
                response_data = {
                    "order_id": order.order_id,
                    "status": "COMPLETED",
                    "payment_method": "In-App Fake Wallet",
                    "brand": voucher.brand,
                    "title": voucher.title,
                    "amount_deducted": str(voucher.sale_price),
                    "remaining_wallet_balance": str(wallet.balance),
                    "revealed_voucher_code": plain_code,
                    "claimed_at": voucher.claimed_at.isoformat(),
                }

                if idempotency_key:
                    IdempotencyLog.objects.create(
                        idempotency_key=idempotency_key,
                        user=request.user,
                        response_body=response_data,
                        status_code=status.HTTP_201_CREATED,
                    )

                return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            import traceback

            traceback.print_exc()  # Ab server terminal me poori error detail dikhegi
            error_message = (
                f"{type(e).__name__}: {str(e)}" if str(e) else type(e).__name__
            )
            return Response(
                {"error": f"Transaction failed: {error_message}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
