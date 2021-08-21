import api.models
import django.contrib.auth.models
import django.db
from rest_framework import serializers
from account.models import *


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class PlantSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = Plant
        fields = "__all__"

    def get_address(self, obj):
        if obj.address:
            return AddressSerializer(obj.address.address).data
        else:
            return {}


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("password",)


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    settings = serializers.SerializerMethodField()
    plants = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"

    def get_settings(self, obj):
        if obj.companysetting_set.count() > 0:
            return CompanySettingSerializer(obj.companysetting_set.all()[0]).data
        else:
            return {}

    def get_address(self, obj):
        if obj.companyaddress_set.count() > 0:
            return AddressSerializer(obj.companyaddress_set.all()[0].address).data
        else:
            return {}

    def get_plants(self, obj):
        if obj.plant_set.count() > 0:
            return PlantSerializer(obj.plant_set.all()[0]).data
        else:
            return {}


class CompanyAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = CompanyAddress
        fields = "__all__"


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = "__all__"

    def get_addresses(self, obj):
        out = []
        if obj.customeraddress_set.count() > 0:
            arr = []
            for ca in obj.customeraddress_set.all():
                arr.append(AddressSerializer(ca.address).data)
            out = arr
        else:
            out = []
        return out


class IdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ids
        fields = "__all__"


class IdsMapSerializer(serializers.ModelSerializer):
    ids = IdsSerializer()

    class Meta:
        model = IdsMap
        fields = "__all__"


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = "__all__"


class UserNoteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserNote
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"

class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeType
        fields = "__all__"


class EmployeeSerializer(UserSerializer):
    addresses = serializers.SerializerMethodField()

    def get_addresses(self, obj):
        if obj.employeeaddress_set.count() > 0:
            return [
                AddressSerializer(e.address).data for e in obj.employeeaddress_set.all()
            ]
        else:
            return []

    class Meta:
        model = Employee
        fields = "__all__"


class DriverSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()

    def get_addresses(self, obj):
        if obj.driveraddress_set.count() > 0:
            return [
                AddressSerializer(e.address).data for e in obj.driveraddress_set.all()
            ]
        else:
            return []

    class Meta:
        model = Driver
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class VendorSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()

    def get_addresses(self, obj):
        if obj.vendoraddress_set.count() > 0:
            return AddressSerializer(obj.vendoraddress_set.all(), many=True).data
        else:
            return {}

    class Meta:
        model = Vendor
        fields = "__all__"


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = "__all__"


class TermAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermAndCondition
        fields = "__all__"


class CompanySettingSerializer(serializers.ModelSerializer):

    emailTemplates = serializers.SerializerMethodField()
    termsAndConditions = serializers.SerializerMethodField()

    def get_emailTemplates(self, obj):
        if obj.emailtemplate_set.count() > 0:
            return EmailTemplateSerializer(obj.emailtemplate_set.all(), many=True).data
        else:
            return {}

    def get_termsAndConditions(self, obj):
        if obj.termandcondition_set.count() > 0:
            return TermAndConditionSerializer(
                obj.termandcondition_set.all(), many=True
            ).data
        else:
            return {}

    class Meta:
        model = CompanySetting
        fields = "__all__"


class UserConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfig
        fields = "__all__"


class DriverAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverAddress
        fields = "__all__"


class EmployeeAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAddress
        fields = "__all__"