import {model1, model2} from './config.js';

const app = Vue.createApp({

    //=========== DATA PROPERTIES ===========
    data() {
        return {
            original_text: "",
            sentiment: "",
            final_text: "",
            textType: "sentence",
        }
    },

    //=========== METHODS ===========
    methods: {
        get_score() {
            console.log(this.original_text);
            fetch(`${model1}`,
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
            fetch(`${model2}`,
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