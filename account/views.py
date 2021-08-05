from api.views import *
from account.models import *
from account.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CompanyViewSet(viewsets.ModelViewSet):

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class CompanyAddressViewSet(viewsets.ModelViewSet):
    queryset = CompanyAddress.objects.all()
    serializer_class = CompanyAddressSerializer


class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class VendorViewSet(viewsets.ModelViewSet):

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class CustomerAddressViewSet(viewsets.ModelViewSet):
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerAddressSerializer


class AddressViewSet(viewsets.ModelViewSet):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class UserNoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserNote.objects.all()
    serializer_class = UserNoteSerializer


class CompanySettingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CompanySetting.objects.all()
    serializer_class = CompanySettingSerializer


class IdsView(APIView):
    def get(self, request, **kwargs):
        out = []
        data = request.query_params
        if len(data) != 0:
            idfor = data["FOR"]
            genWithName(idfor, update=True)
            ids = Ids.objects.filter(name=idfor)
            if len(ids) != 0:
                serials = IdsSerializer(ids, many=True).data
                out = serials
            else:
                print(out)
        else:
            # recalculateIds()
            serials = IdsSerializer(Ids.objects.all(), many=True).data
            out = serials
        return Response(data=out, status=201)

    def post(self, request):
        out = {}
        data = request.data
        serial = Ids(**data)
        serializer = IdsSerializer(serial)
        serializer = IdsSerializer(data=serializer.data)
        valid = serializer.is_valid()
        if valid == True:
            serial.save()
            c, n = genWithName(serial.name, id=serial.id)[0]
            serial.current = c
            serial.upnext = n
            out = IdsSerializer(serial).data
        else:
            out = serializer.errors
        return Response(data=out, status=201)

    def put(self, request, id):
        out = {}
        data = request.data
        serial = Ids.objects.get(id=id)

        today, year, month = getTodayYearMonth()
        padding = 5 if data["name"] == "INVOICE" else 4
        filler = {
            "year": year,
            "month": month,
            "count": formatint(int(data["count"]) + 1, padding),
            "prefix": data["prefix"],
        }
        current = handleMask(data["mask"], data["sep"], filler)
        filler["count"] = formatint(int(filler["count"]) + 1, padding)
        upnext = handleMask(data["mask"], data["sep"], filler)
        data["current"] = current
        data["upnext"] = upnext
        serializer = IdsSerializer(instance=serial, data=data, partial=True)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            out = serializer.data
        else:
            out = serializer.errors
        print(out)
        return Response(data=out, status=201)

    def delete(self, request, id):
        out = {}
        ids = Ids.objects.get(id=id)
        out = IdsSerializer(ids).data
        ids.delete()
        return Response(data=out, status=201)


class IdsMapView(APIView):
    def get(self, request, **kwargs):
        out = []
        data = request.query_params
        if len(data) != 0:
            idname = data["NAME"]
            genWithName(idname)
            ids = IdsMap.objects.filter(name=idname)
            if len(ids) != 0:
                serials = IdsMapSerializer(ids[0]).data
                out = serials
            else:
                out = []
        else:
            serials = IdsMapSerializer(IdsMap.objects.all(), many=True).data
            out = serials
        return Response(data=out, status=201)

    def post(self, request):
        out = {}
        data = request.data
        data["ids"] = Ids.objects.get(id=data["ids"])
        serialmap = IdsMap(**data)
        serializer = IdsMapSerializer(serialmap)
        serializer = IdsMapSerializer(data=serializer.data)
        valid = serializer.is_valid()
        if valid == True:
            serialmap.save()
            out = IdsMapSerializer(serialmap).data
        else:
            out = serializer.errors
        return Response(data=out, status=201)

    def put(self, request, id):
        out = {}
        data = request.data
        serialmap = IdsMap.objects.get(id=id)
        serialmap.ids = Ids.objects.get(id=data["ids"])
        serialmap.save()
        out = IdsMapSerializer(serialmap).data
        return Response(data=out, status=201)

    def delete(self, request, id):
        out = {}
        idsMap = IdsMap.objects.get(id=id)
        out = IdsSerializer(idsMap).data
        idsMap.delete()
        return Response(data=out, status=201)


class TaxViewSet(viewsets.ModelViewSet):

    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer


class TermAndConditionViewSet(viewsets.ModelViewSet):
    queryset = TermAndCondition.objects.all()
    serializer_class = TermAndConditionSerializer