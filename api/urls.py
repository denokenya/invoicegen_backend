from django.urls import include, path
from rest_framework import routers
from account.views import *
from sales.views import *
from stock.views import *
from purchase.views import *
from batch.views import *
from production.views import *
from invoicegen_backend import settings
from rest_framework_jwt.views import (
    obtain_jwt_token,
    verify_jwt_token,
    refresh_jwt_token,
)
from account.models import Department


router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"userconfigs", UserConfigViewSet, basename="userconfig")
router.register(r"companys", CompanyViewSet, basename="company")
router.register(r"plants", PlantViewSet, basename="plant")
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(r"stocks", StockViewSet, basename="stock")
router.register(r"rawmaterials", RawMaterialViewSet, basename="rawmaterial")
router.register(
    r"rawmaterialentrys", RawMaterialEntryViewSet, basename="rawmaterialentry"
)
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(
    r"employeeaddresses", EmployeeAddressViewSet, basename="employeeaddress"
)
router.register(r"drivers", DriverViewSet, basename="driver")
router.register(r"driveraddresses", DriverAddressViewSet, basename="driveraddress")
router.register(r"vehicles", VehicleViewSet, basename="vehicle")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(
    r"customersaddresses", CustomerAddressViewSet, basename="customersaddress"
)
router.register(r"vendors", VendorViewSet, basename="vendor")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"addresses", AddressViewSet, basename="address")
router.register(r"usernotes", UserNoteViewSet, basename="usernote")
router.register(r"taxes", TaxViewSet, basename="taxes")
router.register(r"companysettings", CompanySettingViewSet, basename="companysetting")
router.register(r"companyaddresss", CompanyAddressViewSet, basename="companyaddress")
router.register(r"plantsaleorders", PlantSaleOrderViewSet, basename="plantsaleorder")
router.register(r"emailtemplates", EmailTemplateViewSet, basename="emailtemplate")
router.register(
    r"termsandconditions", TermAndConditionViewSet, basename="termsandcondition"
)
router.register(r"plantsaleorders", PlantSaleOrderViewSet, basename="plantsaleorder")


urlpatterns = [
    path("", include(router.urls)),
    # Sale Order
    path("saleorders/", SaleOrderViewSet.as_view()),
    path("saleorders/<int:id>", SaleOrderViewSet.as_view()),
    # Invoice
    path("invoices/", InvoiceViewSet.as_view()),
    path("invoices/<int:id>", InvoiceViewSet.as_view()),
    # idgen
    path("idsmap/", IdsMapView.as_view()),
    path("idsmap/<int:id>", IdsMapView.as_view()),
    path("serialno/", IdsView.as_view()),
    path("serialno/<int:id>", IdsView.as_view()),
    # outstanding
    path("customeroutstanding/", OutstandingViewSet.as_view()),
    path("customeroutstanding/<int:id>", OutstandingViewSet.as_view()),
    # payments
    path("payments/", PaymentView.as_view()),
    path("payments/<uuid:id>", PaymentView.as_view()),
    # email api
    path("sendmail/", sendMail),
    # chart api
    path("getgraphdata/", graphData),
    # last fives
    path("getlastfive/", getLastFive),
    # api auth
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", obtain_jwt_token),
    path("api-token-verify/", verify_jwt_token),
    path("api-token-refresh/", refresh_jwt_token),
]