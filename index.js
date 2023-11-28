// const model_url = "https://model.socialopinionanalytics.net"
const model_url = "http://127.0.0.1:8080"

const app = Vue.createApp({

    //=========== DATA PROPERTIES ===========
    data() {
        return {
            original_text: "",
            // sentiment: "",
            // final_text: "",
            text_type: "sentence",
            res_data: null,
            error_message: null,
        }
    },

    //=========== METHODS ===========
    methods: {
        get_score() {
            // console.log(this.original_text);
            fetch(`${model_url + "/generate"}`,
                {
                    method: "POST",
                    headers: {
                        "Content-type": "text/plain"
                    },
                    body: this.original_text
                })
                .then(response => response.json())
                .then(data => {
                    this.res_data = data;

                    if (data.code != 200) {
                        this.error_message = data.data;
                    } else {
                        this.error_message = null;
                    }
                    // this.final_text = data.text;
                    // console.log(data);
                });
        },
        get_score2() {
            // console.log(this.original_text);
            fetch(`${model_url + "/generate2"}`,
                {
                    method: "POST",
                    headers: {
                        "Content-type": "text/plain"
                    },
                    body: this.original_text
                })
                .then(response => response.json())
                .then(data => {
                    this.res_data = data;

                    if (data.code != 200) {
                        this.error_message = data.data;
                    } else {
                        this.error_message = null;
                    }
                    // this.final_text = data.text;
                    // console.log(data);
                })
                ;
        },

        activateTooltip() {
            // Assuming you have an element with the ID 'sentiment-tooltip' in your HTML
            const tooltipElement = document.getElementById('sentiment-tooltip');
            // Check if the tooltipElement is available before creating a new tooltip
            if (tooltipElement) {
                new bootstrap.Tooltip(tooltipElement);
            }
        },
    },

    // =========== LIFECYCLE HOOKS ===========
    updated() {
        this.activateTooltip();
    },
})


app.mount('#app')