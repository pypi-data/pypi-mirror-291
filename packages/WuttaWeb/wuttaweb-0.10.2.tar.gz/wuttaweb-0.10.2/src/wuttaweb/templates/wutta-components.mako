
<%def name="make_wutta_components()">
  ${self.make_wutta_button_component()}
</%def>

<%def name="make_wutta_button_component()">
  <script type="text/x-template" id="wutta-button-template">
    <b-button :type="type"
              :native-type="nativeType"
              :tag="tag"
              :href="href"
              :title="title"
              :disabled="buttonDisabled"
              @click="clicked"
              icon-pack="fas"
              :icon-left="iconLeft">
      {{ buttonLabel }}
    </b-button>
  </script>
  <script>
    const WuttaButton = {
        template: '#wutta-button-template',
        props: {
            type: String,
            nativeType: String,
            tag: String,
            href: String,
            label: String,
            title: String,
            iconLeft: String,
            working: String,
            workingLabel: String,
            disabled: Boolean,
            once: Boolean,
        },
        data() {
            return {
                currentLabel: null,
                currentDisabled: null,
            }
        },
        computed: {
            buttonLabel: function() {
                return this.currentLabel || this.label
            },
            buttonDisabled: function() {
                if (this.currentDisabled !== null) {
                    return this.currentDisabled
                }
                return this.disabled
            },
        },
        methods: {

            clicked(event) {
                if (this.once) {
                    this.currentDisabled = true
                    if (this.workingLabel) {
                        this.currentLabel = this.workingLabel
                    } else if (this.working) {
                        this.currentLabel = this.working + ", please wait..."
                    } else {
                        this.currentLabel = "Working, please wait..."
                    }
                }
            }
        },
    }
    Vue.component('wutta-button', WuttaButton)
  </script>
</%def>
