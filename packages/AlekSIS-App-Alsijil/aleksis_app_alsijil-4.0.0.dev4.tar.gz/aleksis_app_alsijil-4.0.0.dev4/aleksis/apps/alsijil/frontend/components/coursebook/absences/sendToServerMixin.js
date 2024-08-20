/**
 * Mixin to provide shared functionality needed to send updated participation data to the server
 */
import { updateParticipationStatuses } from "./participationStatus.graphql";
import mutateMixin from "aleksis.core/mixins/mutateMixin.js";

export default {
  mixins: [mutateMixin],
  methods: {
    sendToServer(participations, field, value) {
      let fieldValue;

      if (field === "absenceReason") {
        fieldValue = {
          absenceReason: value === "present" ? null : value,
        };
      } else if (field === "tardiness") {
        fieldValue = {
          tardiness: value,
        };
      } else {
        console.error(`Wrong field '${field}' for sendToServer`);
        return;
      }

      this.mutate(
        updateParticipationStatuses,
        {
          input: participations.map((participation) => ({
            id: participation?.id || participation,
            ...fieldValue,
          })),
        },
        (storedDocumentations, incomingStatuses) => {
          // TODO: what should happen here in places where there is more than one documentation?
          const documentation = storedDocumentations.find(
            (doc) => doc.id === this.documentation.id,
          );

          incomingStatuses.forEach((newStatus) => {
            const participationStatus = documentation.participations.find(
              (part) => part.id === newStatus.id,
            );
            participationStatus.absenceReason = newStatus.absenceReason;
            participationStatus.tardiness = newStatus.tardiness;
            participationStatus.isOptimistic = newStatus.isOptimistic;
          });

          return storedDocumentations;
        },
      );
    },
  },
};
