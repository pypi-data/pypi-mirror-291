from django.apps import apps

import graphene

from aleksis.apps.kolego.models.absence import AbsenceReasonTag
from aleksis.core.schema.base import FilterOrderList

from .absence import (
    AbsenceBatchCreateMutation,
    AbsenceBatchDeleteMutation,
    AbsenceBatchPatchMutation,
    AbsenceReasonBatchCreateMutation,
    AbsenceReasonBatchDeleteMutation,
    AbsenceReasonBatchPatchMutation,
    AbsenceReasonTagBatchCreateMutation,
    AbsenceReasonTagBatchDeleteMutation,
    AbsenceReasonTagBatchPatchMutation,
    AbsenceReasonTagType,
    AbsenceReasonType,
    AbsenceType,
)


class Query(graphene.ObjectType):
    app_name = graphene.String()
    absences = FilterOrderList(AbsenceType)
    absence_reasons = FilterOrderList(AbsenceReasonType)
    absence_reason_tags = FilterOrderList(AbsenceReasonTagType)
    all_absence_reason_tags = FilterOrderList(AbsenceReasonTagType)

    def resolve_app_name(root, info, **kwargs) -> str:
        return apps.get_app_config("kolego").verbose_name

    def resolve_all_absence_reason_tags(root, info, **kwargs):
        return AbsenceReasonTag.objects.managed_and_unmanaged()


class Mutation(graphene.ObjectType):
    create_absences = AbsenceBatchCreateMutation.Field()
    delete_absences = AbsenceBatchDeleteMutation.Field()
    update_absences = AbsenceBatchPatchMutation.Field()

    create_absence_reasons = AbsenceReasonBatchCreateMutation.Field()
    delete_absence_reasons = AbsenceReasonBatchDeleteMutation.Field()
    update_absence_reasons = AbsenceReasonBatchPatchMutation.Field()

    create_absence_reason_tags = AbsenceReasonTagBatchCreateMutation.Field()
    delete_absence_reason_tags = AbsenceReasonTagBatchDeleteMutation.Field()
    update_absence_reason_tags = AbsenceReasonTagBatchPatchMutation.Field()
