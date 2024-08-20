from django.core.exceptions import PermissionDenied

import graphene
from graphene_django import DjangoObjectType

from aleksis.apps.alsijil.models import NewPersonalNote, ParticipationStatus
from aleksis.apps.alsijil.schema.personal_note import PersonalNoteType
from aleksis.core.schema.base import (
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
)


class ParticipationStatusType(
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
    DjangoFilterMixin,
    DjangoObjectType,
):
    class Meta:
        model = ParticipationStatus
        fields = (
            "id",
            "person",
            "absence_reason",
            "related_documentation",
            "base_absence",
            "tardiness",
        )

    notes_with_extra_mark = graphene.List(PersonalNoteType)
    notes_with_note = graphene.List(PersonalNoteType)

    @staticmethod
    def resolve_notes_with_extra_mark(root: ParticipationStatus, info, **kwargs):
        return NewPersonalNote.objects.filter(
            person=root.person,
            documentation=root.related_documentation,
            extra_mark__isnull=False,
        )

    @staticmethod
    def resolve_notes_with_note(root: ParticipationStatus, info, **kwargs):
        return NewPersonalNote.objects.filter(
            person=root.person,
            documentation=root.related_documentation,
            note__isnull=False,
        )


class ParticipationStatusBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = ParticipationStatus
        fields = (
            "id",
            "absence_reason",
            "tardiness",
        )  # Only the reason and tardiness can be updated after creation
        return_field_name = "participationStatuses"

    @classmethod
    def check_permissions(cls, root, info, input, *args, **kwargs):  # noqa: A002
        pass

    @classmethod
    def after_update_obj(cls, root, info, input, obj, full_input):  # noqa: A002
        if not info.context.user.has_perm(
            "alsijil.edit_participation_status_for_documentation_rule", obj.related_documentation
        ):
            raise PermissionDenied()
