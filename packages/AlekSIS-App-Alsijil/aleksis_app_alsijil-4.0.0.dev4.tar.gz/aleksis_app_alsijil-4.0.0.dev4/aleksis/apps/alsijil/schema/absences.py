from datetime import datetime

from django.core.exceptions import PermissionDenied

import graphene

from aleksis.apps.kolego.models import Absence
from aleksis.core.models import Person

from ..models import ParticipationStatus
from .participation_status import ParticipationStatusType


class AbsencesForPersonsCreateMutation(graphene.Mutation):
    class Arguments:
        persons = graphene.List(graphene.ID, required=True)
        start = graphene.Date(required=True)
        end = graphene.Date(required=True)
        comment = graphene.String(required=False)
        reason = graphene.ID(required=True)

    ok = graphene.Boolean()
    participation_statuses = graphene.List(ParticipationStatusType)

    @classmethod
    def mutate(cls, root, info, persons, start, end, comment, reason):  # noqa
        participation_statuses = []

        persons = Person.objects.filter(pk__in=persons)

        for person in persons:
            if not info.context.user.has_perm("alsijil.register_absence_rule", person):
                raise PermissionDenied()
            kolego_absence, __ = Absence.objects.get_or_create(
                date_start=start,
                date_end=end,
                reason_id=reason,
                person=person,
                defaults={"comment": comment},
            )

            events = ParticipationStatus.get_single_events(
                datetime.combine(start, datetime.min.time()),
                datetime.combine(end, datetime.max.time()),
                None,
                {"person": person},
                with_reference_object=True,
            )

            for event in events:
                participation_status = event["REFERENCE_OBJECT"]
                participation_status.absence_reason_id = reason
                participation_status.base_absence = kolego_absence
                participation_status.save()
                participation_statuses.append(participation_status)

        return AbsencesForPersonsCreateMutation(
            ok=True, participation_statuses=participation_statuses
        )
