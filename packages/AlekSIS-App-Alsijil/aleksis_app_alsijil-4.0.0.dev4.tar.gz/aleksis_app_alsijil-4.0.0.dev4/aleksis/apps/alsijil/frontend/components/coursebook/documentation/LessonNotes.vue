<script setup>
import AbsenceReasonChip from "aleksis.apps.kolego/components/AbsenceReasonChip.vue";
import ExtraMarkChip from "../../extra_marks/ExtraMarkChip.vue";
import TardinessChip from "../absences/TardinessChip.vue";
</script>

<template>
  <div
    class="d-flex align-center justify-space-between justify-md-end flex-wrap gap"
  >
    <v-chip dense color="success" outlined v-if="total > 0">
      {{ $t("alsijil.coursebook.present_number", { present, total }) }}
    </v-chip>
    <absence-reason-chip
      v-for="[reasonId, participations] in Object.entries(absences)"
      :key="'reason-' + reasonId"
      :absence-reason="participations[0].absenceReason"
      dense
    >
      <template #append>
        <span
          >:
          <span>
            {{
              participations
                .slice(0, 5)
                .map((participation) => participation.person.firstName)
                .join(", ")
            }}
          </span>
          <span v-if="participations.length > 5">
            <!-- eslint-disable @intlify/vue-i18n/no-raw-text -->
            +{{ participations.length - 5 }}
            <!-- eslint-enable @intlify/vue-i18n/no-raw-text -->
          </span>
        </span>
      </template>
    </absence-reason-chip>

    <extra-mark-chip
      v-for="[markId, [mark, ...participations]] in Object.entries(
        extraMarkChips,
      )"
      :key="'extra-mark-' + markId"
      :extra-mark="mark"
      dense
    >
      <template #append>
        <span
          >:
          <span>
            {{
              participations
                .slice(0, 5)
                .map((participation) => participation.person.firstName)
                .join(", ")
            }}
          </span>
          <span v-if="participations.length > 5">
            <!-- eslint-disable @intlify/vue-i18n/no-raw-text -->
            +{{ participations.length - 5 }}
            <!-- eslint-enable @intlify/vue-i18n/no-raw-text -->
          </span>
        </span>
      </template>
    </extra-mark-chip>

    <tardiness-chip v-if="tardyParticipations.length > 0">
      {{ $t("alsijil.personal_notes.late") }}

      <template #append>
        <span
          >:
          {{
            tardyParticipations
              .slice(0, 5)
              .map((participation) => participation.person.firstName)
              .join(", ")
          }}

          <span v-if="tardyParticipations.length > 5">
            <!-- eslint-disable @intlify/vue-i18n/no-raw-text -->
            +{{ tardyParticipations.length - 5 }}
            <!-- eslint-enable @intlify/vue-i18n/no-raw-text -->
          </span>
        </span>
      </template>
    </tardiness-chip>

    <manage-students-trigger
      :label-key="total == 0 ? 'alsijil.coursebook.notes.show_list' : ''"
      v-bind="documentationPartProps"
    />
  </div>
</template>

<script>
import documentationPartMixin from "./documentationPartMixin";
import ManageStudentsTrigger from "../absences/ManageStudentsTrigger.vue";

export default {
  name: "LessonNotes",
  components: { ManageStudentsTrigger },
  mixins: [documentationPartMixin],
  computed: {
    total() {
      return this.documentation.participations.length;
    },
    /**
     * Return the number of present people.
     */
    present() {
      return this.documentation.participations.filter(
        (p) => p.absenceReason === null,
      ).length;
    },
    /**
     * Get all course attendants who have an absence reason, grouped by that reason.
     */
    absences() {
      return Object.groupBy(
        this.documentation.participations.filter(
          (p) => p.absenceReason !== null,
        ),
        ({ absenceReason }) => absenceReason.id,
      );
    },
    /**
     * Parse and combine all extraMark notes.
     *
     * Notes with extraMarks are grouped by ExtraMark. ExtraMarks with the showInCoursebook property set to false are ignored.
     * @return An object where the keys are extraMark IDs and the values have the structure [extraMark, note1, note2, ..., noteN]
     */
    extraMarkChips() {
      // Apply the inner function to each participation, with value being the resulting object
      return this.documentation.participations.reduce((value, p) => {
        // Go through every extra mark of this participation
        for (const { extraMark } of p.notesWithExtraMark) {
          // Only proceed if the extraMark should be displayed here
          if (!extraMark.showInCoursebook) {
            continue;
          }

          // value[extraMark.id] is an Array with the structure [extraMark, note1, note2, ..., noteN]
          if (value[extraMark.id]) {
            value[extraMark.id].push(p);
          } else {
            value[extraMark.id] = [
              this.extraMarks.find((e) => e.id === extraMark.id),
              p,
            ];
          }
        }

        return value;
      }, {});
    },
    /**
     * Return a list Participations with a set tardiness
     */
    tardyParticipations() {
      return this.documentation.participations.filter((p) => p.tardiness);
    },
  },
};
</script>

<style scoped>
.gap {
  gap: 0.25em;
}
</style>
