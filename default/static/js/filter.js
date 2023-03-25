const apiURL = "{{ request.build_absolute_uri }}car_mark_models/"
const form = document.querySelector('select[name=car_mark_select]');
form.addEventListener('click', function (event) {
    let val = event.target.value
    console.log(val);
    if (val == Number(val)) {
        prepareData(val);
    }
});

function prepareData(markId) {
    let modelsRequestURL = apiURL + markId
    let modelsRequest = new XMLHttpRequest();
    modelsRequest.open("GET", modelsRequestURL, true);
    modelsRequest.onerror = function () {
        console.log("modelsRequest Connection Error");
    }
    modelsRequest.onload = function() {
        let json_data = JSON.parse(modelsRequest.responseText)
        console.log(json_data);
    }
    modelsRequest.send();
}