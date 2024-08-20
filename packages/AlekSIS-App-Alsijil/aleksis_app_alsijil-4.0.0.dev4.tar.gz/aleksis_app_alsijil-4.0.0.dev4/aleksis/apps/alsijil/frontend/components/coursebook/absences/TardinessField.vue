<script>
import { DateTime } from "luxon";
import documentationPartMixin from "../documentation/documentationPartMixin";
import ConfirmDialog from "aleksis.core/components/generic/dialogs/ConfirmDialog.vue";
import PositiveSmallIntegerField from "aleksis.core/components/generic/forms/PositiveSmallIntegerField.vue";

export default {
  name: "TardinessField",
  components: { ConfirmDialog, PositiveSmallIntegerField },
  mixins: [documentationPartMixin],
  props: {
    value: {
      type: Number,
      default: null,
      required: false,
    },
    participation: {
      type: Object,
      required: true,
    },
  },
  computed: {
    lessonLength() {
      const lessonStart = DateTime.fromISO(this.documentation.datetimeStart);
      const lessonEnd = DateTime.fromISO(this.documentation.datetimeEnd);

      let diff = lessonEnd.diff(lessonStart, "minutes");
      return diff.toObject().minutes;
    },
  },
  methods: {
    lessonLengthRule(time) {
      return (
        time == null ||
        time <= this.lessonLength ||
        this.$t("alsijil.personal_notes.lesson_length_exceeded")
      );
    },
    saveValue(value) {
      this.$emit("input", value);
      this.previousValue = value;
    },
    confirm() {
      this.saveValue(0);
    },
    cancel() {
      this.saveValue(this.previousValue);
    },
    set(newValue) {
      if (!newValue) {
        // this is a DELETE action, show the dialog, ...
        this.showDeleteConfirm = true;
        return;
      }

      this.saveValue(newValue);
    },
  },
  data() {
    return {
      showDeleteConfirm: false,
      previousValue: 0,
    };
  },
  mounted() {
    this.previousValue = this.value;
  },
};
</script>

<template>
  <positive-small-integer-field
    outlined
    class="mt-1"
    prepend-inner-icon="mdi-clock-alert-outline"
    :suffix="$t('time.minutes')"
    :label="$t('alsijil.personal_notes.tardiness')"
    :rules="[lessonLengthRule]"
    :value="value"
    @change="set($event)"
    v-bind="$attrs"
  >
    <template #append>
      <confirm-dialog
        v-model="showDeleteConfirm"
        @confirm="confirm"
        @cancel="cancel"
      >
        <template #title>
          {{ $t("alsijil.personal_notes.confirm_delete") }}
        </template>
        <template #text>
          {{
            $t("alsijil.personal_notes.confirm_delete_tardiness", {
              tardiness: previousValue,
              name: participation.person.fullName,
            })
          }}
        </template>
      </confirm-dialog>
    </template>
  </positive-small-integer-field>
</template>

<style scoped>
.mt-n1-5 {
  margin-top: -6px;
}
</style>
