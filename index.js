// const mimusa_python_code_URL = "https://mimusa-test-model.onrender.com/generate"
const mimusa_python_code_URL = "http://127.0.0.1:8000/generate"
const mimusa2_python_code_URL = "http://127.0.0.1:8000/generate2"
// const mimusa_python_code_URL = "https://model.socialopinionanalytics.net/generate"

const app = Vue.createApp({

    //=========== DATA PROPERTIES ===========
    data() {
        return {
            original_text: "",
            sentiment: "",
            final_text: "",
        }
    },

    //=========== METHODS ===========
    methods: {
        get_score() {
            console.log(this.original_text);
            fetch(`${mimusa_python_code_URL}`,
                {
                    method: "POST",
                    headers: {
                        "Content-type": "text/plain"
                    },
                    body: this.original_text
                })
                .then(response => response.json())
                .then(data => {
                    this.sentiment = data.data;
                    this.final_text = data.text;
                    // console.log(data);
                });
        },
        get_score2() {
            console.log(this.original_text);
            fetch(`${mimusa2_python_code_URL}`,
                {
                    method: "POST",
                    headers: {
                        "Content-type": "text/plain"
                    },
                    body: this.original_text
                })
                .then(response => response.json())
                .then(data => {
                    this.sentiment = data.data;
                    this.final_text = data.text;
                    // console.log(data);
                });
        },
    }
})


app.mount('#app')