# -*- coding: utf-8 -*-
import rest_framework_filters as filters
from django.db import models
from rest_framework import serializers, viewsets, views, response

from .models import Member, MembershipApplication, MembershipApplicationTag, MemberType


class MemberTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MemberType


class MemberTypeFilter(filters.FilterSet):

    class Meta:
        model = MemberType
        fields = {
            'label': filters.ALL_LOOKUPS,
        }


class MemberTypeViewSet(viewsets.ModelViewSet):
    serializer_class = MemberTypeSerializer
    queryset = MemberType.objects.all()
    filter_class = MemberTypeFilter


class MembershipApplicationTagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MembershipApplicationTag
        fields = '__all__'


class MembershipApplicationTagFilter(filters.FilterSet):

    class Meta:
        model = MembershipApplicationTag
        fields = {
            'label': filters.ALL_LOOKUPS,
        }


class MembershipApplicationTagViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipApplicationTagSerializer
    queryset = MembershipApplicationTag.objects.all()
    filter_class = MembershipApplicationTagFilter


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    credit = serializers.CharField(source='credit_annotated', read_only=True)

    class Meta:
        model = Member
        fields = '__all__'


class MemberFilter(filters.FilterSet):

    class Meta:
        model = Member
        fields = {
            'nick': filters.ALL_LOOKUPS,
            'email': filters.ALL_LOOKUPS,
            'lname': filters.ALL_LOOKUPS,
            'fname': filters.ALL_LOOKUPS,
            'accepted': filters.ALL_LOOKUPS,
            'mtypes': filters.ALL_LOOKUPS,
            'anonymized_id': filters.ALL_LOOKUPS,
            'member_id': filters.ALL_LOOKUPS,
        }


class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all().annotate(credit_annotated=models.Sum('creditor_transactions__amount'))
    filter_class = MemberFilter


class MemberSinView(views.APIView):
    def get_queryset(self):
        members = Member.objects.all().annotate(credit_annotated=models.Sum('creditor_transactions__amount'))
        members = members.filter(credit_annotated__lt=0).order_by('credit_annotated')
        return members

    def get(self, request, format=None):
        members = self.get_queryset()
        serializer = MemberSerializer(members, many=True, context={'request': request})
        return response.Response(serializer.data)


class MembershipApplicationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MembershipApplication
        fields = '__all__'


class MembershipApplicationFilter(filters.FilterSet):

    class Meta:
        model = MembershipApplication
        fields = {
            'nick': filters.ALL_LOOKUPS,
            'email': filters.ALL_LOOKUPS,
            'lname': filters.ALL_LOOKUPS,
            'fname': filters.ALL_LOOKUPS,
            'received': filters.ALL_LOOKUPS,
            'tags': filters.ALL_LOOKUPS,
        }


class MembershipApplicationSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipApplicationSerializer
    queryset = MembershipApplication.objects.all()
    filter_class = MembershipApplicationFilter
