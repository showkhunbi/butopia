from django.urls import path
from .views import HomeView, PaymentView, verify_transaction, PromoterProfileView, PromoterDashboardView, ReferredView, referrer_payment_view, CashoutView, PortfolioView, ContactView, download


app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(), name="homeview"),
    path('portfolio/', PortfolioView.as_view(), name="portfolio"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('payment/', PaymentView.as_view(), name="paymentview"),
    path('payment/<slug>/', referrer_payment_view, name="referrerPaymentView"),
    path('verify_transaction/', verify_transaction, name="verify"),
    path('accounts/profile/', PromoterProfileView.as_view(), name="profile"),
    path('accounts/dashboard/', PromoterDashboardView.as_view(), name="dashboard"),
    path('promoter/', PromoterDashboardView.as_view(), name="promoter"),
    path('accounts/referred/', ReferredView.as_view(), name="referred"),
    path('accounts/cashout/', CashoutView.as_view(), name="cashout"),
    path('download/', download, name="download"),
]
