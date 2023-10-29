/*
MIT License

Copyright (c) 2023 Jakob Felix Rieckers
*/
const canvas = document.getElementById('lightCanvas');
const stateButton = document.getElementById('stateButton')
const heightInput = document.getElementById("heightInput")

const baseButtonStyle = "width: 200px;font-size: xx-large;color:#999;"
let selectedXPercent, selectedYPercent;
var sendData = false;
setButton()

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    // Berechnung der Koordinaten in Prozent
    const canvasWidth = canvas.clientWidth;
    const canvasHeight = canvas.clientHeight;
    selectedXPercent = (mouseX / canvasWidth) * 100;
    selectedYPercent = (mouseY / canvasHeight) * 100;

    if (sendData) {
        fetch("/position-update", {
            method: "POST",
            body: JSON.stringify({
                x: selectedXPercent,
                y: selectedYPercent,
                z: heightInput.value*100 //height in cm
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
    }
});

function setButton() {
    if (sendData) {
        stateButton.style = baseButtonStyle + "background-color: red;"
    } else {
        stateButton.style = baseButtonStyle + "background-color: white;"
    }
}

function changeState() {
    if (sendData) {
        sendData = false;
    } else {
        sendData = true;
    }
    console.log(sendData);
    setButton()
}

canvas.addEventListener('click', (e) => {changeState()});
