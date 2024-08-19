<script setup>
import AbsenceReasonChip from "./AbsenceReasonChip.vue";
</script>
<script>
import { gqlAbsenceReasons } from "./helper.graphql";

export default {
  name: "AbsenceReasonGroupSelect",
  extends: "v-chip-group",
  data() {
    return {
      absenceReasons: [],
      innerValue: undefined,
    };
  },
  apollo: {
    absenceReasons: {
      query: gqlAbsenceReasons,
      result({ data }) {
        this.setDefaultReason(data.absenceReasons);
      },
      skip() {
        return this.customAbsenceReasonsExists;
      },
    },
  },
  props: {
    allowEmpty: {
      type: Boolean,
      default: false,
    },
    value: {
      type: [String, Number],
      required: false,
      default: null,
    },
    emptyValue: {
      type: [String, Number],
      required: false,
      default: "present",
    },
    loadSelectedChip: {
      type: Boolean,
      required: false,
      default: false,
    },
    customAbsenceReasons: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  computed: {
    /**
     * Determines whether the chips can be shown.
     *
     * Due to the eagerness of vuetify, we can only mount the chip-group, after the selected item has been loaded.
     * Otherwise, vuetify would set the value to the first existing one. However, if it's possible to not be
     * absent, we can show the chip-group directly, as the present chip is hardcoded.
     *
     * @return {boolean} Whether to mount the chip-group
     */
    showChips() {
      return (
        ((!this.$apollo.queries.absenceReasons.loading &&
          this.absenceReasons.length) ||
          this.customAbsenceReasonsExists ||
          (this.allowEmpty && this.value === this.emptyValue)) &&
        this.innerValue
      );
    },
    customAbsenceReasonsExists() {
      return this.customAbsenceReasons.length > 0;
    },
    innerAbsenceReasons() {
      if (this.customAbsenceReasonsExists) {
        return this.customAbsenceReasons;
      } else {
        return this.absenceReasons;
      }
    },
  },
  mounted() {
    this.innerValue = this.value;
    if (this.customAbsenceReasons) {
      this.setDefaultReason(this.customAbsenceReasons);
    }
  },
  watch: {
    value(newValue) {
      this.innerValue = newValue;
    },
    customAbsenceReasons(newValue) {
      this.setDefaultReason(newValue);
    },
  },
  methods: {
    updateInnerValue($event) {
      this.innerValue = $event;
      this.$emit("input", $event);
    },
    setDefaultReason(absenceReasons) {
      if (!this.innerValue) {
        const defaultReason = absenceReasons.find((ar) => ar.default);
        if (defaultReason) {
          this.updateInnerValue(defaultReason.id);
        }
      }
    },
  },
};
</script>

<template>
  <v-chip-group
    column
    :value="innerValue"
    @change="updateInnerValue"
    mandatory
    v-if="showChips"
  >
    <v-chip
      v-if="allowEmpty"
      color="success"
      :value="emptyValue"
      filter
      outlined
      @click.native="$event.stopPropagation()"
    >
      {{ $t("kolego.absence_reason.present") }}
      <v-avatar right v-if="loadSelectedChip && innerValue === emptyValue">
        <v-progress-circular indeterminate :size="16" :width="2" />
      </v-avatar>
    </v-chip>
    <absence-reason-chip
      v-for="absenceReason in innerAbsenceReasons"
      :key="absenceReason.id"
      :absence-reason="absenceReason"
      filter
      outlined
      :loading="loadSelectedChip && absenceReason.id === innerValue"
      @click.native="$event.stopPropagation()"
    />
  </v-chip-group>
  <v-skeleton-loader v-else type="chip@4" class="d-flex flex-wrap gap" />
</template>

<style scoped>
.gap {
  gap: 0.5em;
}
</style>
