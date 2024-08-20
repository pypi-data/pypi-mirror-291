<!-- Wrapper around Documentation.vue -->
<!-- That uses it either as list item or as editable modal dialog. -->
<template>
  <mobile-fullscreen-dialog v-model="popup" max-width="500px">
    <template #activator="activator">
      <!-- list view -> activate dialog -->
      <documentation
        compact
        v-bind="$attrs"
        :dialog-activator="activator"
        :extra-marks="extraMarks"
        :absence-reasons="absenceReasons"
      />
    </template>
    <!-- dialog view -> deactivate dialog -->
    <!-- cancel | save (through lesson-summary) -->
    <documentation
      v-bind="$attrs"
      :extra-marks="extraMarks"
      :absence-reasons="absenceReasons"
      @close="popup = false"
    />
  </mobile-fullscreen-dialog>
</template>

<script>
import MobileFullscreenDialog from "aleksis.core/components/generic/dialogs/MobileFullscreenDialog.vue";
import Documentation from "./Documentation.vue";

export default {
  name: "DocumentationModal",
  components: {
    MobileFullscreenDialog,
    Documentation,
  },
  data() {
    return {
      popup: false,
    };
  },
  props: {
    extraMarks: {
      type: Array,
      required: true,
    },
    absenceReasons: {
      type: Array,
      required: true,
    },
  },
};
</script>
